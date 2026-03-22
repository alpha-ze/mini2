"""
DistilBERT-based Grievance Classification Service
Automatically routes complaints to correct department
"""

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from typing import Dict
import os


class GrievanceClassifier:
    """
    Classifies grievances into departments using DistilBERT
    """
    
    DEPARTMENTS = [
        "Academic",
        "Examination",
        "Infrastructure",
        "Hostel",
        "Library",
        "Administration",
        "IT / Network",
        "Discipline / Harassment",
        "Other"
    ]
    
    def __init__(self, model_path: str = None):
        """
        Initialize classifier with pre-trained or fine-tuned model
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_loaded = False
        
        try:
            # Get HuggingFace token from environment
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            
            if model_path and os.path.exists(model_path):
                # Load fine-tuned model
                self.tokenizer = DistilBertTokenizer.from_pretrained(
                    model_path,
                    token=hf_token
                )
                self.model = DistilBertForSequenceClassification.from_pretrained(
                    model_path,
                    token=hf_token
                )
            else:
                # Use base model with rule-based classification for now
                self.tokenizer = DistilBertTokenizer.from_pretrained(
                    'distilbert-base-uncased',
                    token=hf_token
                )
                self.model = None  # Will use rule-based until trained
                
            if self.model:
                self.model.to(self.device)
                self.model.eval()
                
            self.model_loaded = True
            print(f"✅ Classifier initialized on {self.device}")
            
        except Exception as e:
            print(f"⚠️ Classifier initialization failed: {e}")
            self.model_loaded = False
    
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model_loaded
    
    
    def predict(self, text: str, threshold: float = 0.7) -> Dict:
        """
        Predict department for given grievance text
        
        Args:
            text: Grievance description
            threshold: Confidence threshold for prediction
            
        Returns:
            Dict with department, confidence, and all predictions
        """
        
        if self.model:
            # Use ML model
            return self._predict_with_model(text, threshold)
        else:
            # Use rule-based classification
            return self._predict_with_rules(text, threshold)
    
    
    def _predict_with_model(self, text: str, threshold: float) -> Dict:
        """
        Predict using fine-tuned DistilBERT model
        """
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)[0]
        
        # Get top prediction
        confidence, predicted_idx = torch.max(probabilities, dim=0)
        confidence = confidence.item()
        predicted_dept = self.DEPARTMENTS[predicted_idx.item()]
        
        # Get all predictions
        all_predictions = {
            dept: prob.item() 
            for dept, prob in zip(self.DEPARTMENTS, probabilities)
        }
        
        # Check threshold
        if confidence < threshold:
            predicted_dept = "Manual Review Required"
        
        return {
            "department": predicted_dept,
            "confidence": confidence,
            "all_predictions": all_predictions
        }
    
    
    def _predict_with_rules(self, text: str, threshold: float) -> Dict:
        """
        Rule-based classification (fallback until model is trained)
        Uses keyword matching for department routing
        """
        text_lower = text.lower()
        
        # Department keywords with weights - MUST match database categories
        keywords = {
            "IT / Network": [
                "wifi", "internet", "network", "computer", "laptop", "software",
                "website", "portal", "login", "password", "email", "server",
                "printer", "projector", "lab", "system", "app", "application",
                "connection", "online", "offline", "tech", "digital", "it"
            ],
            "Infrastructure": [
                "repair", "broken", "fix", "damaged", "leaking", "crack",
                "paint", "door", "window", "ceiling", "floor", "wall",
                "furniture", "chair", "table", "bench", "fan", "light", "bulb",
                "plumbing", "electrical", "carpentry", "maintenance", "building",
                "classroom", "ac", "air conditioning"
            ],
            "Hostel": [
                "room", "hostel", "mess", "food", "warden", "roommate",
                "bed", "mattress", "bathroom", "toilet", "shower", "water",
                "electricity", "cooler", "laundry", "washing",
                "dining", "canteen", "kitchen", "meal", "breakfast", "lunch", "dinner",
                "taste", "quality", "hygiene", "clean", "accommodation"
            ],
            "Academic": [
                "exam", "test", "marks", "grade", "result", "syllabus",
                "lecture", "class", "teacher", "professor", "assignment",
                "project", "attendance", "timetable", "course", "subject",
                "study", "learning", "faculty", "teaching", "curriculum"
            ],
            "Examination": [
                "exam", "examination", "test", "quiz", "marks", "grade",
                "result", "answer sheet", "evaluation", "revaluation",
                "hall ticket", "admit card", "exam schedule"
            ],
            "Library": [
                "book", "library", "issue", "return", "fine", "reading",
                "journal", "reference", "librarian", "card", "borrow",
                "periodical", "magazine", "digital library"
            ],
            "Administration": [
                "certificate", "document", "admission", "registration",
                "id card", "bonafide", "noc", "office", "staff", "admin",
                "fee", "payment", "refund", "scholarship", "receipt",
                "invoice", "bill", "charge", "money", "financial", "bank",
                "tuition", "dues"
            ],
            "Discipline / Harassment": [
                "harassment", "bullying", "ragging", "abuse", "misconduct",
                "discipline", "behavior", "complaint", "safety", "security",
                "threat", "violence"
            ],
            "Other": []  # Catch-all
        }
        
        # Calculate scores for each department
        scores = {}
        match_counts = {}
        
        for dept, dept_keywords in keywords.items():
            if dept == "Other":
                scores[dept] = 0.0
                continue
                
            matches = sum(1 for keyword in dept_keywords if keyword in text_lower)
            match_counts[dept] = matches
            
            # Score based on matches with better scaling
            if matches > 0:
                # Give higher weight to multiple matches
                if matches == 1:
                    scores[dept] = 0.75
                elif matches == 2:
                    scores[dept] = 0.85
                else:
                    scores[dept] = min(0.75 + (matches * 0.1), 0.95)
            else:
                scores[dept] = 0.0
        
        # Get best match
        if scores and max(scores.values()) > 0:
            best_dept = max(scores, key=scores.get)
            confidence = scores[best_dept]
        else:
            # No keywords matched - default to Other with medium confidence
            best_dept = "Other"
            confidence = 0.65
            scores["Other"] = 0.65
        
        # Lower threshold for rule-based to make it more useful
        effective_threshold = max(threshold - 0.1, 0.6)  # Reduce threshold by 10%
        
        if confidence < effective_threshold:
            best_dept = "Other"  # Use "Other" instead of "Manual Review Required"
            confidence = 0.65
        
        return {
            "department": best_dept,
            "confidence": float(confidence),
            "all_predictions": {dept: float(score) for dept, score in scores.items()}
        }


# Training function (to be used separately)
def train_classifier(training_data_path: str, output_path: str):
    """
    Fine-tune DistilBERT on grievance classification task
    
    Args:
        training_data_path: Path to CSV with columns: text, department
        output_path: Where to save fine-tuned model
    """
    import pandas as pd
    from transformers import Trainer, TrainingArguments
    from sklearn.model_selection import train_test_split
    from torch.utils.data import Dataset
    
    # Load data
    df = pd.read_csv(training_data_path)
    
    # Create label mapping
    label2id = {dept: idx for idx, dept in enumerate(GrievanceClassifier.DEPARTMENTS)}
    id2label = {idx: dept for dept, idx in label2id.items()}
    
    # Prepare dataset
    class GrievanceDataset(Dataset):
        def __init__(self, texts, labels, tokenizer):
            self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
            self.labels = labels
        
        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item
        
        def __len__(self):
            return len(self.labels)
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['text'].tolist(),
        [label2id[dept] for dept in df['department']],
        test_size=0.2,
        random_state=42
    )
    
    # Initialize tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=len(GrievanceClassifier.DEPARTMENTS),
        id2label=id2label,
        label2id=label2id
    )
    
    # Create datasets
    train_dataset = GrievanceDataset(train_texts, train_labels, tokenizer)
    val_dataset = GrievanceDataset(val_texts, val_labels, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_path,
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{output_path}/logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )
    
    # Train
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    trainer.train()
    
    # Save model
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    
    print(f"✅ Model trained and saved to {output_path}")
