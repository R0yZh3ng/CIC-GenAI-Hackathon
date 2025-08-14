from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    
    # Overall score
    total_score = Column(Float)  # 0-100
    
    # Score breakdown
    accuracy_score = Column(Float, nullable=True)  # Technical accuracy
    time_score = Column(Float, nullable=True)  # Time efficiency
    optimality_score = Column(Float, nullable=True)  # Solution optimality
    process_score = Column(Float, nullable=True)  # Problem-solving process
    
    # Behavioral scores
    chatgpt_score = Column(Float, nullable=True)  # ChatGPT evaluation
    tone_score = Column(Float, nullable=True)  # Tone analysis
    
    # Metadata
    scoring_method = Column(String)  # "technical" or "behavioral"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    response = relationship("Response")
    interview = relationship("Interview")
    breakdowns = relationship("ScoreBreakdown", back_populates="score")


class ScoreBreakdown(Base):
    __tablename__ = "score_breakdowns"

    id = Column(Integer, primary_key=True, index=True)
    score_id = Column(Integer, ForeignKey("scores.id"))
    
    # Detailed breakdown
    category = Column(String)  # e.g., "accuracy", "time", "tone", "clarity"
    subcategory = Column(String, nullable=True)  # e.g., "syntax", "logic", "efficiency"
    score = Column(Float)  # 0-100
    weight = Column(Float)  # Weight in overall calculation
    feedback = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)  # Additional scoring details
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    score = relationship("Score", back_populates="breakdowns")
