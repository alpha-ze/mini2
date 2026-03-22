# 🤖 AI/ML Integration for DDGRS

## Overview

The ML service adds intelligent features to the grievance system:

1. **Automatic Classification** - AI detects the right department
2. **Duplicate Detection** - Finds similar existing complaints
3. **SLA Prediction** - Estimates resolution time
4. **Smart Information Extraction** - Identifies missing details

---

## 🎯 Hybrid Classifier System

The system supports THREE classification modes:

### 1. DistilBERT (FREE) 🆓
- **Cost:** $0/month
- **Accuracy:** 85-90%
- **Speed:** 100-200ms
- **Pros:** Free, fast, runs locally
- **Cons:** Requires training data, lower accuracy
- **Best for:** Budget-conscious, high-volume usage

### 2. OpenAI GPT-4 (Paid) 💰
- **Cost:** ~$10-20/month (1000 classifications)
- **Accuracy:** 90-95%
- **Speed:** 500-1000ms
- **Pros:** No training needed, very accurate
- **Cons:** Costs money, requires internet
- **Best for:** High accuracy requirements

### 3. Anthropic Claude (Paid) 💰
- **Cost:** ~$10-20/month
- **Accuracy:** 90-95%
- **Speed:** 500-1000ms
- **Pros:** No training needed, very accurate
- **Cons:** Costs money, requires internet
- **Best for:** Alternative to OpenAI

### 4. Auto Mode (Hybrid) 🔄
- **Cost:** $0-20/month (depends on API availability)
- **Accuracy:** 85-95%
- **Speed:** Variable
- **Pros:** Best of both worlds, automatic fallback
- **Cons:** Unpredictable behavior
- **Best for:** Production use with fallback

---

## 📁 File Structure

```
ml-service/
├── main.py                          # FastAPI server
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .env                            # Your configuration
├── SETUP.md                        # Detailed setup guide
└── services/
    ├── hybrid_classifier.py        # ⭐ Main classifier (supports all modes)
    ├── ai_classifier.py            # OpenAI/Claude classifier
    ├── classifier.py               # DistilBERT classifier
    ├── duplicate_detector.py       # Similarity detection
    ├── sla_predictor.py           # Resolution time prediction
    └── ai_info_extractor.py       # Information extraction
```

---

## 🚀 Quick Start

### Step 1: Install Python Dependencies

**Windows:**
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
cd ml-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env file
```

**For FREE mode (DistilBERT):**
```env
CLASSIFIER_MODE=distilbert
```

**For Paid mode (OpenAI):**
```env
CLASSIFIER_MODE=openai
OPENAI_API_KEY=sk-your-key-here
```

**For Auto mode (Hybrid):**
```env
CLASSIFIER_MODE=auto
OPENAI_API_KEY=sk-your-key-here  # Optional
```

### Step 3: Start ML Service

```bash
python main.py
```

Service runs on: http://localhost:8000

### Step 4: Test It

```bash
# Health check
curl http://localhost:8000/

# Test classification
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"My wifi is not working\"}"
```

---

## 🔧 Configuration Options

### Environment Variables

```env
# Classifier Mode
CLASSIFIER_MODE=auto              # distilbert, openai, anthropic, auto

# API Keys (only needed for API-based modes)
OPENAI_API_KEY=sk-...            # For OpenAI mode
ANTHROPIC_API_KEY=sk-ant-...     # For Anthropic mode

# Thresholds
CONFIDENCE_THRESHOLD=0.7          # Minimum confidence for auto-classification
SIMILARITY_THRESHOLD=0.85         # Duplicate detection threshold
TIME_WINDOW_HOURS=72             # Duplicate check time window

# Model Paths (optional)
MODEL_PATH=./models/classifier
SLA_MODEL_PATH=./models/sla_predictor.pkl
```

---

## 📊 API Endpoints

### 1. Health Check
```http
GET /
GET /health
```

Response:
```json
{
  "service": "DDGRS AI Service",
  "status": "running",
  "classifier": {
    "mode": "auto",
    "active_classifier": "distilbert",
    "distilbert_available": true,
    "ai_available": false,
    "cost": "FREE"
  }
}
```

### 2. Classify Grievance
```http
POST /classify
Content-Type: application/json

{
  "text": "My laptop cannot connect to college wifi",
  "threshold": 0.7
}
```

Response:
```json
{
  "department": "IT Cell",
  "confidence": 0.89,
  "all_predictions": {
    "IT Cell": 0.89,
    "Maintenance": 0.05,
    "Hostel": 0.03,
    "Academic": 0.02,
    "Infrastructure": 0.01
  },
  "classifier_used": "DistilBERT (FREE)"
}
```

### 3. Check Duplicate
```http
POST /check-duplicate
Content-Type: application/json

{
  "text": "Wifi not working in room 301",
  "recent_complaints": [
    {
      "id": "GRV-000001",
      "description": "Internet down in hostel",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "time_window_hours": 72
}
```

Response:
```json
{
  "is_duplicate": true,
  "similar_complaint": {
    "id": "GRV-000001",
    "description": "Internet down in hostel",
    "status": "In Progress"
  },
  "similarity_score": 0.92
}
```

### 4. Predict SLA
```http
POST /predict-sla
Content-Type: application/json

{
  "department": "IT Cell",
  "category": "Network",
  "description": "Wifi issue in hostel",
  "priority": "high"
}
```

Response:
```json
{
  "estimated_hours": 4.5,
  "estimated_days": 0.19,
  "confidence": 0.85
}
```

### 5. Extract Information
```http
POST /extract-info
Content-Type: application/json

{
  "text": "My room AC is broken"
}
```

Response:
```json
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

## 🔗 Bot Integration

The bot automatically uses ML service when available.

### bot-twilio-ml.js Features:

1. **Auto-Classification** - Detects category from description
2. **Confidence Display** - Shows AI confidence score
3. **Duplicate Alerts** - Warns about similar complaints
4. **SLA Estimates** - Shows expected resolution time
5. **Fallback** - Manual selection if ML fails

### User Experience:

**Without ML:**
```
Bot: Select category:
     1. Academic
     2. Hostel
     3. Faculty
     4. Infrastructure
User: 1
```

**With ML:**
```
User: My wifi is not working in hostel
Bot: 🤖 Detected Category: IT Cell
     📊 Confidence: 89%
     🔧 Classifier: DistilBERT (FREE)
     ⏱️ Estimated resolution: 1 day
     
     Type "confirm" to submit
     Type "change" to select different category
User: confirm
```

---

## 📈 Performance Metrics

### DistilBERT Mode
- Inference time: 100-200ms
- Accuracy: 85-90%
- Cost: $0
- Requires: 2GB RAM, CPU

### OpenAI Mode
- Inference time: 500-1000ms
- Accuracy: 90-95%
- Cost: $0.01 per classification
- Requires: Internet, API key

### Auto Mode
- Inference time: 100-1000ms (depends on active classifier)
- Accuracy: 85-95%
- Cost: $0-0.01 per classification
- Requires: Flexible

---

## 🐛 Troubleshooting

### Issue: ML service won't start

```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for errors
python main.py
```

### Issue: Classification returns low confidence

```bash
# Check which classifier is active
curl http://localhost:8000/

# Try different mode in .env
CLASSIFIER_MODE=openai  # More accurate
```

### Issue: Bot can't connect to ML service

```bash
# Check ML service is running
curl http://localhost:8000/

# Check bot .env has correct URL
# ML_SERVICE_URL=http://localhost:8000

# Check firewall settings
```

### Issue: OpenAI API errors

```bash
# Verify API key is valid
# Check OpenAI account has credits
# Try Anthropic as alternative:
CLASSIFIER_MODE=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🚀 Deployment

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
cd ml-service
railway init

# Add environment variables
railway variables set CLASSIFIER_MODE=auto
railway variables set OPENAI_API_KEY=sk-...

# Deploy
railway up

# Get URL
railway domain
```

### Deploy to Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Update Bot with Production URL

Edit `.env`:
```env
ML_SERVICE_URL=https://your-ml-service.railway.app
```

---

## 📊 Monitoring

### Check Service Status

```bash
curl https://your-ml-service.railway.app/health
```

### View Logs

**Railway:**
```bash
railway logs
```

**Render:**
View in dashboard

**Local:**
```bash
# Terminal running python main.py shows all logs
```

---

## 💡 Tips

1. **Start with Auto mode** - Best balance of cost and accuracy
2. **Use DistilBERT for testing** - Free and fast
3. **Switch to OpenAI for production** - Better accuracy
4. **Monitor API costs** - Set up billing alerts
5. **Cache classifications** - Reduce API calls
6. **Train DistilBERT** - Improve free accuracy

---

## 📚 Additional Resources

- [ML_INTEGRATION_GUIDE.md](ML_INTEGRATION_GUIDE.md) - Integration guide
- [START_ML_SYSTEM.md](START_ML_SYSTEM.md) - Startup instructions
- [ml-service/SETUP.md](ml-service/SETUP.md) - Detailed setup
- [AI_SERVICE_SUMMARY.md](AI_SERVICE_SUMMARY.md) - Feature overview

---

## 🎯 Next Steps

1. ✅ Set up ML service locally
2. ✅ Test classification
3. ✅ Integrate with bot
4. ⏳ Deploy to cloud
5. ⏳ Monitor performance
6. ⏳ Optimize accuracy

---

## 🤝 Support

For issues:
1. Check logs in terminal
2. Test endpoints with curl
3. Verify environment variables
4. Check API key validity
