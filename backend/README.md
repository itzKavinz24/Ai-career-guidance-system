# AI Career Guidance Backend

Backend API for the AI Career Guidance application built with Flask.

## Folder Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── routes/               # API endpoints
│   ├── input.py         # User input routes
│   ├── quiz.py          # Quiz management routes
│   ├── evaluate.py      # Evaluation routes
│   └── match.py         # Career matching routes
├── services/            # Business logic
│   ├── quiz_engine.py   # Quiz logic
│   ├── question_generator.py # Local question generation
│   ├── scoring.py       # Scoring logic
│   ├── matcher.py       # Career matching logic
│   └── trends.py        # Market trends and insights
├── data/               # Data files
│   ├── careers.json    # Career database
│   └── questions.json  # Quiz questions
└── db/                 # Database
    ├── database.db     # SQLite database
    └── init_db.py      # Database initialization
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python db/init_db.py
```

### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Input Routes (`/api/input`)

- `POST /skills` - Submit user skills
- `POST /interests` - Submit user interests
- `POST /profile` - Create user profile

### Quiz Routes (`/api/quiz`)

- `POST /start` - Start a quiz
- `POST /submit-answer` - Submit quiz answer
- `GET /get-question/<question_id>` - Get specific question
- `POST /end` - End quiz and get results

### Evaluation Routes (`/api/evaluate`)

- `POST /skills` - Evaluate skills
- `POST /quiz-performance` - Evaluate quiz performance
- `POST /overall-assessment` - Generate overall assessment
- `POST /strengths-weaknesses` - Analyze strengths and weaknesses

### Match Routes (`/api/match`)

- `POST /careers` - Get career matches
- `GET /career-details/<career_id>` - Get career details
- `POST /compatibility-score` - Calculate compatibility
- `GET /trending-careers` - Get trending careers
- `GET /growth-opportunities/<career_id>` - Get growth opportunities
- `GET /salary-trends/<career_id>` - Get salary trends

## Configuration

Create a `.env` file in the backend directory:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///db/database.db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

## Services Overview

### Quiz Engine

Manages quiz questions, answers, and results calculation.

### Scoring

Evaluates skills, quiz performance, and generates overall assessments.

### Matcher

Matches user profiles to suitable careers based on skills and interests.

### Trends

Provides market trends, salary data, and growth opportunities.

### Question Generation

- **Question Generator**: Uses Groq API when configured, with local fallback

## Data Files

### careers.json

Contains comprehensive career information including:

- Job description
- Required skills
- Salary information
- Growth rate and outlook
- Specializations and advancement paths

### questions.json

Contains quiz questions with:

- Question text
- Multiple choice options
- Correct answer
- Topic and difficulty level
- Explanations

## Development Notes

- The backend uses SQLite for simplicity in development
- For production, consider upgrading to PostgreSQL
- Question generation is local and does not require external AI services
- All routes include error handling and validation

## Future Enhancements

- Advanced analytics and reporting
- User authentication and authorization
- Caching layer for performance optimization
- WebSocket support for real-time updates
