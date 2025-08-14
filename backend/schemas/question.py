from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    LEETCODE = "leetcode"
    SYSTEM_DESIGN = "system_design"
    BEHAVIORAL = "behavioral"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionCategoryCreate(BaseModel):
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    question_type: QuestionType = Field(..., description="Type of questions in this category")


class QuestionCategoryResponse(QuestionCategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LeetCodeQuestionCreate(BaseModel):
    """Schema for LeetCode questions"""
    title: str = Field(..., description="Question title")
    problem_statement: str = Field(..., description="Full problem description")
    constraints: Optional[str] = Field(None, description="Problem constraints")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="Example inputs and outputs")
    test_cases: Optional[List[Dict[str, Any]]] = Field(None, description="Test cases")
    expected_output: Optional[str] = Field(None, description="Expected output format")
    difficulty: DifficultyLevel = Field(..., description="Question difficulty")
    tags: Optional[List[str]] = Field(None, description="Problem tags")
    estimated_time: Optional[int] = Field(None, description="Estimated time in minutes")
    category_name: str = Field(..., description="Category name")


class SystemDesignQuestionCreate(BaseModel):
    """Schema for System Design questions"""
    title: str = Field(..., description="Question title")
    system_requirements: str = Field(..., description="System requirements")
    scale_requirements: Optional[str] = Field(None, description="Scale requirements")
    design_constraints: Optional[str] = Field(None, description="Design constraints")
    difficulty: DifficultyLevel = Field(..., description="Question difficulty")
    tags: Optional[List[str]] = Field(None, description="Problem tags")
    estimated_time: Optional[int] = Field(None, description="Estimated time in minutes")
    category_name: str = Field(..., description="Category name")


class BehavioralQuestionCreate(BaseModel):
    """Schema for Behavioral questions"""
    title: str = Field(..., description="Question title")
    scenario: str = Field(..., description="Behavioral scenario")
    key_points: Optional[List[str]] = Field(None, description="Key points to evaluate")
    follow_up_questions: Optional[List[str]] = Field(None, description="Follow-up questions")
    difficulty: DifficultyLevel = Field(..., description="Question difficulty")
    tags: Optional[List[str]] = Field(None, description="Problem tags")
    estimated_time: Optional[int] = Field(None, description="Estimated time in minutes")
    category_name: str = Field(..., description="Category name")


class QuestionCreate(BaseModel):
    """Generic question creation schema"""
    question_type: QuestionType
    title: str
    content: str
    description: Optional[str] = None
    difficulty: DifficultyLevel
    tags: Optional[List[str]] = None
    estimated_time: Optional[int] = None
    category_name: str
    
    # Technical question fields
    problem_statement: Optional[str] = None
    constraints: Optional[str] = None
    examples: Optional[List[Dict[str, Any]]] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    expected_output: Optional[str] = None
    
    # System design fields
    system_requirements: Optional[str] = None
    scale_requirements: Optional[str] = None
    design_constraints: Optional[str] = None
    
    # Behavioral fields
    scenario: Optional[str] = None
    key_points: Optional[List[str]] = None
    follow_up_questions: Optional[List[str]] = None


class QuestionResponse(BaseModel):
    id: int
    question_type: QuestionType
    title: str
    content: str
    description: Optional[str]
    difficulty: DifficultyLevel
    tags: Optional[List[str]]
    estimated_time: Optional[int]
    category: QuestionCategoryResponse
    
    # Technical fields
    problem_statement: Optional[str]
    constraints: Optional[str]
    examples: Optional[List[Dict[str, Any]]]
    test_cases: Optional[List[Dict[str, Any]]]
    expected_output: Optional[str]
    
    # System design fields
    system_requirements: Optional[str]
    scale_requirements: Optional[str]
    design_constraints: Optional[str]
    
    # Behavioral fields
    scenario: Optional[str]
    key_points: Optional[List[str]]
    follow_up_questions: Optional[List[str]]
    
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Batch import schemas for preprocessing
class LeetCodeBatchImport(BaseModel):
    """Schema for batch importing LeetCode questions"""
    questions: List[LeetCodeQuestionCreate]


class SystemDesignBatchImport(BaseModel):
    """Schema for batch importing System Design questions"""
    questions: List[SystemDesignQuestionCreate]


class BehavioralBatchImport(BaseModel):
    """Schema for batch importing Behavioral questions"""
    questions: List[BehavioralQuestionCreate]
