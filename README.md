# 🤖 AI-Powered WhatsApp Grievance Management System (DDGRS)

A complete AI-powered grievance management system for educational institutions with WhatsApp interface, admin dashboard, and intelligent classification.

## ✨ Key Features

- 🤖 **AI-Powered Classification** - Automatic department detection using ML
- 📱 **WhatsApp Interface** - Easy-to-use conversational bot
- 💻 **Modern Admin Dashboard** - React-based management interface
- 🔍 **Duplicate Detection** - Finds similar existing complaints
- ⏱️ **SLA Prediction** - Estimates resolution time
- 🗄️ **Cloud Database** - PostgreSQL via Supabase
- 🎯 **Hybrid AI** - Supports FREE (DistilBERT) and PAID (GPT-4/Claude) modes

## 🚀 Quick Start

**New to the project?** Start here:

1. **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Understand what was built
3. **[WHATS_NEXT.md](WHATS_NEXT.md)** - Know what to do next

**Full documentation index:** [README_INDEX.md](README_INDEX.md)

## 📚 Documentation

### Getting Started
- [QUICK_START.md](QUICK_START.md) - Fast startup guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete overview
- [WHATS_NEXT.md](WHATS_NEXT.md) - Action plan

### ML/AI Features
- [ML_README.md](ML_README.md) - Complete ML documentation
- [ML_INTEGRATION_GUIDE.md](ML_INTEGRATION_GUIDE.md) - Integration guide
- [START_ML_SYSTEM.md](START_ML_SYSTEM.md) - Startup instructions
- [ML_IMPLEMENTATION_COMPLETE.md](ML_IMPLEMENTATION_COMPLETE.md) - What was built

### System & Architecture
- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Architecture overview
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Project status & roadmap
- [FEATURES.md](FEATURES.md) - Feature list

### Setup & Deployment
- [SETUP_TWILIO.md](SETUP_TWILIO.md) - Twilio WhatsApp setup
- [SUPABASE_INSTRUCTIONS.md](SUPABASE_INSTRUCTIONS.md) - Database setup
- [ADMIN_PANEL_SETUP.md](ADMIN_PANEL_SETUP.md) - Admin dashboard setup
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment checklist

## 🎯 System Components

### 1. WhatsApp Bot
**Files:** `bot-twilio.js` (basic), `bot-twilio-ml.js` (with ML)

**Features:**
- Conversational interface
- Anonymous submissions
- Media attachments (images, videos, audio)
- Tracking with unique IDs (GRV-000001)
- Auto-classification with ML
- Duplicate detection alerts
- SLA predictions

### 2. ML Service
**Location:** `ml-service/`

**Features:**
- Hybrid classifier (DistilBERT + GPT-4 + Claude)
- Automatic department classification
- Duplicate detection
- SLA prediction
- Information extraction
- FastAPI REST API

**Modes:**
- DistilBERT (FREE) - 85-90% accuracy
- OpenAI GPT-4 (Paid) - 90-95% accuracy
- Anthropic Claude (Paid) - 90-95% accuracy
- Auto (Hybrid) - Fallback support

### 3. Admin Dashboard
**Location:** `admin-panel/`

**Features:**
- Modern React + TypeScript UI
- Real-time grievance list
- Detailed grievance view
- Status management (8 levels)
- Admin remarks system
- Action history timeline
- User authentication

### 4. Database
**Platform:** Supabase (PostgreSQL)

**Features:**
- Auto-generated IDs (GRV-000001)
- Timestamp tracking
- Media URL storage
- Action history
- RLS policies

## 🏗️ Architecture

```
WhatsApp User → Twilio → Bot → ML Service → Classification
                           ↓
                      Supabase Database
                           ↓
                    Admin Dashboard
```

## 💻 Technology Stack

- **Frontend:** React 18, TypeScript, Tailwind CSS, Vite
- **Backend:** Node.js, Express, Python, FastAPI
- **Database:** PostgreSQL (Supabase)
- **Messaging:** Twilio WhatsApp API
- **AI/ML:** HuggingFace Transformers, OpenAI, Anthropic
- **Hosting:** Vercel (frontend), Railway/Render (backend)

## 🚀 Installation

### Prerequisites
- Node.js 16+
- Python 3.9+
- Twilio account
- Supabase account
- OpenAI/Anthropic API key (optional)

### Step 1: Clone Repository
```bash
git clone https://github.com/alpha-ze/ddgrs2.git
cd ddgrs2
npm install
```

### Step 2: Configure Environment
```bash
# Copy and edit .env
cp .env.example .env

# Add your credentials:
# - Twilio credentials
# - Supabase URL and key
# - ML service URL
```

### Step 3: Set Up ML Service
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Configure ML mode
cp .env.example .env
# Edit .env: Set CLASSIFIER_MODE=distilbert (FREE) or openai (Paid)
```

### Step 4: Set Up Admin Panel
```bash
cd admin-panel
npm install

# Configure Supabase
cp .env.example .env
# Edit .env: Add Supabase credentials
```

## 🎮 Running the System

### Terminal 1: ML Service
```bash
cd ml-service
venv\Scripts\activate
python main.py
```
Runs on: http://localhost:8000

### Terminal 2: WhatsApp Bot
```bash
# With ML (recommended):
node bot-twilio-ml.js

# Without ML:
node bot-twilio.js
```
Runs on: http://localhost:3001

### Terminal 3: Admin Panel
```bash
cd admin-panel
npm run dev
```
Runs on: http://localhost:5173

### Terminal 4: ngrok (for Twilio webhook)
```bash
ngrok http 3001
```
Copy URL to Twilio Console

## 🧪 Testing

### Test ML Service
```bash
curl http://localhost:8000/

curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"My wifi is not working\"}"
```

### Test Bot
Send WhatsApp message: "start"

### Test Admin Dashboard
Open: http://localhost:5173

## 📊 Comparison: With vs Without ML

### Without ML (bot-twilio.js)
```
User: My wifi is not working
Bot: Select category: 1-4
User: 1
Bot: ✅ Submitted!
```

### With ML (bot-twilio-ml.js)
```
User: My wifi is not working in hostel
Bot: 🤖 Detected: IT Cell (89%)
     ⏱️ Estimated: 1 day
     Type "confirm" to submit
User: confirm
Bot: ✅ Submitted! Track: GRV-000001
```

## 💰 Cost Analysis

### Development (FREE)
- Supabase: FREE
- Vercel: FREE
- Railway: FREE ($5 credit)
- Twilio: ~$0-5/month
- ML: FREE (DistilBERT)

**Total: $0-5/month**

### Production (With ML)
- Supabase: FREE
- Vercel: FREE
- Railway: $10-20/month
- Twilio: $5-10/month
- ML Service: $10-20/month
- OpenAI API: $10-20/month (optional)

**Total: $30-50/month**

## 🎯 Use Cases

- Educational institutions (colleges, universities)
- Corporate grievance systems
- Customer support automation
- Complaint management
- Feedback collection

## 🔒 Security

- Anonymous submissions supported
- User IDs hashed for privacy
- Media URLs proxied
- RLS policies on database
- API key protection

## 📈 Performance

- Bot response: <2s
- ML classification: 100-1000ms
- Database queries: <100ms
- Admin load: <1s
- Concurrent users: ~100

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Quick deploy:**
- Frontend: Vercel (automatic from GitHub)
- Backend: Railway or Render
- Database: Supabase (already cloud)
- ML Service: Railway or Render

## 🤝 Contributing

This is a complete, production-ready system. For customization:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Twilio for WhatsApp API
- Supabase for database
- HuggingFace for ML models
- OpenAI/Anthropic for AI APIs

## 📞 Support

For issues or questions:
1. Check [README_INDEX.md](README_INDEX.md) for documentation
2. Review troubleshooting sections
3. Check logs for errors
4. Verify configuration

## 🌟 Star This Repo

If you find this useful, please star the repository!

## 🔗 Links

- **GitHub:** https://github.com/alpha-ze/ddgrs2
- **Documentation:** [README_INDEX.md](README_INDEX.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)

---

**Built with ❤️ for educational institutions**
