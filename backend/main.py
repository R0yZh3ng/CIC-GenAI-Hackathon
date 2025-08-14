from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import tempfile
import logging

from database import get_db, engine
from models import Base
from core.interview_manager import InterviewManager
from schemas.interview import InterviewCreate, InterviewResponse
from schemas.question import QuestionResponse, LeetCodeBatchImport, SystemDesignBatchImport, BehavioralBatchImport
from models.interview import InterviewType, InterviewStatus
from models.question import QuestionType, DifficultyLevel

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Interviewer API",
    description="AI-powered interview system with technical and behavioral assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize interview manager
interview_manager = InterviewManager()


@app.get("/")
async def root():
    return {"message": "AI Interviewer API is running"}


@app.post("/chat/")
async def chat_with_bedrock(message: str):
    """Chat with Bedrock OpenAI GPT model"""
    try:
        response = await interview_manager.ai_service.chat_with_bedrock(message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Interview Management Endpoints
@app.post("/interviews/", response_model=InterviewResponse)
async def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db)
):
    """Create a new interview"""
    try:
        interview = await interview_manager.create_interview(
            db=db,
            user_id=interview_data.user_id,
            interview_type=interview_data.interview_type,
            title=interview_data.title,
            description=interview_data.description
        )
        return interview
    except Exception as e:
        logger.error(f"Error creating interview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interviews/{interview_id}/sessions/")
async def start_interview_session(
    interview_id: int,
    session_type: InterviewType,
    db: Session = Depends(get_db)
):
    """Start a new interview session (technical or behavioral)"""
    try:
        session = await interview_manager.start_interview_session(
            db=db,
            interview_id=interview_id,
            session_type=session_type
        )
        return {
            "session_id": session.id,
            "session_type": session.session_type.value,
            "start_time": session.start_time
        }
    except Exception as e:
        logger.error(f"Error starting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}/questions/next/")
async def get_next_question(
    session_id: int,
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
    db: Session = Depends(get_db)
):
    """Get the next question for the interview session"""
    try:
        question = await interview_manager.get_next_question(
            db=db,
            session_id=session_id,
            difficulty=difficulty
        )
        
        if not question:
            return {"message": "No more questions available"}
        
        return {
            "question_id": question.id,
            "title": question.title,
            "content": question.content,
            "question_type": question.question_type.value,
            "difficulty": question.difficulty.value,
            "problem_statement": question.problem_statement,
            "constraints": question.constraints,
            "examples": question.examples,
            "system_requirements": question.system_requirements,
            "scenario": question.scenario,
            "key_points": question.key_points
        }
    except Exception as e:
        logger.error(f"Error getting next question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions/{session_id}/responses/technical/")
async def submit_technical_response(
    session_id: int,
    question_id: int = Form(...),
    user_id: int = Form(...),
    code_response: str = Form(...),
    time_taken: float = Form(...),
    db: Session = Depends(get_db)
):
    """Submit a technical response (coding problem)"""
    try:
        result = await interview_manager.submit_technical_response(
            db=db,
            session_id=session_id,
            question_id=question_id,
            user_id=user_id,
            code_response=code_response,
            time_taken=time_taken
        )
        return result
    except Exception as e:
        logger.error(f"Error submitting technical response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions/{session_id}/responses/behavioral/")
async def submit_behavioral_response(
    session_id: int,
    question_id: int = Form(...),
    user_id: int = Form(...),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Submit a behavioral response with audio recording"""
    try:
        # Validate file type
        if not audio_file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
            raise HTTPException(status_code=400, detail="Unsupported audio format")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            result = await interview_manager.submit_behavioral_response(
                db=db,
                session_id=session_id,
                question_id=question_id,
                user_id=user_id,
                audio_file_path=temp_file_path
            )
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except Exception as e:
        logger.error(f"Error submitting behavioral response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions/{session_id}/end/")
async def end_interview_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """End an interview session"""
    try:
        result = await interview_manager.end_interview_session(
            db=db,
            session_id=session_id
        )
        return result
    except Exception as e:
        logger.error(f"Error ending session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/interviews/{interview_id}/summary/")
async def get_interview_summary(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive interview summary"""
    try:
        summary = await interview_manager.get_interview_summary(
            db=db,
            interview_id=interview_id
        )
        return summary
    except Exception as e:
        logger.error(f"Error getting interview summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Question Management Endpoints
@app.post("/questions/import/leetcode/")
async def import_leetcode_questions(
    batch_data: LeetCodeBatchImport,
    db: Session = Depends(get_db)
):
    """Import LeetCode questions in batch"""
    try:
        from models.question import Question, QuestionCategory
        from models.question import QuestionType
        
        imported_count = 0
        
        for question_data in batch_data.questions:
            # Get or create category
            category = db.query(QuestionCategory).filter(
                QuestionCategory.name == question_data.category_name
            ).first()
            
            if not category:
                category = QuestionCategory(
                    name=question_data.category_name,
                    question_type=QuestionType.LEETCODE
                )
                db.add(category)
                db.commit()
                db.refresh(category)
            
            # Create question
            question = Question(
                category_id=category.id,
                question_type=QuestionType.LEETCODE,
                difficulty=question_data.difficulty,
                title=question_data.title,
                content=question_data.problem_statement,
                problem_statement=question_data.problem_statement,
                constraints=question_data.constraints,
                examples=question_data.examples,
                test_cases=question_data.test_cases,
                expected_output=question_data.expected_output,
                tags=question_data.tags,
                estimated_time=question_data.estimated_time
            )
            
            db.add(question)
            imported_count += 1
        
        db.commit()
        return {"message": f"Successfully imported {imported_count} LeetCode questions"}
        
    except Exception as e:
        logger.error(f"Error importing LeetCode questions: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/questions/import/system-design/")
async def import_system_design_questions(
    batch_data: SystemDesignBatchImport,
    db: Session = Depends(get_db)
):
    """Import System Design questions in batch"""
    try:
        from models.question import Question, QuestionCategory
        from models.question import QuestionType
        
        imported_count = 0
        
        for question_data in batch_data.questions:
            # Get or create category
            category = db.query(QuestionCategory).filter(
                QuestionCategory.name == question_data.category_name
            ).first()
            
            if not category:
                category = QuestionCategory(
                    name=question_data.category_name,
                    question_type=QuestionType.SYSTEM_DESIGN
                )
                db.add(category)
                db.commit()
                db.refresh(category)
            
            # Create question
            question = Question(
                category_id=category.id,
                question_type=QuestionType.SYSTEM_DESIGN,
                difficulty=question_data.difficulty,
                title=question_data.title,
                content=question_data.system_requirements,
                system_requirements=question_data.system_requirements,
                scale_requirements=question_data.scale_requirements,
                design_constraints=question_data.design_constraints,
                tags=question_data.tags,
                estimated_time=question_data.estimated_time
            )
            
            db.add(question)
            imported_count += 1
        
        db.commit()
        return {"message": f"Successfully imported {imported_count} System Design questions"}
        
    except Exception as e:
        logger.error(f"Error importing System Design questions: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/questions/import/behavioral/")
async def import_behavioral_questions(
    batch_data: BehavioralBatchImport,
    db: Session = Depends(get_db)
):
    """Import Behavioral questions in batch"""
    try:
        from models.question import Question, QuestionCategory
        from models.question import QuestionType
        
        imported_count = 0
        
        for question_data in batch_data.questions:
            # Get or create category
            category = db.query(QuestionCategory).filter(
                QuestionCategory.name == question_data.category_name
            ).first()
            
            if not category:
                category = QuestionCategory(
                    name=question_data.category_name,
                    question_type=QuestionType.BEHAVIORAL
                )
                db.add(category)
                db.commit()
                db.refresh(category)
            
            # Create question
            question = Question(
                category_id=category.id,
                question_type=QuestionType.BEHAVIORAL,
                difficulty=question_data.difficulty,
                title=question_data.title,
                content=question_data.scenario,
                scenario=question_data.scenario,
                key_points=question_data.key_points,
                follow_up_questions=question_data.follow_up_questions,
                tags=question_data.tags,
                estimated_time=question_data.estimated_time
            )
            
            db.add(question)
            imported_count += 1
        
        db.commit()
        return {"message": f"Successfully imported {imported_count} Behavioral questions"}
        
    except Exception as e:
        logger.error(f"Error importing Behavioral questions: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
