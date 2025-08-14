from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from rag_interview_chatbot import RAGInterviewChatbot
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = RAGInterviewChatbot("../questions")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive message from React frontend
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "get_question":
                # Send question to frontend
                if message["section"] == "technical":
                    question = await chatbot.ask_technical_question()
                    response = {
                        "type": "question",
                        "content": question,
                        "section": "technical",
                        "question_data": chatbot.current_question_data
                    }
                else:
                    question = await chatbot.ask_behavioral_question()
                    response = {
                        "type": "question", 
                        "content": question,
                        "section": "behavioral"
                    }
                
                await websocket.send_text(json.dumps(response))
            
            elif message["type"] == "submit_answer":
                # Evaluate answer and send feedback
                if message["section"] == "technical":
                    if "question_data" in message:
                        chatbot.current_question_data = message["question_data"]
                    feedback = await chatbot.evaluate_technical_answer(message["answer"])
                else:
                    feedback = await chatbot.evaluate_behavioral_answer(message["answer"])
                
                response = {
                    "type": "feedback",
                    "content": feedback,
                    "section": message["section"]
                }
                
                await websocket.send_text(json.dumps(response))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)