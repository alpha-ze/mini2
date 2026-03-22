"""
Duplicate Complaint Detection using Sentence Embeddings
Identifies similar complaints to avoid redundant processing
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta


class DuplicateDetector:
    """
    Detects duplicate complaints using semantic similarity
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize with sentence transformer model
        
        Args:
            model_name: HuggingFace model for embeddings
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.model_loaded = True
            print(f"✅ Duplicate detector initialized with {model_name}")
        except Exception as e:
            print(f"⚠️ Duplicate detector initialization failed: {e}")
            self.model_loaded = False
    
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model_loaded
    
    
    def check_duplicate(
        self,
        text: str,
        recent_complaints: List[Dict],
        time_window_hours: int = 72,
        similarity_threshold: float = 0.85
    ) -> Dict:
        """
        Check if complaint is duplicate of recent complaints
        
        Args:
            text: New complaint text
            recent_complaints: List of recent complaints with 'description' and 'created_at'
            time_window_hours: Time window to check for duplicates
            similarity_threshold: Minimum similarity score to consider duplicate
            
        Returns:
            Dict with is_duplicate, similar_complaint, similarity_score
        """
        
        try:
            if not self.model_loaded or not recent_complaints:
                return {
                    "is_duplicate": False,
                    "similar_complaint": None,
                    "similarity_score": 0.0
                }
            
            # Filter complaints within time window
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            filtered_complaints = []
            for c in recent_complaints:
                try:
                    created_at = self._parse_datetime(c.get('created_at', ''))
                    if created_at > cutoff_time:
                        filtered_complaints.append(c)
                except Exception as e:
                    print(f"⚠️ Error parsing datetime for complaint: {e}")
                    # Include complaint anyway if datetime parsing fails
                    filtered_complaints.append(c)
            
            if not filtered_complaints:
                return {
                    "is_duplicate": False,
                    "similar_complaint": None,
                    "similarity_score": 0.0
                }
            
            # Generate embeddings
            new_embedding = self.model.encode([text])[0]
            complaint_texts = [c.get('description', '') for c in filtered_complaints]
            
            # Skip empty descriptions
            valid_complaints = [(i, c) for i, c in enumerate(filtered_complaints) if complaint_texts[i].strip()]
            if not valid_complaints:
                return {
                    "is_duplicate": False,
                    "similar_complaint": None,
                    "similarity_score": 0.0
                }
            
            valid_texts = [complaint_texts[i] for i, _ in valid_complaints]
            complaint_embeddings = self.model.encode(valid_texts)
            
            # Calculate similarities
            similarities = cosine_similarity([new_embedding], complaint_embeddings)[0]
            
            # Find most similar
            max_similarity_idx = np.argmax(similarities)
            max_similarity = float(similarities[max_similarity_idx])
            
            # Get the actual complaint from valid_complaints
            actual_complaint = valid_complaints[max_similarity_idx][1]
            
            # Check if duplicate
            is_duplicate = max_similarity >= similarity_threshold
            
            return {
                "is_duplicate": is_duplicate,
                "similar_complaint": actual_complaint if is_duplicate else None,
                "similarity_score": max_similarity
            }
        except Exception as e:
            print(f"❌ Error in check_duplicate: {e}")
            # Return safe default on error
            return {
                "is_duplicate": False,
                "similar_complaint": None,
                "similarity_score": 0.0
            }
    
    
    def _parse_datetime(self, date_str: str) -> datetime:
        """Parse datetime string with multiple format support"""
        if not date_str:
            return datetime.min
        
        try:
            # Try ISO format with Z
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            pass
        
        try:
            # Try standard ISO format
            return datetime.fromisoformat(date_str)
        except:
            pass
        
        try:
            # Try parsing as timestamp
            from dateutil import parser
            return parser.parse(date_str)
        except:
            pass
        
        # Return min datetime if all parsing fails
        return datetime.min
