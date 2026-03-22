"""
API-Based Grievance Classification using OpenAI/Anthropic
No training required - uses powerful LLM APIs
"""

import os
from typing import Dict, Optional
import json
from openai import OpenAI
from anthropic import Anthropic


class AIClassifier:
    """
    Classifies grievances using LLM APIs (OpenAI GPT-4 or Anthropic Claude)
    """
    
    DEPARTMENTS = [
        "IT Cell",
        "Maintenance", 
        "Hostel",
        "Transport",
        "Academics",
        "Accounts",
        "Library",
        "Administration"
    ]
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize AI classifier
        
        Args:
            provider: "openai" or "anthropic"
        """
        self.provider = provider
        self.model_loaded = False
        
        try:
            if provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment")
                self.client = OpenAI(api_key=api_key)
                self.model = "gpt-4-turbo-preview"
                
            elif provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found in environment")
                self.client = Anthropic(api_key=api_key)
                self.model = "claude-3-sonnet-20240229"
            
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            self.model_loaded = True
            print(f"✅ AI Classifier initialized with {provider} ({self.model})")
            
        except Exception as e:
            print(f"⚠️ AI Classifier initialization failed: {e}")
            self.model_loaded = False
    
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model_loaded
    
    
    def predict(self, text: str, threshold: float = 0.7) -> Dict:
        """
        Classify grievance using AI API
        
        Args:
            text: Grievance description
            threshold: Confidence threshold
            
        Returns:
            Dict with department, confidence, and all predictions
        """
        
        if not self.model_loaded:
            return self._fallback_classification(text)
        
        try:
            if self.provider == "openai":
                return self._classify_with_openai(text, threshold)
            else:
                return self._classify_with_anthropic(text, threshold)
                
        except Exception as e:
            print(f"⚠️ AI classification failed: {e}")
            return self._fallback_classification(text)
    
    
    def _classify_with_openai(self, text: str, threshold: float) -> Dict:
        """Classify using OpenAI GPT-4"""
        
        system_prompt = f"""You are an expert grievance classifier for an institution.
Classify the following complaint into ONE of these departments:
{', '.join(self.DEPARTMENTS)}

Respond ONLY with a JSON object in this exact format:
{{
    "department": "Department Name",
    "confidence": 0.95,
    "reasoning": "Brief explanation",
    "all_predictions": {{
        "IT Cell": 0.95,
        "Maintenance": 0.03,
        "Hostel": 0.01,
        "Transport": 0.00,
        "Academics": 0.00,
        "Accounts": 0.00,
        "Library": 0.00,
        "Administration": 0.01
    }}
}}

Rules:
- Confidence must be between 0 and 1
- All predictions must sum to approximately 1.0
- Choose the most appropriate department based on the complaint content"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Complaint: {text}"}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Validate and format response
        department = result.get("department", "Administration")
        confidence = float(result.get("confidence", 0.5))
        all_predictions = result.get("all_predictions", {})
        
        # Check threshold
        if confidence < threshold:
            department = "Manual Review Required"
        
        return {
            "department": department,
            "confidence": confidence,
            "all_predictions": all_predictions,
            "reasoning": result.get("reasoning", "")
        }
    
    
    def _classify_with_anthropic(self, text: str, threshold: float) -> Dict:
        """Classify using Anthropic Claude"""
        
        prompt = f"""Classify this institutional complaint into ONE department.

Departments: {', '.join(self.DEPARTMENTS)}

Complaint: {text}

Respond with JSON only:
{{
    "department": "Department Name",
    "confidence": 0.95,
    "reasoning": "Brief explanation",
    "all_predictions": {{
        "IT Cell": 0.95,
        "Maintenance": 0.03,
        ...
    }}
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result = json.loads(response.content[0].text)
        
        department = result.get("department", "Administration")
        confidence = float(result.get("confidence", 0.5))
        
        if confidence < threshold:
            department = "Manual Review Required"
        
        return {
            "department": department,
            "confidence": confidence,
            "all_predictions": result.get("all_predictions", {}),
            "reasoning": result.get("reasoning", "")
        }
    
    
    def _fallback_classification(self, text: str) -> Dict:
        """Simple keyword-based fallback"""
        text_lower = text.lower()
        
        keywords = {
            "IT Cell": ["wifi", "internet", "computer", "software", "portal"],
            "Maintenance": ["repair", "broken", "fix", "damaged", "ac"],
            "Hostel": ["room", "hostel", "mess", "food", "warden"],
            "Transport": ["bus", "transport", "vehicle", "driver"],
            "Academics": ["exam", "marks", "teacher", "class", "assignment"],
            "Accounts": ["fee", "payment", "refund", "scholarship"],
            "Library": ["book", "library", "issue", "return"],
            "Administration": ["certificate", "document", "admission"]
        }
        
        scores = {}
        for dept, dept_keywords in keywords.items():
            score = sum(1 for kw in dept_keywords if kw in text_lower)
            scores[dept] = score / len(dept_keywords) if dept_keywords else 0
        
        best_dept = max(scores, key=scores.get) if scores else "Administration"
        confidence = min(scores[best_dept] * 3, 0.7)
        
        return {
            "department": best_dept,
            "confidence": float(confidence),
            "all_predictions": {d: float(s) for d, s in scores.items()},
            "reasoning": "Fallback keyword matching"
        }
