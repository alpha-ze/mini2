require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const twilio = require('twilio');
const axios = require('axios');
const Database = require('./database-supabase');

const app = express();
const db = new Database();

// Twilio credentials
const accountSid = process.env.TWILIO_ACCOUNT_SID || 'your_account_sid';
const authToken = process.env.TWILIO_AUTH_TOKEN || 'your_auth_token';
const client = twilio(accountSid, authToken);

const TWILIO_WHATSAPP_NUMBER = process.env.TWILIO_WHATSAPP_NUMBER || 'whatsapp:+14155238886';

// ML Service Configuration
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
const ENABLE_AUTO_CLASSIFICATION = process.env.ENABLE_AUTO_CLASSIFICATION === 'true';

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const userSessions = new Map();

const DEPARTMENTS = {
    '1': 'Academic',
    '2': 'Hostel',
    '3': 'Infrastructure',
    '4': 'IT / Network',
    '5': 'Library',
    '6': 'Administration',
    '7': 'Examination',
    '8': 'Other'
};

// Call ML service for classification
async function classifyGrievance(text) {
    try {
        console.log('🔍 Calling ML classification for:', text.substring(0, 50));
        const response = await axios.post(`${ML_SERVICE_URL}/classify`, {
            text: text,
            threshold: 0.7
        }, {
            timeout: 5000
        });
        console.log('✅ Classification result:', JSON.stringify(response.data));
        return response.data;
    } catch (error) {
        console.error('ML classification error:', error.message);
        return null;
    }
}

// Check for duplicate grievances
async function checkDuplicate(text) {
    try {
        // Get recent grievances from database
        const recentGrievances = await db.getRecentGrievances(72); // 72 hours
        
        const response = await axios.post(`${ML_SERVICE_URL}/check-duplicate`, {
            text: text,
            recent_complaints: recentGrievances,
            time_window_hours: 72
        }, {
            timeout: 5000
        });
        return response.data;
    } catch (error) {
        console.error('Duplicate check error:', error.message);
        return null;
    }
}

// Predict SLA
async function predictSLA(department, description) {
    try {
        const response = await axios.post(`${ML_SERVICE_URL}/predict-sla`, {
            department: department,
            category: department,
            description: description,
            priority: 'medium'
        }, {
            timeout: 5000
        });
        return response.data;
    } catch (error) {
        console.error('SLA prediction error:', error.message);
        return null;
    }
}

// Webhook endpoint for incoming WhatsApp messages
app.post('/webhook', async (req, res) => {
    const userId = req.body.From;
    const userMessage = req.body.Body.trim();
    
    console.log(`Message from ${userId}: ${userMessage}`);

    let responseMessage = '';

    // Check for tracking command
    if (userMessage.toLowerCase().startsWith('track ')) {
        const trackingId = userMessage.split(' ')[1];
        const grievance = await db.getGrievanceById(trackingId);
        
        if (grievance) {
            responseMessage = 
                `📋 Grievance Status\n\n` +
                `Tracking ID: ${grievance.grievance_id}\n` +
                `Category: ${grievance.category}\n` +
                `Status: ${grievance.status}\n` +
                `Submitted: ${new Date(grievance.created_at).toLocaleString()}\n\n`;
            
            if (grievance.response) {
                responseMessage += `Admin Response:\n${grievance.response}\n\n`;
            } else {
                responseMessage += `Your grievance is being reviewed.\n\n`;
            }
            
            responseMessage += `Type "start" to submit a new grievance.`;
        } else {
            responseMessage = `❌ Tracking ID ${trackingId} not found.\n\nPlease check the ID and try again.`;
        }
        
        await client.messages.create({
            body: responseMessage,
            from: TWILIO_WHATSAPP_NUMBER,
            to: userId
        });
        
        return res.status(200).send('OK');
    }

    if (!userSessions.has(userId)) {
        userSessions.set(userId, { step: 'start' });
    }

    const session = userSessions.get(userId);

    try {
        if (userMessage.toLowerCase() === 'start' || session.step === 'start') {
            session.step = 'anonymous';
            responseMessage = 
                '👋 Welcome to AI-Powered Grievance System\n\n' +
                'Do you want to submit anonymously?\n' +
                '1️⃣ Yes (Anonymous)\n' +
                '2️⃣ No (With my details)\n\n' +
                'Reply with 1 or 2';
                
        } else if (session.step === 'anonymous') {
            if (userMessage === '1') {
                session.isAnonymous = true;
                session.step = 'grievance';
                responseMessage = 
                    '✅ Anonymous submission selected\n\n' +
                    '📝 Please describe your grievance:\n' +
                    '(You can send text, images, audio, or video)\n\n' +
                    (ENABLE_AUTO_CLASSIFICATION ? 
                        '🤖 AI will automatically detect the category' : 
                        'You will select the category next');
            } else if (userMessage === '2') {
                session.isAnonymous = false;
                session.step = 'grievance';
                responseMessage = 
                    '✅ Submission with details\n\n' +
                    '📝 Please describe your grievance:\n' +
                    '(You can send text, images, audio, or video)\n\n' +
                    (ENABLE_AUTO_CLASSIFICATION ? 
                        '🤖 AI will automatically detect the category' : 
                        'You will select the category next');
            } else {
                responseMessage = '❌ Invalid selection. Please reply with 1 or 2.';
            }
            
        } else if (session.step === 'grievance') {
            // Handle media attachments
            const numMedia = parseInt(req.body.NumMedia) || 0;
            let mediaUrls = [];
            
            for (let i = 0; i < numMedia; i++) {
                const mediaUrl = req.body[`MediaUrl${i}`];
                const mediaType = req.body[`MediaContentType${i}`];
                if (mediaUrl) {
                    mediaUrls.push({ url: mediaUrl, type: mediaType });
                }
            }
            
            session.grievance = userMessage;
            session.mediaUrls = mediaUrls;
            
            // Check for duplicates
            const duplicateCheck = await checkDuplicate(userMessage);
            if (duplicateCheck && duplicateCheck.is_duplicate) {
                responseMessage = 
                    `⚠️ Similar Grievance Found!\n\n` +
                    `A similar complaint was submitted recently:\n` +
                    `ID: ${duplicateCheck.similar_complaint.grievance_id}\n` +
                    `Status: ${duplicateCheck.similar_complaint.status}\n\n` +
                    `Do you still want to submit?\n` +
                    `1️⃣ Yes, submit anyway\n` +
                    `2️⃣ No, track existing one\n\n` +
                    `Reply with 1 or 2`;
                session.step = 'duplicate_confirm';
                session.duplicateId = duplicateCheck.similar_complaint.grievance_id;
            } else if (ENABLE_AUTO_CLASSIFICATION) {
                // Auto-classify using ML
                const classification = await classifyGrievance(userMessage);
                
                if (classification && classification.confidence > 0.7) {
                    session.department = classification.department;
                    session.confidence = classification.confidence;
                    session.classifierUsed = classification.classifier_used;
                    
                    // Predict SLA
                    const sla = await predictSLA(classification.department, userMessage);
                    let slaText = '';
                    if (sla) {
                        const days = Math.ceil(sla.estimated_days);
                        slaText = `\n⏱️ Estimated resolution: ${days} day${days > 1 ? 's' : ''}`;
                    }
                    
                    let mediaInfo = '';
                    if (mediaUrls.length > 0) {
                        mediaInfo = `\nAttachments: ${mediaUrls.length} file(s)`;
                    }
                    
                    session.step = 'confirm';
                    responseMessage = 
                        '📝 Summary:\n' +
                        `🤖 Detected Category: ${session.department}\n` +
                        `📊 Confidence: ${(classification.confidence * 100).toFixed(0)}%\n` +
                        `🔧 Classifier: ${classification.classifier_used}\n` +
                        `Anonymous: ${session.isAnonymous ? 'Yes' : 'No'}\n` +
                        `Grievance: ${session.grievance}${mediaInfo}${slaText}\n\n` +
                        'Type "confirm" to submit\n' +
                        'Type "change" to select different category\n' +
                        'Type "cancel" to restart';
                } else {
                    // Low confidence, ask user to select
                    session.step = 'category';
                    responseMessage = 
                        '⚠️ Could not auto-detect category\n\n' +
                        'Please select category:\n' +
                        '1️⃣ Academic\n' +
                        '2️⃣ Hostel\n' +
                        '3️⃣ Infrastructure\n' +
                        '4️⃣ IT / Network\n' +
                        '5️⃣ Library\n' +
                        '6️⃣ Administration\n' +
                        '7️⃣ Examination\n' +
                        '8️⃣ Other\n\n' +
                        'Reply with the number (1-8)';
                }
            } else {
                // Manual category selection
                session.step = 'category';
                responseMessage = 
                    'Select Category:\n' +
                    '1️⃣ Academic\n' +
                    '2️⃣ Hostel\n' +
                    '3️⃣ Infrastructure\n' +
                    '4️⃣ IT / Network\n' +
                    '5️⃣ Library\n' +
                    '6️⃣ Administration\n' +
                    '7️⃣ Examination\n' +
                    '8️⃣ Other\n\n' +
                    'Reply with the number (1-8)';
            }
            
        } else if (session.step === 'duplicate_confirm') {
            if (userMessage === '1') {
                // Continue with submission
                if (ENABLE_AUTO_CLASSIFICATION) {
                    const classification = await classifyGrievance(session.grievance);
                    if (classification && classification.confidence > 0.7) {
                        session.department = classification.department;
                        session.step = 'confirm';
                        responseMessage = 
                            '📝 Summary:\n' +
                            `Category: ${session.department} (Auto-detected)\n` +
                            `Anonymous: ${session.isAnonymous ? 'Yes' : 'No'}\n` +
                            `Grievance: ${session.grievance}\n\n` +
                            'Type "confirm" to submit or "cancel" to restart';
                    } else {
                        session.step = 'category';
                        responseMessage = 'Please select category (1-8):';
                    }
                } else {
                    session.step = 'category';
                    responseMessage = 'Please select category (1-8):';
                }
            } else if (userMessage === '2') {
                responseMessage = 
                    `Track existing grievance:\n` +
                    `track ${session.duplicateId}\n\n` +
                    `Type "start" to submit a new grievance.`;
                userSessions.delete(userId);
            } else {
                responseMessage = 'Please reply with 1 or 2.';
            }
            
        } else if (session.step === 'category') {
            if (DEPARTMENTS[userMessage]) {
                session.department = DEPARTMENTS[userMessage];
                session.step = 'confirm';
                
                let mediaInfo = '';
                if (session.mediaUrls && session.mediaUrls.length > 0) {
                    mediaInfo = `\nAttachments: ${session.mediaUrls.length} file(s)`;
                }
                
                responseMessage = 
                    '📝 Summary:\n' +
                    `Category: ${session.department}\n` +
                    `Anonymous: ${session.isAnonymous ? 'Yes' : 'No'}\n` +
                    `Grievance: ${session.grievance}${mediaInfo}\n\n` +
                    'Type "confirm" to submit or "cancel" to restart';
            } else {
                responseMessage = '❌ Invalid selection. Please reply with a number between 1-8.';
            }
            
        } else if (session.step === 'confirm') {
            if (userMessage.toLowerCase() === 'confirm') {
                const displayUserId = session.isAnonymous ? 'Anonymous' : userId;
                const grievanceId = await db.addGrievance({
                    userId: displayUserId,
                    department: session.department,
                    grievance: session.grievance,
                    status: 'Submitted',
                    isAnonymous: session.isAnonymous,
                    mediaUrls: JSON.stringify(session.mediaUrls || []),
                    confidence: session.confidence || null,
                    classifierUsed: session.classifierUsed || 'Manual'
                });
                
                let aiInfo = '';
                if (session.classifierUsed) {
                    aiInfo = `\n🤖 Classified by: ${session.classifierUsed}`;
                }
                
                responseMessage = 
                    `✅ Your grievance has been submitted!\n` +
                    `Tracking ID: ${grievanceId}${aiInfo}\n\n` +
                    `Track your grievance anytime by sending:\n` +
                    `track ${grievanceId}\n\n` +
                    `Type "start" to submit another grievance.`;
                userSessions.delete(userId);
            } else if (userMessage.toLowerCase() === 'change') {
                session.step = 'category';
                responseMessage = 
                    'Select Category:\n' +
                    '1️⃣ Academic\n' +
                    '2️⃣ Hostel\n' +
                    '3️⃣ Infrastructure\n' +
                    '4️⃣ IT / Network\n' +
                    '5️⃣ Library\n' +
                    '6️⃣ Administration\n' +
                    '7️⃣ Examination\n' +
                    '8️⃣ Other\n\n' +
                    'Reply with the number (1-8)';
            } else if (userMessage.toLowerCase() === 'cancel') {
                userSessions.delete(userId);
                responseMessage = '❌ Cancelled. Type "start" to begin again.';
            } else {
                responseMessage = 'Please type "confirm", "change", or "cancel"';
            }
        }

        // Send response via Twilio
        await client.messages.create({
            body: responseMessage,
            from: TWILIO_WHATSAPP_NUMBER,
            to: userId
        });

        res.status(200).send('OK');
    } catch (error) {
        console.error('Error processing message:', error);
        res.status(500).send('Error');
    }
});

// Function to send admin responses
async function sendResponseToUser(userId, message) {
    try {
        await client.messages.create({
            body: `📢 Admin Response:\n\n${message}\n\nThank you for your patience!`,
            from: TWILIO_WHATSAPP_NUMBER,
            to: userId
        });
        console.log(`Response sent to ${userId}`);
        return true;
    } catch (error) {
        console.error('Error sending response:', error);
        return false;
    }
}

// Endpoint to proxy Twilio media
app.get('/media/:messageId/:index', async (req, res) => {
    try {
        const { messageId, index } = req.params;
        const grievance = await db.getGrievanceById(messageId);
        
        if (!grievance || !grievance.mediaUrls) {
            return res.status(404).send('Media not found');
        }
        
        const mediaUrls = JSON.parse(grievance.mediaUrls);
        const media = mediaUrls[index];
        
        if (!media) {
            return res.status(404).send('Media not found');
        }
        
        const response = await fetch(media.url, {
            headers: {
                'Authorization': 'Basic ' + Buffer.from(`${accountSid}:${authToken}`).toString('base64')
            }
        });
        
        const buffer = await response.buffer();
        res.set('Content-Type', media.type);
        res.send(buffer);
    } catch (error) {
        console.error('Error fetching media:', error);
        res.status(500).send('Error fetching media');
    }
});

// Monitor database for admin responses
setInterval(async () => {
    try {
        const grievances = await db.getAllGrievances();
        const resolved = grievances.filter(g => g.status === 'Resolved' && !g.responseSent && g.response);
        
        for (const grievance of resolved) {
            if (grievance.userId !== 'Anonymous') {
                const success = await sendResponseToUser(
                    grievance.userId, 
                    `Tracking ID: ${grievance.id}\n\n${grievance.response}`
                );
                
                if (success) {
                    await db.markResponseSent(grievance.id);
                }
            } else {
                await db.markResponseSent(grievance.id);
            }
        }
    } catch (error) {
        console.error('Error checking for responses:', error);
    }
}, 5000);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🤖 AI-Powered WhatsApp Bot running on port ${PORT}`);
    console.log(`📡 Webhook URL: http://localhost:${PORT}/webhook`);
    console.log(`🧠 ML Service: ${ML_SERVICE_URL}`);
    console.log(`🎯 Auto-Classification: ${ENABLE_AUTO_CLASSIFICATION ? 'Enabled' : 'Disabled'}`);
    console.log('Configure webhook URL in Twilio Console');
});

module.exports = { sendResponseToUser };
