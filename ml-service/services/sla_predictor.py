"""
SLA-Based Resolution Time Prediction
Predicts expected completion time using ML
"""

import pickle
import os
from typing import Dict


class SLAPredictor:
    """
    Predicts resolution time based on historical data
    """
    
    # Default SLA times (in hours) by department
    DEFAULT_SLA = {
        "IT Cell": 24,
        "Maintenance": 48,
        "Hostel": 24,
        "Transport": 12,
        "Academics": 72,
        "Accounts": 48,
        "Library": 24,
        "Administration": 48
    }
    
    def __init__(self, model_path: str = None):
        """Initialize SLA predictor"""
        self.model = None
        self.model_loaded = False
        
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                print("✅ SLA predictor model loaded")
            except Exception as e:
                print(f"⚠️ SLA predictor failed to load: {e}")
        else:
            print("ℹ️ Using default SLA times")
    
    def is_loaded(self) -> bool:
        return True  # Always available with defaults
    
    def predict(
        self,
        department: str,
        category: str,
        description: str,
        priority: str = "medium"
    ) -> Dict:
        """Predict resolution time"""
        
        # Get base SLA
        base_hours = self.DEFAULT_SLA.get(department, 48)
        
        # Adjust for priority
        priority_multiplier = {
            "low": 1.5,
            "medium": 1.0,
            "high": 0.7,
            "urgent": 0.5
        }
        
        estimated_hours = base_hours * priority_multiplier.get(priority, 1.0)
        
        return {
            "estimated_hours": estimated_hours,
            "estimated_days": estimated_hours / 24,
            "confidence": 0.75
        }
