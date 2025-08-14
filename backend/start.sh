#!/bin/bash

# AI Interviewer Backend Startup Script

echo "🚀 Starting AI Interviewer Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with the following variables:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "DATABASE_URL=sqlite:///./interviewer.db"
    echo "SECRET_KEY=your_secret_key_here"
    echo ""
    echo "Creating a basic .env file..."
    cat > .env << EOF
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=sqlite:///./interviewer.db

# Security
SECRET_KEY=your_secret_key_here

# Redis (optional)
REDIS_URL=redis://localhost:6379
EOF
    echo "✅ Created .env file. Please update it with your actual values."
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the application
echo "🌟 Starting FastAPI application..."
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo "🔗 API Base URL: http://localhost:8000"
echo ""

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info
