from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_interview_chatbot import RAGInterviewChatbot
import asyncio

app = FastAPI()

# Global chatbot instance
chatbot = RAGInterviewChatbot("../questions")

class QuestionRequest(BaseModel):
    section: str  # "technical" or "behavioral"

class AnswerRequest(BaseModel):
    section: str
    answer: str
    question_data: dict = None

@app.post("/api/question")
async def get_question(request: QuestionRequest):
    """Get a new interview question"""
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

@app.post("/api/evaluate")
async def evaluate_answer(request: AnswerRequest):
    """Evaluate user's answer"""
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

@app.get("/api/stats")
async def get_stats():
    """Get question statistics"""
    return {
        "total_questions": len(chatbot.technical_questions),
        "question_count": chatbot.question_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)