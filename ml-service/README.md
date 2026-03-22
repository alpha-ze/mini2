# DDGRS ML Service

AI-powered backend for intelligent grievance classification and analysis.

## Features

1. **DistilBERT Classification** - Automatic department routing
2. **Duplicate Detection** - Semantic similarity using sentence embeddings
3. **SLA Prediction** - Resolution time estimation
4. **Information Extraction** - Smart field completion

## Quick Start

### 1. Install Dependencies

```bash
cd ml-service
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run Service

```bash
python main.py
```

Service will start on `http://localhost:8000`

### 3. Test API

```bash
# Health check
curl http://localhost:8000/health

# Classify grievance
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "WiFi not working in hostel room 301"}'
```

## API Endpoints

### POST /classify
Classify grievance into department

**Request:**
```json
{
  "text": "WiFi not working in hostel",
  "threshold": 0.7
}
```

**Response:**
```json
{
  "department": "IT Cell",
  "confidence": 0.92,
  "all_predictions": {
    "IT Cell": 0.92,
    "Maintenance": 0.05,
    ...
  }
}
```

### POST /check-duplicate
Check for duplicate complaints

**Request:**
```json
{
  "text": "AC not working in room 301",
  "recent_complaints": [...],
  "time_window_hours": 72
}
```

**Response:**
```json
{
  "is_duplicate": true,
  "similar_complaint": {...},
  "similarity_score": 0.89
}
```

### POST /predict-sla
Predict resolution time

**Request:**
```json
{
  "department": "IT Cell",
  "category": "Network",
  "description": "WiFi issue",
  "priority": "high"
}
```

**Response:**
```json
{
  "estimated_hours": 16.8,
  "estimated_days": 0.7,
  "confidence": 0.75
}
```

### POST /extract-info
Extract information and identify gaps

**Request:**
```json
{
  "text": "AC not working"
}
```

**Response:**
```json
{
  "missing_fields": ["location", "urgency"],
  "extracted_info": {"description": "AC not working"},
  "follow_up_questions": [
    "Where exactly is this issue located?",
    "How urgent is this issue?"
  ]
}
```

## Model Training

### Train Classification Model

```python
from services.classifier import train_classifier

train_classifier(
    training_data_path='data/training_data.csv',
    output_path='models/classifier'
)
```

**Training data format (CSV):**
```csv
text,department
"WiFi not working in lab","IT Cell"
"Broken chair in classroom","Maintenance"
...
```

## Deployment

### Docker

```bash
docker build -t ddgrs-ml-service .
docker run -p 8000:8000 ddgrs-ml-service
```

### Railway/Render

1. Push to GitHub
2. Connect repository
3. Set environment variables
4. Deploy

## Environment Variables

```env
MODEL_PATH=./models/classifier
SIMILARITY_THRESHOLD=0.85
SLA_MODEL_PATH=./models/sla_predictor.pkl
```

## Performance

- Classification: <500ms
- Duplicate Detection: <300ms
- SLA Prediction: <100ms
- Info Extraction: <50ms

## Next Steps

1. Collect training data from real complaints
2. Fine-tune DistilBERT model
3. Train SLA prediction model
4. Deploy to production
5. Monitor and improve
