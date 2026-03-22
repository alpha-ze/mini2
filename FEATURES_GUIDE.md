# 🎯 DDGRS Features Guide

## Complete Feature List & How to Use Them

---

## 1. 🤖 AI-Powered Auto-Classification

**What it does:** Automatically detects the category of your grievance using AI

**How to use:**
1. Send "start" to WhatsApp bot
2. Choose anonymous option
3. Describe your grievance
4. Bot automatically classifies it with confidence score

**Example:**
```
You: "The wifi is not working in my room"
Bot: 🤖 Detected Category: IT / Network
     📊 Confidence: 75%
```

**Categories:**
- Academic
- Examination
- Infrastructure
- Hostel
- Library
- Administration
- IT / Network
- Discipline / Harassment
- Other

---

## 2. 🔍 Duplicate Detection

**What it does:** Checks if similar grievance was submitted in last 72 hours

**How to use:**
- Automatic! When you submit a grievance, it checks for duplicates
- If found, bot asks if you want to submit anyway or track existing one

**Example:**
```
Bot: ⚠️ Similar Grievance Found!
     A similar complaint was submitted recently:
     ID: GRV-000005
     Status: Under Review
     
     Do you still want to submit?
     1️⃣ Yes, submit anyway
     2️⃣ No, track existing one
```

---

## 3. ⏱️ SLA Prediction

**What it does:** Estimates resolution time based on category

**How to use:**
- Automatic! Shows estimated resolution time after classification

**Example:**
```
Bot: ⏱️ Estimated resolution: 2 days
```

**Default SLA Times:**
- IT / Network: 1 day
- Infrastructure: 3 days
- Hostel: 2 days
- Academic: 5 days
- Examination: 3 days
- Administration: 7 days
- Library: 1 day
- Other: 5 days

---

## 4. 📱 WhatsApp Interface

**What it does:** Submit and track grievances via WhatsApp

**Commands:**

### Submit Grievance
```
start
```

### Track Grievance
```
track GRV-000001
```

### Help
```
help
```

**Features:**
- Anonymous submission option
- Text, image, video, audio support
- Step-by-step guided flow
- Real-time status updates

---

## 5. 🎛️ Admin Dashboard

**What it does:** Web interface for managing grievances

**Access:** http://localhost:5173

**Features:**

### Dashboard View
- Total grievances count
- Status breakdown (Submitted, In Progress, Resolved, etc.)
- Recent grievances list
- Quick stats

### Grievance List
- View all grievances
- Filter by status
- Search by ID or description
- Sort by date

### Grievance Detail
- Full grievance information
- Update status (8 levels)
- Add remarks/comments
- View action history timeline
- See all attachments

**Status Levels:**
1. Submitted
2. Acknowledged
3. Under Review
4. In Progress
5. Awaiting Confirmation
6. Resolved
7. Closed
8. Rejected

---

## 6. 📊 Action History

**What it does:** Tracks all status changes and admin actions

**How to use:**
1. Open grievance in admin dashboard
2. Scroll to "Action History" section
3. See timeline of all changes

**Shows:**
- Who made the change
- When it was made
- What status was set
- Remarks added

---

## 7. 🔐 Anonymous Submissions

**What it does:** Submit grievances without revealing identity

**How to use:**
```
Bot: Do you want to submit anonymously?
You: 1 (for Yes)
```

**Benefits:**
- Privacy protection
- Encourages reporting sensitive issues
- Still trackable with GRV-ID

---

## 8. 📎 Media Attachments

**What it does:** Attach images, videos, or audio to grievances

**How to use:**
1. During grievance description step
2. Send image/video/audio file
3. Bot confirms attachment received
4. Continue with text description

**Supported:**
- Images (JPG, PNG)
- Videos (MP4)
- Audio (MP3, WAV)

---

## 9. 🔢 Tracking System

**What it does:** Track grievance status anytime

**How to use:**
```
track GRV-000001
```

**Response shows:**
- Grievance ID
- Category
- Current status
- Submission date
- Description

---

## 10. 🔄 Manual Category Override

**What it does:** Change AI-suggested category

**How to use:**
```
Bot: 🤖 Detected Category: IT / Network
     Type "confirm" to submit
     Type "change" to select different category

You: change

Bot: Select Category:
     1️⃣ Academic
     2️⃣ Hostel
     ...
```

---

## 11. 🔍 Search & Filter (Admin)

**What it does:** Find specific grievances quickly

**How to use:**
1. Open admin dashboard
2. Go to Grievance List
3. Use search bar or filters

**Search by:**
- Grievance ID
- Description keywords
- Status
- Category
- Date range

---

## 12. 💬 Admin Remarks

**What it does:** Add notes/updates to grievances

**How to use:**
1. Open grievance in admin dashboard
2. Scroll to "Update Status" section
3. Select new status
4. Add remarks
5. Click "Update Status"

**Example remarks:**
- "Assigned to IT team"
- "Parts ordered, will fix by Friday"
- "Issue resolved, please verify"

---

## 13. 📈 Confidence Scores

**What it does:** Shows AI classification confidence

**How to use:**
- Automatic! Displayed after AI classification

**Interpretation:**
- 90-100%: Very confident
- 75-89%: Confident
- 60-74%: Moderate confidence
- Below 60%: Manual selection required

---

## 14. 🔔 Real-time Updates

**What it does:** Instant sync between bot and admin panel

**How it works:**
- Submit via WhatsApp → Appears in admin immediately
- Admin updates status → Can be tracked via WhatsApp
- Uses Supabase real-time database

---

## 15. 📱 Multi-step Conversation

**What it does:** Guided grievance submission flow

**Steps:**
1. Anonymous option
2. Grievance description
3. AI classification (with confidence)
4. Confirmation
5. Submission
6. Tracking ID provided

---

## Advanced Features

### 16. 🧠 Hybrid Classifier

**Modes:**
- **DistilBERT (FREE):** Rule-based + ML
- **OpenAI GPT-4 (Paid):** API-based
- **Anthropic Claude (Paid):** API-based
- **Auto:** Tries API first, falls back to DistilBERT

**Configure in:** `ml-service/.env`
```
CLASSIFIER_MODE=distilbert  # FREE
# or
CLASSIFIER_MODE=openai      # Paid
```

### 17. 📊 Analytics (Admin Dashboard)

**Metrics:**
- Total grievances
- Status distribution
- Category breakdown
- Resolution times
- Trends over time

### 18. 🔐 Row Level Security (RLS)

**What it does:** Database-level access control

**Status:** Currently disabled for testing
**Enable:** Run SQL in Supabase:
```sql
ALTER TABLE grievances ENABLE ROW LEVEL SECURITY;
```

---

## Quick Reference

### WhatsApp Commands
| Command | Action |
|---------|--------|
| `start` | Submit new grievance |
| `track GRV-000001` | Check status |
| `help` | Show help |

### Admin Dashboard URLs
| Page | URL |
|------|-----|
| Dashboard | http://localhost:5173 |
| Grievance List | http://localhost:5173/grievances |
| Grievance Detail | http://localhost:5173/grievances/:id |

### ML Service Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /` | Health check |
| `POST /classify` | Classify text |
| `POST /check-duplicate` | Find duplicates |
| `POST /predict-sla` | Estimate resolution time |

---

## Tips & Best Practices

### For Users:
1. Be specific in descriptions
2. Include location/room numbers
3. Attach photos if helpful
4. Track your grievance regularly
5. Use anonymous option for sensitive issues

### For Admins:
1. Update status regularly
2. Add detailed remarks
3. Respond within SLA times
4. Use proper status progression
5. Close resolved grievances

### For Developers:
1. Monitor ML service logs
2. Check classification accuracy
3. Adjust keywords if needed
4. Train custom model with real data
5. Deploy to production when ready

---

## Troubleshooting

### Bot not responding?
- Check ngrok is running
- Verify webhook URL in Twilio
- Check bot logs

### Classification not working?
- Check ML service is running (port 8000)
- Verify HuggingFace token
- Check bot logs for errors

### Admin dashboard empty?
- Verify Supabase credentials
- Check browser console (F12)
- Ensure grievances exist in database

---

## Next Steps

1. ✅ Test all features
2. ✅ Collect real grievance data
3. ⏳ Train custom ML model
4. ⏳ Deploy to production
5. ⏳ Add more features (notifications, reports, etc.)

---

**Need help?** Check the documentation:
- [README.md](README.md) - Project overview
- [ML_README.md](ML_README.md) - ML service details
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment

**Your system is fully functional with all features active! 🎉**
