#!/usr/bin/env python3
import asyncio
from core.ai_service import AIService

class SoftwareInterviewChatbot:
    def __init__(self):
        self.ai_service = AIService()
        self.current_section = None
        self.question_count = 0
        self.waiting_for_answer = False
        self.current_question = None
    
    async def ask_technical_question(self) -> str:
        """Ask a technical question"""
        prompt = """You are a senior software engineer conducting a technical interview. Ask ONE coding/algorithm question.

Format your question exactly like this:
TECHNICAL QUESTION: [Your specific coding question]
DIFFICULTY: [Easy/Medium/Hard]

Ask a question now:"""
        
        self.waiting_for_answer = True
        return await self.ai_service.chat_with_bedrock(prompt)
    
    async def evaluate_technical_answer(self, user_answer: str) -> str:
        """Evaluate the technical answer and give feedback"""
        prompt = f"""You are evaluating a technical interview answer.

Question asked: {self.current_question}
Candidate's answer: {user_answer}

Provide feedback in this exact format:
FEEDBACK:
✓ STRENGTHS: [What they did well]
⚠ AREAS FOR IMPROVEMENT: [Issues with their solution]
💡 SUGGESTIONS: [Specific improvements]
SCORE: [X/10]

provide an plan to improve after evaluation is complete 

Evaluate now:"""
        
        self.waiting_for_answer = False
        return await self.ai_service.chat_with_bedrock(prompt)
    
    async def ask_behavioral_question(self) -> str:
        """Ask a behavioral question"""
        prompt = """You are a hiring manager conducting a behavioral interview. Ask ONE behavioral question.

Format your question exactly like this:
BEHAVIORAL QUESTION: [Your specific behavioral question]
FOCUS AREA: [Leadership/Teamwork/Problem-solving/Communication/etc.]
STAR REMINDER: Please structure your answer using Situation, Task, Action, Result

Ask a question now:"""
        
        self.waiting_for_answer = True
        return await self.ai_service.chat_with_bedrock(prompt)
    
    async def evaluate_behavioral_answer(self, user_answer: str) -> str:
        """Evaluate the behavioral answer and give feedback"""
        prompt = f"""You are evaluating a behavioral interview answer.

Question asked: {self.current_question}
Candidate's answer: {user_answer}

Provide feedback in this exact format:
FEEDBACK:
📊 STAR COMPLETENESS: [Rate Situation/Task/Action/Result - which were covered]
🎯 KEY STRENGTHS: [What they demonstrated well]
🔄 MISSING ELEMENTS: [What could be improved or was missing]
OVERALL RATING: [X/10]

provide an plan to improve after evaluation is complete 

Evaluate now:"""
        
        self.waiting_for_answer = False
        return await self.ai_service.chat_with_bedrock(prompt)

async def main():
    chatbot = SoftwareInterviewChatbot()
    
    print("🎯 SOFTWARE INTERVIEW SIMULATOR")
    print("=" * 50)
    print("Choose section:")
    print("1. Technical Interview (Coding/Algorithms)")
    print("2. Behavioral Interview (STAR Method)")
    print("Type 'switch' to change sections, 'quit' to exit")
    print("=" * 50)
    
    while True:
        if not chatbot.current_section:
            section = input("\nSelect section (1 or 2): ").strip()
            if section == "1":
                chatbot.current_section = "technical"
                print("\n🔧 TECHNICAL INTERVIEW MODE")
            elif section == "2":
                chatbot.current_section = "behavioral"
                print("\n👥 BEHAVIORAL INTERVIEW MODE")
            else:
                print("Please enter 1 or 2")
                continue
        
        if not chatbot.waiting_for_answer:
            # Ask a new question
            if chatbot.current_section == "technical":
                response = await chatbot.ask_technical_question()
            else:
                response = await chatbot.ask_behavioral_question()
            
            chatbot.current_question = response
            print(f"\nInterviewer: {response}")
            print("\n[Provide your answer below]")
        
        user_input = input(f"\n[{chatbot.current_section.upper()}] Your Answer: ")
        
        if user_input.lower() == 'quit':
            print("Interview ended. Good luck!")
            break
        elif user_input.lower() == 'switch':
            chatbot.current_section = None
            chatbot.question_count = 0
            chatbot.waiting_for_answer = False
            continue
        
        # Evaluate the answer
        if chatbot.current_section == "technical":
            feedback = await chatbot.evaluate_technical_answer(user_input)
        else:
            feedback = await chatbot.evaluate_behavioral_answer(user_input)
        
        print(f"\nInterviewer: {feedback}")
        print("\n" + "="*50)
        chatbot.question_count += 1

if __name__ == "__main__":
    asyncio.run(main())