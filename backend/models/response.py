from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    # Response content
    text_response = Column(Text, nullable=True)
    code_response = Column(Text, nullable=True)
    
    # Timing
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Scoring
    score = Column(Float, nullable=True)  # 0-100
    feedback = Column(Text, nullable=True)
    score_breakdown = Column(JSON, nullable=True)  # Detailed scoring breakdown
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="responses")
    interview = relationship("Interview", back_populates="responses")
    session = relationship("InterviewSession", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    audio_response = relationship("AudioResponse", back_populates="response", uselist=False)


class AudioResponse(Base):
    __tablename__ = "audio_responses"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), unique=True)
    
    # Audio file information
    file_path = Column(String)
    file_size = Column(Integer)  # Size in bytes
    duration_seconds = Column(Float)
    format = Column(String)  # wav, mp3, etc.
    
    # Transcription
    transcription = Column(Text, nullable=True)
    transcription_confidence = Column(Float, nullable=True)
    
    # Audio analysis
    audio_analysis = Column(JSON, nullable=True)  # Tone, pace, clarity metrics
    
    # Processing status
    is_processed = Column(Integer, default=0)  # 0: pending, 1: processing, 2: completed, 3: failed
    processing_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    response = relationship("Response", back_populates="audio_response")
