from fastapi import FastAPI, HTTPException, Request
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
async def evaluate_answer(request: Request):
    """Evaluate user answer"""
    try:
        # Get raw body for debugging
        body = await request.body()
        print(f"Raw request body: {body}")
        
        # Parse JSON
        data = json.loads(body)
        print(f"Parsed data: {data}")
        
        # Validate required fields
        if 'section' not in data or 'answer' not in data:
            raise HTTPException(status_code=422, detail="Missing required fields: section and answer")
        
        section = data['section']
        answer = data['answer']
        question_data = data.get('question_data')
        
        print(f"Section: {section}, Answer: {answer[:50]}...")
        if section == "technical":
            if question_data:
                chatbot.current_question_data = question_data
            feedback = await chatbot.evaluate_technical_answer(answer)
        else:
            feedback = await chatbot.evaluate_behavioral_answer(answer)
        
        return {
            "feedback": feedback,
            "section": section
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Interview API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)