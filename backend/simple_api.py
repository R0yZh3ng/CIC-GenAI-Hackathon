from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_interview_chatbot import RAGInterviewChatbot
import json

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot = RAGInterviewChatbot("../questions")

class QuestionRequest(BaseModel):
    section: str  # "technical" or "behavioral"

class AnswerRequest(BaseModel):
    section: str
    answer: str
    question_data: dict = None

@app.post("/question")
async def get_question(request: QuestionRequest):
    """Get interview question"""
    try:
        if request.section == "technical":
            question = await chatbot.ask_technical_question()
            return {
                "question": question,
                "question_data": chatbot.current_question_data,
                "section": "technical"
            }
        else:
            question = await chatbot.ask_behavioral_question()
            return {
                "question": question,
                "section": "behavioral"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
async def evaluate_answer(request: AnswerRequest):
    """Evaluate user answer"""
    try:
        if request.section == "technical":
            if request.question_data:
                chatbot.current_question_data = request.question_data
            feedback = await chatbot.evaluate_technical_answer(request.answer)
        else:
            feedback = await chatbot.evaluate_behavioral_answer(request.answer)
        
        return {
            "feedback": feedback,
            "section": request.section
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Interview API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)