import openai
from typing import List, Dict, Any, Optional
from config import settings
import json
import logging

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def evaluate_behavioral_response(self, question: str, response: str, key_points: List[str]) -> Dict[str, Any]:
        """
        Evaluate behavioral response using ChatGPT
        """
        try:
            prompt = f"""
            You are an expert interviewer evaluating a behavioral response.
            
            Question: {question}
            Key points to evaluate: {', '.join(key_points)}
            
            Candidate Response: {response}
            
            Please evaluate this response on a scale of 0-100 based on:
            1. Relevance to the question
            2. Specificity and detail
            3. STAR method usage (Situation, Task, Action, Result)
            4. Communication clarity
            5. Professionalism
            
            Provide your evaluation in the following JSON format:
            {{
                "score": <0-100>,
                "feedback": "<detailed feedback>",
                "strengths": ["<strength1>", "<strength2>"],
                "areas_for_improvement": ["<area1>", "<area2>"],
                "key_points_covered": ["<point1>", "<point2>"],
                "missing_points": ["<missing_point1>", "<missing_point2>"]
            }}
            """
            
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating behavioral response: {e}")
            return {
                "score": 0,
                "feedback": "Error in evaluation",
                "strengths": [],
                "areas_for_improvement": [],
                "key_points_covered": [],
                "missing_points": []
            }
    
    async def generate_follow_up_questions(self, question: str, response: str, original_follow_ups: List[str]) -> List[str]:
        """
        Generate contextual follow-up questions based on the response
        """
        try:
            prompt = f"""
            Based on the original question and the candidate's response, generate 2-3 relevant follow-up questions.
            
            Original Question: {question}
            Candidate Response: {response}
            Original Follow-up Questions: {original_follow_ups}
            
            Generate follow-up questions that:
            1. Probe deeper into the candidate's experience
            2. Ask for specific examples or details
            3. Challenge assumptions or explore edge cases
            4. Are relevant to the candidate's response
            
            Return as a JSON array of strings.
            """
            
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            follow_ups = json.loads(response.choices[0].message.content)
            return follow_ups if isinstance(follow_ups, list) else []
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return original_follow_ups
    
    async def evaluate_technical_solution(self, problem: str, solution: str, expected_output: str) -> Dict[str, Any]:
        """
        Evaluate technical solution using ChatGPT
        """
        try:
            prompt = f"""
            You are an expert technical interviewer evaluating a coding solution.
            
            Problem: {problem}
            Candidate Solution: {solution}
            Expected Output: {expected_output}
            
            Please evaluate this solution on a scale of 0-100 based on:
            1. Correctness (50% weight)
            2. Time complexity (20% weight)
            3. Code quality and optimality (20% weight)
            4. Problem-solving approach (10% weight)
            
            Provide your evaluation in the following JSON format:
            {{
                "overall_score": <0-100>,
                "correctness_score": <0-100>,
                "time_complexity_score": <0-100>,
                "optimality_score": <0-100>,
                "process_score": <0-100>,
                "feedback": "<detailed feedback>",
                "time_complexity": "<O(n), O(n^2), etc.>",
                "space_complexity": "<O(1), O(n), etc.>",
                "issues": ["<issue1>", "<issue2>"],
                "suggestions": ["<suggestion1>", "<suggestion2>"]
            }}
            """
            
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating technical solution: {e}")
            return {
                "overall_score": 0,
                "correctness_score": 0,
                "time_complexity_score": 0,
                "optimality_score": 0,
                "process_score": 0,
                "feedback": "Error in evaluation",
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "issues": [],
                "suggestions": []
            }
    
    async def evaluate_system_design(self, requirements: str, design: str) -> Dict[str, Any]:
        """
        Evaluate system design response
        """
        try:
            prompt = f"""
            You are an expert system design interviewer evaluating a design solution.
            
            Requirements: {requirements}
            Candidate Design: {design}
            
            Please evaluate this design on a scale of 0-100 based on:
            1. Completeness of the design (30% weight)
            2. Scalability considerations (25% weight)
            3. Technical feasibility (20% weight)
            4. Trade-offs understanding (15% weight)
            5. Communication clarity (10% weight)
            
            Provide your evaluation in the following JSON format:
            {{
                "overall_score": <0-100>,
                "completeness_score": <0-100>,
                "scalability_score": <0-100>,
                "feasibility_score": <0-100>,
                "trade_offs_score": <0-100>,
                "communication_score": <0-100>,
                "feedback": "<detailed feedback>",
                "strengths": ["<strength1>", "<strength2>"],
                "weaknesses": ["<weakness1>", "<weakness2>"],
                "missing_components": ["<component1>", "<component2>"],
                "improvements": ["<improvement1>", "<improvement2>"]
            }}
            """
            
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating system design: {e}")
            return {
                "overall_score": 0,
                "completeness_score": 0,
                "scalability_score": 0,
                "feasibility_score": 0,
                "trade_offs_score": 0,
                "communication_score": 0,
                "feedback": "Error in evaluation",
                "strengths": [],
                "weaknesses": [],
                "missing_components": [],
                "improvements": []
            }
