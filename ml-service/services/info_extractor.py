"""
Information Extraction Service
Identifies missing fields and generates follow-up questions
"""

import re
from typing import Dict, List


class InformationExtractor:
    """
    Extracts information from complaint text and identifies gaps
    """
    
    REQUIRED_FIELDS = [
        "location",
        "urgency",
        "category",
        "description"
    ]
    
    def __init__(self):
        self.model_loaded = True
        print("✅ Information extractor initialized")
    
    def is_loaded(self) -> bool:
        return self.model_loaded
    
    def extract(self, text: str) -> Dict:
        """
        Extract information and identify missing fields
        """
        extracted = {}
        missing = []
        
        # Extract location
        location_patterns = [
            r'(?:in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'room\s+(\d+)',
            r'block\s+([A-Z])',
            r'floor\s+(\d+)'
        ]
        
        location_found = False
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted['location'] = match.group(1)
                location_found = True
                break
        
        if not location_found:
            missing.append('location')
        
        # Extract urgency
        urgency_keywords = {
            'urgent': ['urgent', 'emergency', 'immediately', 'asap'],
            'high': ['important', 'critical', 'serious'],
            'medium': ['soon', 'needed'],
            'low': ['whenever', 'eventually']
        }
        
        urgency_found = False
        for level, keywords in urgency_keywords.items():
            if any(kw in text.lower() for kw in keywords):
                extracted['urgency'] = level
                urgency_found = True
                break
        
        if not urgency_found:
            missing.append('urgency')
        
        # Check description length
        if len(text.split()) < 5:
            missing.append('description')
        else:
            extracted['description'] = text
        
        # Generate follow-up questions
        questions = self._generate_questions(missing)
        
        return {
            "missing_fields": missing,
            "extracted_info": extracted,
            "follow_up_questions": questions
        }
    
    def _generate_questions(self, missing_fields: List[str]) -> List[str]:
        """Generate follow-up questions for missing fields"""
        question_map = {
            "location": "Where exactly is this issue located? (e.g., Room 301, Block A)",
            "urgency": "How urgent is this issue? (urgent/high/medium/low)",
            "category": "Which category does this belong to?",
            "description": "Could you provide more details about the issue?"
        }
        
        return [question_map[field] for field in missing_fields if field in question_map]
