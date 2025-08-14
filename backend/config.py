import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./interviewer.db"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Audio Processing
    MAX_AUDIO_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    SUPPORTED_AUDIO_FORMATS: list = [".wav", ".mp3", ".m4a", ".flac"]
    
    # Redis (for caching and Celery)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Scoring Weights
    TECHNICAL_ACCURACY_WEIGHT: float = 0.5
    TECHNICAL_TIME_WEIGHT: float = 0.2
    TECHNICAL_OPTIMALITY_WEIGHT: float = 0.2
    TECHNICAL_PROCESS_WEIGHT: float = 0.1
    
    BEHAVIORAL_CHATGPT_WEIGHT: float = 0.8
    BEHAVIORAL_TONE_WEIGHT: float = 0.2
    
    # Interview Settings
    MAX_INTERVIEW_DURATION: int = 3600  # 1 hour in seconds
    MAX_QUESTIONS_PER_CATEGORY: int = 10
    
    class Config:
        env_file = ".env"


settings = Settings()
