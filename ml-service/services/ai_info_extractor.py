"""
AI-Powered Information Extraction
Uses LLM to extract structured data and identify missing fields
"""

import os
import json
from typing import Dict, List
from openai import OpenAI
from anthropic import Anthropic


class AIInformationExtractor:
    """
    Extracts information and generates follow-up questions using AI
    """
    
    def __init__(self, provider: str = "openai"):
        """Initialize AI extractor"""
        self.provider = provider
        self.model_loaded = False
        
        try:
            if provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not found")
                self.client = OpenAI(api_key=api_key)
                self.model = "gpt-4-turbo-preview"
                
            elif provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found")
                self.client = Anthropic(api_key=api_key)
                self.model = "claude-3-sonnet-20240229"
            
            self.model_loaded = True
            print(f"✅ AI Info Extractor initialized with {provider}")
            
        except Exception as e:
            print(f"⚠️ AI Info Extractor failed: {e}")
            self.model_loaded = False
    
    
    def is_loaded(self) -> bool:
        return self.model_loaded
    
    
    def extract(self, text: str) -> Dict:
        """
        Extract information and identify missing fields
        """
        
        if not self.model_loaded:
            return self._basic_extraction(text)
        
        try:
            if self.provider == "openai":
                return self._extract_with_openai(text)
            else:
                return self._extract_with_anthropic(text)
                
        except Exception as e:
            print(f"⚠️ AI extraction failed: {e}")
            return self._basic_extraction(text)
    
    
    def _extract_with_openai(self, text: str) -> Dict:
        """Extract using OpenAI"""
        
        system_prompt = """You are an expert at extracting structured information from complaints.

Analyze the complaint and extract:
1. Location (room number, building, area)
2. Urgency level (urgent/high/medium/low)
3. Category/Type of issue
4. Specific details

Identify what information is MISSING that would help resolve the complaint.

Respond with JSON only:
{
    "extracted_info": {
        "location": "Room 301, Block A",
        "urgency": "high",
        "category": "Maintenance",
        "details": "AC not cooling properly"
    },
    "missing_fields": ["contact_person", "time_of_occurrence"],
    "follow_up_questions": [
        "When did you first notice this issue?",
        "Have you reported this before?"
    ],
    "completeness_score": 0.7
}"""

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
        
        return {
            "missing_fields": result.get("missing_fields", []),
            "extracted_info": result.get("extracted_info", {}),
            "follow_up_questions": result.get("follow_up_questions", []),
            "completeness_score": result.get("completeness_score", 0.5)
        }
    
    
    def _extract_with_anthropic(self, text: str) -> Dict:
        """Extract using Anthropic"""
        
        prompt = f"""Analyze this complaint and extract structured information.

Complaint: {text}

Extract: location, urgency, category, details
Identify: missing information
Generate: follow-up questions

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text)
        
        return {
            "missing_fields": result.get("missing_fields", []),
            "extracted_info": result.get("extracted_info", {}),
            "follow_up_questions": result.get("follow_up_questions", [])
        }
    
    
    def _basic_extraction(self, text: str) -> Dict:
        """Basic fallback extraction"""
        import re
        
        extracted = {}
        missing = []
        
        # Try to extract location
        location_match = re.search(r'room\s+(\d+)|block\s+([A-Z])', text, re.IGNORECASE)
        if location_match:
            extracted['location'] = location_match.group(0)
        else:
            missing.append('location')
        
        # Check urgency keywords
        if any(word in text.lower() for word in ['urgent', 'emergency', 'immediately']):
            extracted['urgency'] = 'high'
        else:
            missing.append('urgency')
        
        questions = []
        if 'location' in missing:
            questions.append("Where exactly is this issue located?")
        if 'urgency' in missing:
            questions.append("How urgent is this issue?")
        
        return {
            "missing_fields": missing,
            "extracted_info": extracted,
            "follow_up_questions": questions
        }
