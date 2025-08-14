from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .interview import Interview, InterviewSession
from .question import Question, QuestionCategory
from .response import Response, AudioResponse
from .score import Score, ScoreBreakdown

__all__ = [
    "Base",
    "User",
    "Interview", 
    "InterviewSession",
    "Question",
    "QuestionCategory",
    "Response",
    "AudioResponse",
    "Score",
    "ScoreBreakdown"
]
