#!/usr/bin/env python3
import asyncio
import pandas as pd
import os
from core.ai_service import AIService
from typing import List, Dict
import random

class RAGInterviewChatbot:
    def __init__(self, csv_folder_path: str):
        self.ai_service = AIService()
        self.csv_folder = csv_folder_path
        self.technical_questions = []
        self.current_section = None
        self.question_count = 0
        self.waiting_for_answer = False
        self.current_question = None
        self.load_questions()
    
    def load_questions(self):
        """Load technical questions from CSV files"""
        if not os.path.exists(self.csv_folder):
            print(f"CSV folder not found: {self.csv_folder}")
            return
        
        for filename in os.listdir(self.csv_folder):
            if filename.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(self.csv_folder, filename))
                    # Assume CSV has columns: Question, Answer, Difficulty, Topic
                    for _, row in df.iterrows():
                        self.technical_questions.append({
                            'question': row.get('Question', ''),
                            'answer': row.get('Answer', ''),
                            'difficulty': row.get('Difficulty', 'Medium'),
                            'topic': row.get('Topic', 'General'),
                            'source': filename
                        })
                    print(f"Loaded {len(df)} questions from {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        print(f"Total questions loaded: {len(self.technical_questions)}")
    
    def get_random_question(self) -> Dict:
        """Get a random technical question from the loaded data"""
        if not self.technical_questions:
            return {
                'question': 'What is the time complexity of binary search?',
                'answer': 'O(log n)',
                'difficulty': 'Medium',
                'topic': 'Algorithms'
            }
        return random.choice(self.technical_questions)
    
    async def ask_technical_question(self) -> str:
        """Ask a technical question from CSV data"""
        question_data = self.get_random_question()
        
        prompt = f"""You are a senior software engineer conducting a technical coding interview. 

Use this LeetCode-style problem from our database:
PROBLEM: {question_data['question']}
EXPECTED SOLUTION: {question_data['answer']}
DIFFICULTY: {question_data['difficulty']}
TOPIC: {question_data['topic']}

Present this as a CODING PROBLEM in this format:
CODING PROBLEM: [Present the problem clearly with examples and constraints]
DIFFICULTY: {question_data['difficulty']}
TOPIC: {question_data['topic']}
EXAMPLE: [Provide a clear input/output example]
CONSTRAINTS: [List any constraints]

This should be a hands-on coding problem that requires writing actual code, not theoretical questions. Present the problem now:"""
        
        self.waiting_for_answer = True
        self.current_question_data = question_data
        return await self.ai_service.chat_with_bedrock(prompt)
    
    async def evaluate_technical_answer(self, user_answer: str) -> str:
        """Evaluate the technical answer against CSV data"""
        prompt = f"""You are evaluating a LeetCode-style coding solution.

ORIGINAL PROBLEM: {self.current_question_data['question']}
EXPECTED SOLUTION: {self.current_question_data['answer']}
DIFFICULTY: {self.current_question_data['difficulty']}
TOPIC: {self.current_question_data['topic']}

CANDIDATE'S CODE: {user_answer}

Evaluate this code solution and provide feedback:

CODE EVALUATION:
✅ CORRECTNESS: [Does the code solve the problem correctly?]
⏱️ TIME COMPLEXITY: [What's the time complexity? Is it optimal?]
💾 SPACE COMPLEXITY: [What's the space complexity?]
🔧 CODE QUALITY: [Is the code clean, readable, and well-structured?]
⚠️ ISSUES: [Any bugs, edge cases missed, or improvements needed?]
💡 OPTIMIZATION: [How can this be optimized?]
📚 EXPECTED SOLUTION: {self.current_question_data['answer']}
SCORE: [X/10]

Evaluate the code now:"""
        
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
        question = await self.ai_service.chat_with_bedrock(prompt)
        self.current_question = question  # Store the question for evaluation
        return question
    
    async def evaluate_behavioral_answer(self, user_answer: str) -> str:
        """Evaluate the behavioral answer"""
        prompt = f"""You are evaluating a behavioral interview answer.

Question asked: {self.current_question}
Candidate's answer: {user_answer}

Provide feedback in this exact format:
FEEDBACK:
📊 STAR COMPLETENESS: [Rate Situation/Task/Action/Result - which were covered]
🎯 KEY STRENGTHS: [What they demonstrated well]
🔄 MISSING ELEMENTS: [What could be improved or was missing]
OVERALL RATING: [X/10]

Evaluate now:"""
        
        self.waiting_for_answer = False
        return await self.ai_service.chat_with_bedrock(prompt)

async def main():
    # Use default CSV folder path
    csv_path = "../questions"  # Default path
    
    chatbot = RAGInterviewChatbot(csv_path)
    
    print("🎯 RAG SOFTWARE INTERVIEW SIMULATOR")
    print("=" * 50)
    print("Choose section:")
    print("1. Technical Interview (From CSV Data)")
    print("2. Behavioral Interview (STAR Method)")
    print("Type 'switch' to change sections, 'quit' to exit")
    print("=" * 50)
    
    while True:
        if not chatbot.current_section:
            section = input("\nSelect section (1 or 2): ").strip()
            if section == "1":
                chatbot.current_section = "technical"
                print(f"\n🔧 TECHNICAL INTERVIEW MODE ({len(chatbot.technical_questions)} questions loaded)")
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