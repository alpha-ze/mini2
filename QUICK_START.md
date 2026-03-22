# 🚀 DDGRS Quick Start Guide

## Current System Status

✅ **Working:**
- WhatsApp Bot (Twilio)
- Admin Dashboard (React)
- Database (Supabase)
- ML Service (Ready to test)

---

## Start Everything

### Terminal 1: ML Service (Optional but Recommended)
```bash
cd ml-service
venv\Scripts\activate
python main.py
```
Runs on: http://localhost:8000

**Note:** Your HuggingFace token is already configured in `ml-service/.env`

### Terminal 2: WhatsApp Bot
```bash
# With ML (recommended):
node bot-twilio-ml.js

# Without ML (original):
node bot-twilio.js
```
Runs on: http://localhost:3001

### Terminal 3: Admin Panel
```bash
cd admin-panel
npm run dev
```
Runs on: http://localhost:5173

### Terminal 4: ngrok (for Twilio)
```bash
ngrok http 3001
```
Copy URL to Twilio Console

---

## Quick Test

### Test ML Service
```bash
curl http://localhost:8000/
```

### Test Classification
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"My wifi is not working\"}"
```

### Test Bot
Send WhatsApp message: "start"

---

## Configuration Files

### .env (Root)
```env
# Twilio
TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN=16b4a94801588d548da75d94027a8ce5
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Supabase
SUPABASE_URL=https://qpklahpxqafobibvvcob.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ML Service
ML_SERVICE_URL=http://localhost:8000
ENABLE_AUTO_CLASSIFICATION=true
```

### ml-service/.env
```env
# Classifier mode: distilbert (FREE), openai, anthropic, auto
CLASSIFIER_MODE=distilbert

# Only needed for API modes:
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### admin-panel/.env
```env
VITE_SUPABASE_URL=https://qpklahpxqafobibvvcob.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Features

### Without ML (bot-twilio.js)
- Manual category selection
- Basic tracking
- Admin responses

### With ML (bot-twilio-ml.js)
- ✨ Auto-classification
- ✨ Confidence scores
- ✨ Duplicate detection
- ✨ SLA prediction
- ✨ Smart suggestions

---

## Troubleshooting

### ML Service Won't Start
```bash
python --version  # Need 3.9+
pip install -r requirements.txt --force-reinstall
```

### Bot Can't Connect to ML
```bash
curl http://localhost:8000/  # Check ML is running
# Verify .env has ML_SERVICE_URL=http://localhost:8000
```

### Admin Panel Shows No Data
```bash
# Check Supabase credentials in admin-panel/.env
# Verify grievances exist in database
```

---

## Documentation

- **ML_README.md** - Complete ML guide
- **ML_INTEGRATION_GUIDE.md** - Integration steps
- **START_ML_SYSTEM.md** - Detailed startup
- **ML_IMPLEMENTATION_COMPLETE.md** - What was built
- **DEPLOYMENT_GUIDE.md** - Production deployment
- **PROJECT_STATUS.md** - Full project status

---

## URLs

- ML Service: http://localhost:8000
- Bot: http://localhost:3001
- Admin: http://localhost:5173
- Supabase: https://qpklahpxqafobibvvcob.supabase.co
- GitHub: https://github.com/alpha-ze/ddgrs2

---

## Next Steps

1. ✅ Test ML service locally
2. ✅ Test bot with ML
3. ⏳ Deploy ML service
4. ⏳ Update production URLs
5. ⏳ Monitor performance

---

## Support

Check terminal logs for errors. Each service shows detailed output.
