#!/usr/bin/env python3
import asyncio
from core.ai_service import AIService

async def main():
    ai_service = AIService()
    print("🤖 Bedrock Chat Terminal")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        
        response = await ai_service.chat_with_bedrock(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())