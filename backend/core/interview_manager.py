from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import random
import os

from models import Interview, InterviewSession, Question, Response, Score, ScoreBreakdown
from models.interview import InterviewType, InterviewStatus
from models.question import QuestionType, DifficultyLevel
from core.ai_service import AIService
from core.audio_processor import AudioProcessor
from core.scoring_engine import ScoringEngine

logger = logging.getLogger(__name__)


class InterviewManager:
    def __init__(self):
        self.ai_service = AIService()
        self.audio_processor = AudioProcessor()
        self.scoring_engine = ScoringEngine()
    
    async def create_interview(self, db: Session, user_id: int, interview_type: InterviewType, title: str, description: str = None) -> Interview:
        """
        Create a new interview session
        """
        try:
            interview = Interview(
                user_id=user_id,
                interview_type=interview_type,
                status=InterviewStatus.PENDING,
                title=title,
                description=description
            )
            
            db.add(interview)
            db.commit()
            db.refresh(interview)
            
            logger.info(f"Created interview {interview.id} for user {user_id}")
            return interview
            
        except Exception as e:
            logger.error(f"Error creating interview: {e}")
            db.rollback()
            raise
    
    async def start_interview_session(self, db: Session, interview_id: int, session_type: InterviewType) -> InterviewSession:
        """
        Start a new interview session (technical or behavioral)
        """
        try:
            session = InterviewSession(
                interview_id=interview_id,
                session_type=session_type,
                start_time=datetime.utcnow()
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            
            # Update interview status
            interview = db.query(Interview).filter(Interview.id == interview_id).first()
            if interview:
                interview.status = InterviewStatus.IN_PROGRESS
                interview.started_at = datetime.utcnow()
                db.commit()
            
            logger.info(f"Started session {session.id} for interview {interview_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error starting interview session: {e}")
            db.rollback()
            raise
    
    async def get_next_question(self, db: Session, session_id: int, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM) -> Optional[Question]:
        """
        Get the next question for the interview session
        """
        try:
            session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
            if not session:
                raise ValueError("Session not found")
            
            # Get questions based on session type
            if session.session_type == InterviewType.TECHNICAL:
                question_types = [QuestionType.LEETCODE, QuestionType.SYSTEM_DESIGN]
            else:
                question_types = [QuestionType.BEHAVIORAL]
            
            # Get questions that haven't been answered in this session
            answered_question_ids = db.query(Response.question_id).filter(
                Response.session_id == session_id
            ).subquery()
            
            available_questions = db.query(Question).filter(
                Question.question_type.in_(question_types),
                Question.difficulty == difficulty,
                Question.is_active == 1,
                ~Question.id.in_(answered_question_ids)
            ).all()
            
            if not available_questions:
                # Try with different difficulty
                available_questions = db.query(Question).filter(
                    Question.question_type.in_(question_types),
                    Question.is_active == 1,
                    ~Question.id.in_(answered_question_ids)
                ).all()
            
            if available_questions:
                return random.choice(available_questions)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting next question: {e}")
            raise
    
    async def submit_technical_response(self, db: Session, session_id: int, question_id: int, user_id: int, 
                                      code_response: str, time_taken: float) -> Dict[str, Any]:
        """
        Submit and evaluate a technical response
        """
        try:
            # Get question details
            question = db.query(Question).filter(Question.id == question_id).first()
            if not question:
                raise ValueError("Question not found")
            
            # Create response record
            response = Response(
                user_id=user_id,
                session_id=session_id,
                question_id=question_id,
                code_response=code_response,
                duration_seconds=time_taken,
                start_time=datetime.utcnow() - timedelta(seconds=time_taken),
                end_time=datetime.utcnow()
            )
            
            db.add(response)
            db.commit()
            db.refresh(response)
            
            # Evaluate using AI
            evaluation = await self.ai_service.evaluate_technical_solution(
                problem=question.problem_statement or question.content,
                solution=code_response,
                expected_output=question.expected_output or ""
            )
            
            # Calculate score
            score_result = self.scoring_engine.calculate_technical_score(evaluation, time_taken)
            
            # Create score record
            score = Score(
                response_id=response.id,
                interview_id=response.interview_id,
                total_score=score_result["total_score"],
                accuracy_score=score_result["raw_scores"].get("correctness", 0),
                time_score=score_result["raw_scores"].get("time", 0),
                optimality_score=score_result["raw_scores"].get("optimality", 0),
                process_score=score_result["raw_scores"].get("process", 0),
                scoring_method="technical"
            )
            
            db.add(score)
            db.commit()
            db.refresh(score)
            
            # Update response with score
            response.score = score_result["total_score"]
            response.feedback = score_result["feedback"]
            response.score_breakdown = score_result["score_breakdown"]
            db.commit()
            
            return {
                "response_id": response.id,
                "score": score_result["total_score"],
                "feedback": score_result["feedback"],
                "evaluation": evaluation,
                "score_breakdown": score_result["score_breakdown"]
            }
            
        except Exception as e:
            logger.error(f"Error submitting technical response: {e}")
            db.rollback()
            raise
    
    async def submit_behavioral_response(self, db: Session, session_id: int, question_id: int, user_id: int,
                                       audio_file_path: str) -> Dict[str, Any]:
        """
        Submit and evaluate a behavioral response with audio
        """
        try:
            # Get question details
            question = db.query(Question).filter(Question.id == question_id).first()
            if not question:
                raise ValueError("Question not found")
            
            # Process audio file
            audio_result = self.audio_processor.process_audio_file(audio_file_path)
            
            if not audio_result["success"]:
                raise ValueError(f"Audio processing failed: {audio_result.get('error', 'Unknown error')}")
            
            # Create response record
            response = Response(
                user_id=user_id,
                session_id=session_id,
                question_id=question_id,
                text_response=audio_result["transcription"],
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow()
            )
            
            db.add(response)
            db.commit()
            db.refresh(response)
            
            # Create audio response record
            from models.response import AudioResponse
            audio_response = AudioResponse(
                response_id=response.id,
                file_path=audio_file_path,
                file_size=os.path.getsize(audio_file_path),
                duration_seconds=audio_result["audio_features"].get("duration_seconds", 0),
                format=os.path.splitext(audio_file_path)[1],
                transcription=audio_result["transcription"],
                audio_analysis=audio_result["tone_analysis"],
                is_processed=2  # Completed
            )
            
            db.add(audio_response)
            db.commit()
            
            # Evaluate using ChatGPT
            chatgpt_evaluation = await self.ai_service.evaluate_behavioral_response(
                question=question.content,
                response=audio_result["transcription"],
                key_points=question.key_points or []
            )
            
            # Calculate score
            score_result = self.scoring_engine.calculate_behavioral_score(
                chatgpt_evaluation, 
                audio_result["tone_analysis"]
            )
            
            # Create score record
            score = Score(
                response_id=response.id,
                interview_id=response.interview_id,
                total_score=score_result["total_score"],
                chatgpt_score=score_result["raw_scores"].get("chatgpt", 0),
                tone_score=score_result["raw_scores"].get("tone", 0),
                scoring_method="behavioral"
            )
            
            db.add(score)
            db.commit()
            db.refresh(score)
            
            # Update response with score
            response.score = score_result["total_score"]
            response.feedback = score_result["chatgpt_feedback"]
            response.score_breakdown = score_result["score_breakdown"]
            db.commit()
            
            return {
                "response_id": response.id,
                "score": score_result["total_score"],
                "feedback": score_result["chatgpt_feedback"],
                "transcription": audio_result["transcription"],
                "tone_analysis": audio_result["tone_analysis"],
                "score_breakdown": score_result["score_breakdown"]
            }
            
        except Exception as e:
            logger.error(f"Error submitting behavioral response: {e}")
            db.rollback()
            raise
    
    async def end_interview_session(self, db: Session, session_id: int) -> Dict[str, Any]:
        """
        End an interview session and calculate final scores
        """
        try:
            session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
            if not session:
                raise ValueError("Session not found")
            
            # Update session end time
            session.end_time = datetime.utcnow()
            session.duration_seconds = (session.end_time - session.start_time).total_seconds()
            
            # Calculate session score
            responses = db.query(Response).filter(Response.session_id == session_id).all()
            if responses:
                avg_score = sum(r.score or 0 for r in responses) / len(responses)
                session.session_score = round(avg_score, 2)
                session.questions_answered = len(responses)
            
            db.commit()
            
            return {
                "session_id": session.id,
                "session_score": session.session_score,
                "questions_answered": session.questions_answered,
                "duration_seconds": session.duration_seconds
            }
            
        except Exception as e:
            logger.error(f"Error ending interview session: {e}")
            db.rollback()
            raise
    
    async def get_interview_summary(self, db: Session, interview_id: int) -> Dict[str, Any]:
        """
        Get comprehensive interview summary with scores
        """
        try:
            interview = db.query(Interview).filter(Interview.id == interview_id).first()
            if not interview:
                raise ValueError("Interview not found")
            
            sessions = db.query(InterviewSession).filter(InterviewSession.interview_id == interview_id).all()
            
            technical_session = next((s for s in sessions if s.session_type == InterviewType.TECHNICAL), None)
            behavioral_session = next((s for s in sessions if s.session_type == InterviewType.BEHAVIORAL), None)
            
            summary = {
                "interview_id": interview.id,
                "title": interview.title,
                "status": interview.status.value,
                "technical_score": technical_session.session_score if technical_session else None,
                "behavioral_score": behavioral_session.session_score if behavioral_session else None,
                "overall_score": None
            }
            
            # Calculate overall score
            if technical_session and behavioral_session:
                overall_score = self.scoring_engine.calculate_overall_interview_score(
                    technical_session.session_score or 0,
                    behavioral_session.session_score or 0
                )
                summary["overall_score"] = overall_score
                interview.overall_score = overall_score
                db.commit()
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting interview summary: {e}")
            raise
