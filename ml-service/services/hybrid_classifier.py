"""
Hybrid Classifier - Supports both API-based and DistilBERT
Choose based on your needs: Free (DistilBERT) or Powerful (GPT-4/Claude)
"""

import os
from typing import Dict
from .ai_classifier import AIClassifier
from .classifier import GrievanceClassifier


class HybridClassifier:
    """
    Intelligent classifier that can use:
    1. DistilBERT (FREE, local, fast)
    2. OpenAI GPT-4 (Paid, powerful, accurate)
    3. Anthropic Claude (Paid, powerful, accurate)
    """
    
    def __init__(self, mode: str = "auto"):
        """
        Initialize hybrid classifier
        
        Args:
            mode: "distilbert", "openai", "anthropic", or "auto"
                  "auto" tries API first, falls back to DistilBERT
        """
        self.mode = mode
        self.distilbert = None
        self.ai_classifier = None
        
        # Initialize based on mode
        if mode in ["distilbert", "auto"]:
            try:
                self.distilbert = GrievanceClassifier()
                print("✅ DistilBERT classifier loaded (FREE)")
            except Exception as e:
                print(f"⚠️ DistilBERT failed: {e}")
        
        if mode in ["openai", "anthropic", "auto"]:
            try:
                provider = mode if mode in ["openai", "anthropic"] else os.getenv("AI_PROVIDER", "openai")
                self.ai_classifier = AIClassifier(provider=provider)
                print(f"✅ AI classifier loaded ({provider})")
            except Exception as e:
                print(f"⚠️ AI classifier failed: {e}")
        
        # Determine active classifier
        if mode == "auto":
            if self.ai_classifier and self.ai_classifier.is_loaded():
                self.active = "ai"
                print("🎯 Using AI classifier (API-based)")
            elif self.distilbert and self.distilbert.is_loaded():
                self.active = "distilbert"
                print("🎯 Using DistilBERT (FREE)")
            else:
                self.active = "fallback"
                print("⚠️ Using fallback (keyword-based)")
        else:
            self.active = mode
    
    
    def is_loaded(self) -> bool:
        """Check if any classifier is loaded"""
        if self.active == "ai":
            return self.ai_classifier and self.ai_classifier.is_loaded()
        elif self.active == "distilbert":
            return self.distilbert and self.distilbert.is_loaded()
        return True  # Fallback always available
    
    
    def predict(self, text: str, threshold: float = 0.7) -> Dict:
        """
        Classify grievance using active classifier
        """
        try:
            if self.active == "ai" and self.ai_classifier:
                result = self.ai_classifier.predict(text, threshold)
                result["classifier_used"] = "AI (GPT-4/Claude)"
                return result
                
            elif self.active == "distilbert" and self.distilbert:
                result = self.distilbert.predict(text, threshold)
                result["classifier_used"] = "DistilBERT (FREE)"
                return result
                
            else:
                # Fallback to keyword-based
                result = self._fallback_classification(text, threshold)
                result["classifier_used"] = "Keyword-based (Fallback)"
                return result
                
        except Exception as e:
            print(f"⚠️ Classification error: {e}")
            result = self._fallback_classification(text, threshold)
            result["classifier_used"] = "Keyword-based (Error Fallback)"
            return result
    
    
    def _fallback_classification(self, text: str, threshold: float) -> Dict:
        """Simple keyword-based classification"""
        text_lower = text.lower()
        
        keywords = {
            "IT / Network": ["wifi", "internet", "computer", "software", "portal", "network", "it"],
            "Infrastructure": ["repair", "broken", "fix", "damaged", "ac", "fan", "light", "maintenance"],
            "Hostel": ["room", "hostel", "mess", "food", "warden", "bed"],
            "Academic": ["exam", "marks", "teacher", "class", "assignment", "grade"],
            "Examination": ["exam", "test", "result", "marks", "evaluation"],
            "Administration": ["certificate", "document", "admission", "id card", "fee", "payment"],
            "Library": ["book", "library", "issue", "return", "fine"],
            "Discipline / Harassment": ["harassment", "bullying", "ragging", "abuse"],
            "Other": []
        }
        
        scores = {}
        for dept, dept_keywords in keywords.items():
            if dept == "Other":
                scores[dept] = 0.0
                continue
            matches = sum(1 for kw in dept_keywords if kw in text_lower)
            if matches > 0:
                if matches == 1:
                    scores[dept] = 0.75
                elif matches == 2:
                    scores[dept] = 0.85
                else:
                    scores[dept] = min(0.75 + (matches * 0.1), 0.95)
            else:
                scores[dept] = 0.0
        
        best_dept = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else "Other"
        confidence = scores.get(best_dept, 0.65)
        
        if confidence == 0:
            best_dept = "Other"
            confidence = 0.65
        
        # Lower threshold for fallback
        effective_threshold = max(threshold - 0.1, 0.6)
        if confidence < effective_threshold:
            best_dept = "Other"
            confidence = 0.65
        
        return {
            "department": best_dept,
            "confidence": float(confidence),
            "all_predictions": {d: float(s) for d, s in scores.items()}
        }
    
    
    def get_info(self) -> Dict:
        """Get information about active classifier"""
        return {
            "mode": self.mode,
            "active_classifier": self.active,
            "distilbert_available": self.distilbert is not None and self.distilbert.is_loaded(),
            "ai_available": self.ai_classifier is not None and self.ai_classifier.is_loaded(),
            "cost": "FREE" if self.active == "distilbert" else "Paid API" if self.active == "ai" else "FREE"
        }
