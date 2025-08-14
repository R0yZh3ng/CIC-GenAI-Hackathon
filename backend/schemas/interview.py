from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class InterviewType(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


class InterviewStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InterviewCreate(BaseModel):
    user_id: int = Field(..., description="User ID")
    interview_type: InterviewType = Field(..., description="Type of interview")
    title: str = Field(..., description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    interview_type: InterviewType
    status: InterviewStatus
    title: str
    description: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    technical_score: Optional[int]
    behavioral_score: Optional[int]
    overall_score: Optional[int]

    class Config:
        from_attributes = True


class InterviewSessionCreate(BaseModel):
    interview_id: int = Field(..., description="Interview ID")
    session_type: InterviewType = Field(..., description="Session type")


class InterviewSessionResponse(BaseModel):
    id: int
    interview_id: int
    session_type: InterviewType
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[int]
    session_score: Optional[int]
    questions_answered: int
    total_questions: int

    class Config:
        from_attributes = True
