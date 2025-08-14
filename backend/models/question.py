from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class QuestionType(enum.Enum):
    LEETCODE = "leetcode"
    SYSTEM_DESIGN = "system_design"
    BEHAVIORAL = "behavioral"


class DifficultyLevel(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    question_type = Column(Enum(QuestionType))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    questions = relationship("Question", back_populates="category")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("question_categories.id"))
    question_type = Column(Enum(QuestionType))
    difficulty = Column(Enum(DifficultyLevel))
    
    # Question content
    title = Column(String)
    content = Column(Text)
    description = Column(Text, nullable=True)
    
    # For technical questions
    problem_statement = Column(Text, nullable=True)
    constraints = Column(Text, nullable=True)
    examples = Column(JSON, nullable=True)  # List of example inputs/outputs
    test_cases = Column(JSON, nullable=True)  # List of test cases
    expected_output = Column(Text, nullable=True)
    
    # For system design questions
    system_requirements = Column(Text, nullable=True)
    scale_requirements = Column(Text, nullable=True)
    design_constraints = Column(Text, nullable=True)
    
    # For behavioral questions
    scenario = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # List of key points to look for
    follow_up_questions = Column(JSON, nullable=True)  # List of follow-up questions
    
    # Metadata
    tags = Column(JSON, nullable=True)  # List of tags
    estimated_time = Column(Integer, nullable=True)  # Estimated time in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive

    # Relationships
    category = relationship("QuestionCategory", back_populates="questions")
    responses = relationship("Response", back_populates="question")
