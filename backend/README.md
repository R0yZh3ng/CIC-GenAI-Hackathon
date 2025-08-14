# AI Interviewer Backend

A modular, AI-powered interview system that conducts technical and behavioral interviews with intelligent scoring and feedback.

## Features

- **Technical Interviews**: LeetCode problems and System Design questions
- **Behavioral Interviews**: Audio-based responses with tone analysis
- **AI-Powered Scoring**: ChatGPT integration for intelligent evaluation
- **Modular Architecture**: Clean separation of concerns for easy collaboration
- **Comprehensive Analytics**: Detailed scoring breakdowns and feedback
- **Audio Processing**: Speech-to-text and tone analysis
- **RESTful API**: Full CRUD operations for interviews and responses

## Architecture

```
backend/
├── core/                    # Core business logic
│   ├── ai_service.py       # ChatGPT integration
│   ├── audio_processor.py  # Audio processing & analysis
│   ├── scoring_engine.py   # Scoring algorithms
│   └── interview_manager.py # Interview orchestration
├── models/                  # Database models
│   ├── user.py             # User management
│   ├── interview.py        # Interview sessions
│   ├── question.py         # Question bank
│   ├── response.py         # User responses
│   └── score.py            # Scoring data
├── schemas/                 # API schemas
│   ├── interview.py        # Interview schemas
│   ├── question.py         # Question schemas
│   ├── response.py         # Response schemas
│   └── user.py             # User schemas
├── main.py                  # FastAPI application
├── config.py               # Configuration
├── database.py             # Database setup
└── requirements.txt        # Dependencies
```

## Scoring System

### Technical Interviews (100 points total)
- **Accuracy (50%)**: Correctness of solution
- **Time Efficiency (20%)**: Speed of completion
- **Optimality (20%)**: Code quality and efficiency
- **Process (10%)**: Problem-solving approach

### Behavioral Interviews (100 points total)
- **ChatGPT Evaluation (80%)**: Content analysis and STAR method
- **Tone Analysis (20%)**: Audio clarity, professionalism, sentiment

## Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=sqlite:///./interviewer.db

# Security
SECRET_KEY=your_secret_key_here

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379
```

### 3. Database Setup

The database will be automatically created when you run the application for the first time.

### 4. Run the Application

```bash
# Development
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Core Endpoints

#### Interview Management
- `POST /interviews/` - Create new interview
- `POST /interviews/{id}/sessions/` - Start interview session
- `GET /interviews/{id}/summary/` - Get interview summary

#### Question Management
- `GET /sessions/{id}/questions/next/` - Get next question
- `POST /questions/import/leetcode/` - Import LeetCode questions
- `POST /questions/import/system-design/` - Import System Design questions
- `POST /questions/import/behavioral/` - Import Behavioral questions

#### Response Submission
- `POST /sessions/{id}/responses/technical/` - Submit technical response
- `POST /sessions/{id}/responses/behavioral/` - Submit behavioral response (audio)
- `POST /sessions/{id}/end/` - End interview session

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Data Import

### 1. Prepare Your Data

Follow the schemas in `data_preprocessing_schemas.md` to format your datasets.

### 2. Import Questions

```bash
# Import LeetCode questions
curl -X POST "http://localhost:8000/questions/import/leetcode/" \
  -H "Content-Type: application/json" \
  -d @processed_leetcode_data.json

# Import System Design questions
curl -X POST "http://localhost:8000/questions/import/system-design/" \
  -H "Content-Type: application/json" \
  -d @processed_system_design_data.json

# Import Behavioral questions
curl -X POST "http://localhost:8000/questions/import/behavioral/" \
  -H "Content-Type: application/json" \
  -d @processed_behavioral_data.json
```

## Usage Examples

### 1. Create an Interview

```python
import requests

# Create interview
interview_data = {
    "user_id": 1,
    "interview_type": "mixed",
    "title": "Software Engineer Interview",
    "description": "Technical and behavioral assessment"
}

response = requests.post("http://localhost:8000/interviews/", json=interview_data)
interview_id = response.json()["id"]
```

### 2. Start Technical Session

```python
# Start technical session
session_data = {"session_type": "technical"}
response = requests.post(f"http://localhost:8000/interviews/{interview_id}/sessions/", json=session_data)
session_id = response.json()["session_id"]
```

### 3. Get Next Question

```python
# Get next question
response = requests.get(f"http://localhost:8000/sessions/{session_id}/questions/next/")
question = response.json()
```

### 4. Submit Technical Response

```python
# Submit code solution
response_data = {
    "question_id": question["question_id"],
    "user_id": 1,
    "code_response": "def twoSum(nums, target):\n    # Your solution here",
    "time_taken": 180.5
}

response = requests.post(f"http://localhost:8000/sessions/{session_id}/responses/technical/", data=response_data)
score = response.json()["score"]
```

### 5. Submit Behavioral Response

```python
# Submit audio response
with open("audio_response.wav", "rb") as audio_file:
    files = {"audio_file": audio_file}
    data = {
        "question_id": question_id,
        "user_id": 1
    }
    response = requests.post(f"http://localhost:8000/sessions/{session_id}/responses/behavioral/", 
                           files=files, data=data)
```

## Development

### Project Structure

The system is designed with modularity in mind:

- **Core Modules**: Handle business logic and external integrations
- **Models**: Define database structure and relationships
- **Schemas**: Validate API requests and responses
- **API Layer**: RESTful endpoints for frontend integration

### Adding New Features

1. **New Question Types**: Extend `QuestionType` enum and add corresponding schemas
2. **New Scoring Criteria**: Modify `ScoringEngine` class
3. **New AI Features**: Extend `AIService` class
4. **New Audio Processing**: Extend `AudioProcessor` class

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## Configuration

### Scoring Weights

Modify weights in `config.py`:

```python
# Technical scoring weights
TECHNICAL_ACCURACY_WEIGHT = 0.5
TECHNICAL_TIME_WEIGHT = 0.2
TECHNICAL_OPTIMALITY_WEIGHT = 0.2
TECHNICAL_PROCESS_WEIGHT = 0.1

# Behavioral scoring weights
BEHAVIORAL_CHATGPT_WEIGHT = 0.8
BEHAVIORAL_TONE_WEIGHT = 0.2
```

### Audio Processing

Supported formats: `.wav`, `.mp3`, `.m4a`, `.flac`

Maximum file size: 50MB (configurable)

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**: Check your API key and quota
2. **Audio Processing Failures**: Ensure audio file is valid and supported format
3. **Database Errors**: Check database connection and permissions
4. **Import Failures**: Validate JSON format against schemas

### Logs

Check application logs for detailed error information:

```bash
# View logs
tail -f logs/app.log
```

## Contributing

1. Follow the modular architecture
2. Add appropriate tests for new features
3. Update documentation
4. Use type hints and docstrings
5. Follow PEP 8 style guidelines

## License

This project is part of the CIC-GenAI-Hackathon.

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository.
