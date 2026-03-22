# 🚀 START HERE - Quick Launch Guide

## Your System is Ready!

Everything is configured with your HuggingFace token. Follow these steps to start:

---

## Step 1: Install ML Dependencies (One-Time Setup)

Open PowerShell/Terminal and run:

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** This will take 5-10 minutes (downloading ~500MB of packages including PyTorch).

---

## Step 2: Start ML Service

After installation completes:

```bash
# Make sure you're still in ml-service folder with venv activated
python main.py
```

You should see:
```
✅ Classifier initialized on cpu
✅ DistilBERT classifier loaded (FREE)
🎯 Using DistilBERT (FREE)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal open!**

---

## Step 3: Start WhatsApp Bot

Open a NEW terminal:

```bash
node bot-twilio-ml.js
```

You should see:
```
🤖 AI-Powered WhatsApp Bot running on port 3001
🧠 ML Service: http://localhost:8000
🎯 Auto-Classification: Enabled
```

**Leave this terminal open!**

---

## Step 4: Start Admin Dashboard

Open a NEW terminal:

```bash
cd admin-panel
npm run dev
```

Opens at: http://localhost:5173

**Leave this terminal open!**

---

## Step 5: Start ngrok

Open a NEW terminal:

```bash
ngrok http 3001
```

Copy the HTTPS URL and configure in Twilio Console.

---

## Test It!

Send WhatsApp message: **"start"**

Bot will:
1. Ask for anonymous option
2. Ask for grievance description
3. **Auto-classify using AI** 🤖
4. Show confidence score
5. Let you confirm or change

---

## What's Running

- ✅ ML Service (Port 8000) - FREE DistilBERT classifier
- ✅ WhatsApp Bot (Port 3001) - With ML integration
- ✅ Admin Dashboard (Port 5173) - React UI
- ✅ ngrok - Webhook tunnel

---

## Cost: $0/month

Using FREE DistilBERT classifier with your HuggingFace token!

---

## Need Help?

Check the documentation:
- [READY_TO_START.md](READY_TO_START.md) - Detailed instructions
- [ML_README.md](ML_README.md) - ML service guide
- [HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md) - Your token info

---

**Your HuggingFace token is already configured in `ml-service/.env`**

Enjoy your AI-powered grievance system! 🎉
