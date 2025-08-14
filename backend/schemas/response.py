from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ResponseCreate(BaseModel):
    user_id: int = Field(..., description="User ID")
    session_id: int = Field(..., description="Session ID")
    question_id: int = Field(..., description="Question ID")
    text_response: Optional[str] = Field(None, description="Text response")
    code_response: Optional[str] = Field(None, description="Code response")
    duration_seconds: Optional[float] = Field(None, description="Response duration")


class ResponseResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    question_id: int
    text_response: Optional[str]
    code_response: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[float]
    score: Optional[float]
    feedback: Optional[str]
    score_breakdown: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class TechnicalResponseSubmit(BaseModel):
    question_id: int = Field(..., description="Question ID")
    user_id: int = Field(..., description="User ID")
    code_response: str = Field(..., description="Code solution")
    time_taken: float = Field(..., description="Time taken in seconds")


class BehavioralResponseSubmit(BaseModel):
    question_id: int = Field(..., description="Question ID")
    user_id: int = Field(..., description="User ID")
    # Audio file will be handled separately via multipart form


class ScoreResponse(BaseModel):
    response_id: int
    interview_id: int
    total_score: float
    accuracy_score: Optional[float]
    time_score: Optional[float]
    optimality_score: Optional[float]
    process_score: Optional[float]
    chatgpt_score: Optional[float]
    tone_score: Optional[float]
    scoring_method: str
    created_at: datetime

    class Config:
        from_attributes = True
