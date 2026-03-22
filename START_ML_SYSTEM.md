# 🚀 Start AI-Powered Grievance System

## Quick Start Guide

### Option 1: Start Everything (Recommended for Testing)

#### Terminal 1: Start ML Service
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env and set:
# CLASSIFIER_MODE=auto  (tries API, falls back to DistilBERT)
# or
# CLASSIFIER_MODE=distilbert  (FREE, no API key needed)

python main.py
```

ML Service will run on: http://localhost:8000

#### Terminal 2: Start WhatsApp Bot (with ML)
```bash
# Make sure .env has:
# ML_SERVICE_URL=http://localhost:8000
# ENABLE_AUTO_CLASSIFICATION=true

node bot-twilio-ml.js
```

Bot will run on: http://localhost:3001

#### Terminal 3: Start Admin Panel
```bash
cd admin-panel
npm run dev
```

Admin panel will run on: http://localhost:5173

#### Terminal 4: Start ngrok (for Twilio webhook)
```bash
ngrok http 3001
```

Copy the ngrok URL and configure in Twilio Console.

---

### Option 2: Start Without ML (Original Bot)

If you don't want AI features yet:

```bash
# Terminal 1: Bot
node bot-twilio.js

# Terminal 2: Admin Panel
cd admin-panel
npm run dev

# Terminal 3: ngrok
ngrok http 3001
```

---

## Testing ML Service

### Test 1: Health Check
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "service": "DDGRS AI Service",
  "status": "running",
  "classifier": {
    "mode": "auto",
    "active_classifier": "distilbert",
    "cost": "FREE"
  }
}
```

### Test 2: Classification
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"My wifi is not working in hostel room 301\"}"
```

Expected response:
```json
{
  "department": "IT Cell",
  "confidence": 0.89,
  "all_predictions": {...},
  "classifier_used": "DistilBERT (FREE)"
}
```

### Test 3: Duplicate Detection
```bash
curl -X POST http://localhost:8000/check-duplicate \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Wifi not working\", \"recent_complaints\": [], \"time_window_hours\": 72}"
```

---

## Testing End-to-End Flow

1. Send WhatsApp message to Twilio number: "start"
2. Select anonymous option: "1"
3. Describe grievance: "My laptop cannot connect to college wifi"
4. Bot will auto-classify using ML
5. Confirm submission: "confirm"
6. Check admin panel for new grievance
7. Track grievance: "track GRV-000001"

---

## Switching Between Classifiers

### Use DistilBERT (FREE)
Edit `ml-service/.env`:
```env
CLASSIFIER_MODE=distilbert
```

Restart ML service.

### Use OpenAI GPT-4 (Paid, More Accurate)
Edit `ml-service/.env`:
```env
CLASSIFIER_MODE=openai
OPENAI_API_KEY=sk-your-key-here
```

Restart ML service.

### Use Auto Mode (Hybrid)
Edit `ml-service/.env`:
```env
CLASSIFIER_MODE=auto
OPENAI_API_KEY=sk-your-key-here  # Optional
```

If API key is provided, uses API. Otherwise, uses DistilBERT.

---

## Troubleshooting

### ML Service won't start
```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Bot can't connect to ML service
```bash
# Check ML service is running
curl http://localhost:8000/

# Check .env has correct URL
# ML_SERVICE_URL=http://localhost:8000
```

### Classification not working
```bash
# Check ML service logs
# Look for errors in terminal running python main.py

# Test classification directly
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"test\"}"
```

### Bot still using manual category selection
```bash
# Check .env has:
# ENABLE_AUTO_CLASSIFICATION=true

# Restart bot
# Ctrl+C and run: node bot-twilio-ml.js
```

---

## What's Different with ML?

### Without ML (bot-twilio.js):
1. User describes grievance
2. Bot shows 4 categories
3. User selects manually
4. Grievance submitted

### With ML (bot-twilio-ml.js):
1. User describes grievance
2. Bot auto-classifies using AI
3. Bot shows detected category + confidence
4. User confirms or changes
5. Grievance submitted with AI metadata

---

## Cost Comparison

| Mode | Cost | Accuracy | Speed | Setup |
|------|------|----------|-------|-------|
| DistilBERT | FREE | 85-90% | 100-200ms | Medium |
| OpenAI GPT-4 | $10-20/mo | 90-95% | 500-1000ms | Easy |
| Anthropic Claude | $10-20/mo | 90-95% | 500-1000ms | Easy |
| Auto (Hybrid) | $0-20/mo | 85-95% | Variable | Easy |

---

## Next Steps

1. ✅ Start ML service locally
2. ✅ Test classification endpoint
3. ✅ Start bot with ML integration
4. ✅ Test end-to-end flow
5. ⏳ Deploy ML service to cloud
6. ⏳ Update bot with production URL
7. ⏳ Monitor and optimize

---

## Support

Check logs in each terminal for errors. ML service logs show which classifier is active and any errors.
