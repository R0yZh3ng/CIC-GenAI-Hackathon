from typing import Dict, Any, List, Optional
from config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ScoringEngine:
    def __init__(self):
        self.technical_weights = {
            "accuracy": settings.TECHNICAL_ACCURACY_WEIGHT,
            "time": settings.TECHNICAL_TIME_WEIGHT,
            "optimality": settings.TECHNICAL_OPTIMALITY_WEIGHT,
            "process": settings.TECHNICAL_PROCESS_WEIGHT
        }
        
        self.behavioral_weights = {
            "chatgpt": settings.BEHAVIORAL_CHATGPT_WEIGHT,
            "tone": settings.BEHAVIORAL_TONE_WEIGHT
        }
    
    def calculate_technical_score(self, evaluation: Dict[str, Any], time_taken: float) -> Dict[str, Any]:
        """
        Calculate technical score based on evaluation and time taken
        """
        try:
            # Extract scores from evaluation
            correctness_score = evaluation.get("correctness_score", 0)
            optimality_score = evaluation.get("optimality_score", 0)
            process_score = evaluation.get("process_score", 0)
            
            # Calculate time score (inverse relationship - faster is better)
            time_score = self._calculate_time_score(time_taken)
            
            # Apply weights
            weighted_scores = {
                "accuracy": correctness_score * self.technical_weights["accuracy"],
                "time": time_score * self.technical_weights["time"],
                "optimality": optimality_score * self.technical_weights["optimality"],
                "process": process_score * self.technical_weights["process"]
            }
            
            # Calculate total score
            total_score = sum(weighted_scores.values())
            
            return {
                "total_score": round(total_score, 2),
                "score_breakdown": weighted_scores,
                "raw_scores": {
                    "correctness": correctness_score,
                    "time": time_score,
                    "optimality": optimality_score,
                    "process": process_score
                },
                "weights": self.technical_weights,
                "feedback": evaluation.get("feedback", ""),
                "time_taken": time_taken
            }
            
        except Exception as e:
            logger.error(f"Error calculating technical score: {e}")
            return {
                "total_score": 0,
                "score_breakdown": {},
                "raw_scores": {},
                "weights": self.technical_weights,
                "feedback": "Error in scoring calculation",
                "time_taken": time_taken
            }
    
    def calculate_behavioral_score(self, chatgpt_evaluation: Dict[str, Any], tone_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate behavioral score based on ChatGPT evaluation and tone analysis
        """
        try:
            # Extract ChatGPT score
            chatgpt_score = chatgpt_evaluation.get("score", 0)
            
            # Calculate tone score from audio analysis
            tone_score = self._calculate_tone_score_from_analysis(tone_analysis)
            
            # Apply weights
            weighted_scores = {
                "chatgpt": chatgpt_score * self.behavioral_weights["chatgpt"],
                "tone": tone_score * self.behavioral_weights["tone"]
            }
            
            # Calculate total score
            total_score = sum(weighted_scores.values())
            
            return {
                "total_score": round(total_score, 2),
                "score_breakdown": weighted_scores,
                "raw_scores": {
                    "chatgpt": chatgpt_score,
                    "tone": tone_score
                },
                "weights": self.behavioral_weights,
                "chatgpt_feedback": chatgpt_evaluation.get("feedback", ""),
                "tone_analysis": tone_analysis
            }
            
        except Exception as e:
            logger.error(f"Error calculating behavioral score: {e}")
            return {
                "total_score": 0,
                "score_breakdown": {},
                "raw_scores": {},
                "weights": self.behavioral_weights,
                "chatgpt_feedback": "Error in scoring calculation",
                "tone_analysis": {}
            }
    
    def _calculate_time_score(self, time_taken: float) -> float:
        """
        Calculate time score based on time taken (inverse relationship)
        """
        # Define optimal time ranges (in seconds)
        optimal_ranges = {
            "easy": (30, 120),      # 30 seconds to 2 minutes
            "medium": (60, 300),    # 1 to 5 minutes
            "hard": (120, 600)      # 2 to 10 minutes
        }
        
        # For now, use medium difficulty as default
        min_time, max_time = optimal_ranges["medium"]
        
        if time_taken <= min_time:
            # Too fast - might indicate rushing
            return 80
        elif min_time < time_taken <= max_time:
            # Optimal range
            return 100
        elif max_time < time_taken <= max_time * 1.5:
            # Slightly over time
            return 70
        elif max_time * 1.5 < time_taken <= max_time * 2:
            # Over time
            return 50
        else:
            # Way over time
            return 30
    
    def _calculate_tone_score_from_analysis(self, tone_analysis: Dict[str, Any]) -> float:
        """
        Calculate tone score from audio analysis
        """
        try:
            # Extract relevant metrics
            clarity_score = tone_analysis.get("clarity_score", 0.0)
            professionalism_score = tone_analysis.get("professionalism_score", 0.0)
            sentiment_score = abs(tone_analysis.get("sentiment_score", 0.0))
            
            # Weighted combination
            tone_score = (
                clarity_score * 0.3 +
                professionalism_score * 0.4 +
                sentiment_score * 0.3
            )
            
            return min(100.0, tone_score * 100)
            
        except Exception as e:
            logger.error(f"Error calculating tone score: {e}")
            return 0.0
    
    def calculate_overall_interview_score(self, technical_score: float, behavioral_score: float) -> float:
        """
        Calculate overall interview score
        """
        # Equal weight for technical and behavioral
        overall_score = (technical_score + behavioral_score) / 2
        return round(overall_score, 2)
    
    def generate_score_breakdown(self, scores: Dict[str, Any], interview_type: str) -> List[Dict[str, Any]]:
        """
        Generate detailed score breakdown for database storage
        """
        breakdowns = []
        
        if interview_type == "technical":
            raw_scores = scores.get("raw_scores", {})
            weights = scores.get("weights", {})
            
            for category, score in raw_scores.items():
                breakdowns.append({
                    "category": category,
                    "subcategory": None,
                    "score": score,
                    "weight": weights.get(category, 0),
                    "feedback": scores.get("feedback", "")
                })
                
        elif interview_type == "behavioral":
            raw_scores = scores.get("raw_scores", {})
            weights = scores.get("weights", {})
            
            for category, score in raw_scores.items():
                breakdowns.append({
                    "category": category,
                    "subcategory": None,
                    "score": score,
                    "weight": weights.get(category, 0),
                    "feedback": scores.get("chatgpt_feedback", "")
                })
        
        return breakdowns
    
    def get_score_grade(self, score: float) -> str:
        """
        Convert numerical score to letter grade
        """
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "F"
