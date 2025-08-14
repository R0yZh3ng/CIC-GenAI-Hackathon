from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class InterviewType(enum.Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


class InterviewStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_type = Column(Enum(InterviewType))
    status = Column(Enum(InterviewStatus), default=InterviewStatus.PENDING)
    title = Column(String)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Overall scores
    technical_score = Column(Integer, nullable=True)  # 0-100
    behavioral_score = Column(Integer, nullable=True)  # 0-100
    overall_score = Column(Integer, nullable=True)  # 0-100

    # Relationships
    user = relationship("User", back_populates="interviews")
    sessions = relationship("InterviewSession", back_populates="interview")
    responses = relationship("Response", back_populates="interview")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    session_type = Column(Enum(InterviewType))  # technical or behavioral
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Session-specific scores
    session_score = Column(Integer, nullable=True)  # 0-100
    questions_answered = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)

    # Relationships
    interview = relationship("Interview", back_populates="sessions")
    responses = relationship("Response", back_populates="session")
