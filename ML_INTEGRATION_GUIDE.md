# ML Service Integration Guide

## Overview
This guide explains how to integrate the ML service with the WhatsApp bot for automatic grievance classification.

---

## Architecture

```
WhatsApp User → Twilio → Bot (bot-twilio.js) → ML Service (FastAPI) → Classification Result
                                                ↓
                                            Supabase Database
```

---

## Step 1: Start ML Service

### Option A: Using DistilBERT (FREE)
```bash
cd ml-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and set:
CLASSIFIER_MODE=distilbert

# Start service
python main.py
```

### Option B: Using OpenAI/Claude (Paid, More Accurate)
```bash
cd ml-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and set:
CLASSIFIER_MODE=openai  # or "anthropic"
OPENAI_API_KEY=sk-your-key-here

# Start service
python main.py
```

### Option C: Auto Mode (Hybrid)
```bash
# Edit .env and set:
CLASSIFIER_MODE=auto
OPENAI_API_KEY=sk-your-key-here  # Optional

# If API key is provided, uses API
# If not, falls back to DistilBERT
```

ML Service will run on: `http://localhost:8000`

---

## Step 2: Test ML Service

```bash
# Test health endpoint
curl http://localhost:8000/

# Test classification
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "My wifi is not working in hostel room"}'

# Expected response:
{
  "department": "IT Cell",
  "confidence": 0.92,
  "all_predictions": {...},
  "classifier_used": "AI (GPT-4/Claude)"  # or "DistilBERT (FREE)"
}
```

---

## Step 3: Update Bot Configuration

Add ML service URL to `.env`:

```env
# ML Service Configuration
ML_SERVICE_URL=http://localhost:8000
ENABLE_AUTO_CLASSIFICATION=true
```

---

## Step 4: Bot Integration Options

### Option 1: Automatic Classification (Recommended)
Bot automatically classifies grievances, user can override if needed.

**Flow:**
1. User describes grievance
2. Bot calls ML service for classification
3. Bot shows: "Detected category: IT Cell (92% confidence)"
4. User confirms or selects different category
5. Grievance submitted

### Option 2: Smart Suggestions
Bot suggests categories based on ML, user selects.

**Flow:**
1. User describes grievance
2. Bot calls ML service
3. Bot shows: "Suggested: IT Cell, Maintenance, Hostel"
4. User selects from suggestions
5. Grievance submitted

### Option 3: Silent Classification
Bot classifies in background, no user interaction.

**Flow:**
1. User describes grievance
2. Bot calls ML service
3. Category auto-assigned
4. Grievance submitted
5. Admin can reclassify if needed

---

## Step 5: Deploy ML Service

### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Deploy
railway up

# Get URL
railway domain
```

### Render Deployment
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from .env
7. Deploy

---

## API Endpoints

### 1. Classify Grievance
```http
POST /classify
Content-Type: application/json

{
  "text": "My laptop is not connecting to college wifi",
  "threshold": 0.7
}

Response:
{
  "department": "IT Cell",
  "confidence": 0.89,
  "all_predictions": {
    "IT Cell": 0.89,
    "Maintenance": 0.05,
    "Hostel": 0.03,
    ...
  },
  "classifier_used": "AI (GPT-4/Claude)"
}
```

### 2. Check Duplicate
```http
POST /check-duplicate
Content-Type: application/json

{
  "text": "Wifi not working in room 301",
  "recent_complaints": [
    {"id": "GRV-000001", "description": "Internet down in hostel", "created_at": "2024-01-01"}
  ],
  "time_window_hours": 72
}

Response:
{
  "is_duplicate": true,
  "similar_complaint": {"id": "GRV-000001", ...},
  "similarity_score": 0.92
}
```

### 3. Predict SLA
```http
POST /predict-sla
Content-Type: application/json

{
  "department": "IT Cell",
  "category": "Network",
  "description": "Wifi issue",
  "priority": "high"
}

Response:
{
  "estimated_hours": 4.5,
  "estimated_days": 0.19,
  "confidence": 0.85
}
```

### 4. Extract Information
```http
POST /extract-info
Content-Type: application/json

{
  "text": "My room AC is broken"
}

Response:
{
  "missing_fields": ["location", "urgency"],
  "extracted_info": {
    "issue": "AC broken",
    "category": "Maintenance"
  },
  "follow_up_questions": [
    "Which room number?",
    "How urgent is this issue?"
  ]
}
```

---

## Cost Comparison

### DistilBERT (FREE)
- Cost: $0/month
- Accuracy: 85-90%
- Speed: 100-200ms
- Setup: Requires training data
- Maintenance: Model retraining needed

### OpenAI GPT-4 (Paid)
- Cost: ~$10-20/month (1000 classifications)
- Accuracy: 90-95%
- Speed: 500-1000ms
- Setup: Just API key
- Maintenance: None

### Anthropic Claude (Paid)
- Cost: ~$10-20/month
- Accuracy: 90-95%
- Speed: 500-1000ms
- Setup: Just API key
- Maintenance: None

---

## Monitoring

### Check Service Health
```bash
curl http://localhost:8000/health

Response:
{
  "status": "healthy",
  "models_loaded": {
    "classifier": true,
    "duplicate_detector": true,
    "sla_predictor": true,
    "info_extractor": true
  }
}
```

### View Logs
```bash
# Local
tail -f ml-service.log

# Railway
railway logs

# Render
View in dashboard
```

---

## Troubleshooting

### Issue: ML Service won't start
```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for errors
python main.py
```

### Issue: Classification not working
```bash
# Test endpoint directly
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'

# Check logs for errors
# Verify API keys in .env
```

### Issue: Bot can't connect to ML service
```bash
# Check ML service is running
curl http://localhost:8000/

# Check bot .env has correct URL
# Check firewall/network settings
```

---

## Next Steps

1. ✅ Start ML service locally
2. ✅ Test classification endpoint
3. ✅ Update bot code (see bot-twilio-ml.js)
4. ✅ Test end-to-end flow
5. ✅ Deploy ML service to cloud
6. ✅ Update bot with production URL
7. ✅ Monitor and optimize

---

## Support

For issues or questions:
1. Check logs: `python main.py` output
2. Test endpoints with curl
3. Verify environment variables
4. Check API key validity (if using paid APIs)
