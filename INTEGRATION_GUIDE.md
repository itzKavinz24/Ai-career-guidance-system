# Frontend-Backend Integration Guide

This document explains how the frontend and backend are connected in the AI Career Guidance application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        React Frontend                        │
│  (Port 3000 - http://localhost:3000)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Service Layer (api.js)              │  │
│  │  - Centralized API calls                             │  │
│  │  - Error handling & response parsing                 │  │
│  │  - Base URL configuration via .env                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              ↓
                         HTTP/REST
                    (CORS Enabled - Port 5000)
                              ↑
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend                           │
│  (Port 5000 - http://localhost:5000)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  API Routes                          │  │
│  │  - /api/input/*      (User input management)         │  │
│  │  - /api/quiz/*       (Quiz operations)               │  │
│  │  - /api/evaluate/*   (Assessment & scoring)          │  │
│  │  - /api/match/*      (Career matching)               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Business Logic Services                 │  │
│  │  - quiz_engine.py    (Quiz management)               │  │
│  │  - scoring.py        (Skill & assessment scoring)    │  │
│  │  - matcher.py        (Career matching logic)         │  │
│  │  - trends.py         (Market trends & data)          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Data Layer                         │  │
│  │  - SQLite Database (db/database.db)                  │  │
│  │  - JSON files (careers.json, questions.json)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## How They Connect

### 1. API Service Layer (Frontend)

The frontend uses a centralized API service (`src/services/api.js`) to communicate with the backend:

```javascript
// Example: Submitting skills
import * as api from "../services/api";

const response = await api.submitSkills(["Python", "JavaScript"]);
```

**Key Features:**

- Single base URL configuration
- Automatic JSON serialization/deserialization
- Consistent error handling
- Built-in fetch with standard headers

### 2. Backend API Routes

The backend exposes RESTful API endpoints through Flask blueprints:

**Structure:**

```
/api/
├── input/          # User input management
│   ├── POST /skills
│   ├── POST /interests
│   └── POST /profile
├── quiz/           # Quiz operations
│   ├── POST /start
│   ├── POST /submit-answer
│   ├── GET /get-question/<id>
│   └── POST /end
├── evaluate/       # Assessment
│   ├── POST /skills
│   ├── POST /quiz-performance
│   ├── POST /overall-assessment
│   └── POST /strengths-weaknesses
└── match/          # Career matching
    ├── POST /careers
    ├── GET /career-details/<id>
    ├── POST /compatibility-score
    ├── GET /trending-careers
    ├── GET /growth-opportunities/<id>
    └── GET /salary-trends/<id>
```

### 3. Data Flow Example: Skills Assessment

```
User Interface (SkillInput.jsx)
          ↓
User adds skills and clicks "Submit"
          ↓
handleSubmitSkills() in SkillInput.jsx
          ↓
api.submitSkills(skills) in api.js
          ↓
fetch('http://localhost:5000/api/input/skills', {
  method: 'POST',
  body: JSON.stringify({skills: ['Python', 'JavaScript']})
})
          ↓
Backend receives POST request
          ↓
input_routes.py → submit_skills()
          ↓
Validates and processes skills
          ↓
Returns JSON response
          ↓
Frontend receives response
          ↓
api.evaluateSkills() called automatically
          ↓
evaluate_routes.py → evaluate_skills()
          ↓
scoring.py → evaluate_skill_set()
          ↓
Returns evaluation scores
          ↓
Frontend displays results
```

## Configuration

### Frontend Configuration (.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

**How it's used:**

```javascript
// In api.js
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000/api";
```

### Backend Configuration (app.py)

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

**CORS Configuration:**

- Allows requests from `http://localhost:3000` (frontend)
- Supports standard HTTP methods (GET, POST, PUT, DELETE)
- Allows JSON content type

## Running Both Services

### Terminal 1: Start Backend

```bash
cd backend
python app.py
# Backend runs on http://localhost:5000
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

### Verification

1. **Backend Health Check:**
   - Open: `http://localhost:5000/health`
   - Should return: `{"status": "healthy"}`

2. **Frontend Status:**
   - Home page should show "API Status: ✓ Connected"
   - If offline, check console for errors

## Common Issues & Solutions

### Issue: CORS Error

**Problem:**

```
Access to XMLHttpRequest at 'http://localhost:5000/api/...'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**

1. Ensure backend has `CORS(app)` enabled
2. Check API URL in `.env` is correct
3. Restart backend server

### Issue: Connection Refused

**Problem:**

```
Failed to fetch from http://localhost:5000/api/...
```

**Solution:**

1. Verify backend is running: `http://localhost:5000/health`
2. Check port 5000 is not in use: `netstat -an | grep 5000`
3. Check firewall settings

### Issue: JSON Parse Error

**Problem:**

```
SyntaxError: Unexpected token < in JSON at position 0
```

**Solution:**

1. Backend might be returning HTML error page
2. Check backend logs for errors
3. Verify request body format matches API specification

### Issue: 404 Not Found

**Problem:**

```
404 - Not Found
```

**Solution:**

1. Check route path in backend
2. Verify HTTP method (GET vs POST)
3. Check blueprint is registered in app.py

## API Request/Response Examples

### Example 1: Submit Skills

**Request (Frontend):**

```javascript
const response = await api.submitSkills(["Python", "JavaScript"]);
```

**HTTP Request:**

```
POST /api/input/skills HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{"skills": ["Python", "JavaScript"]}
```

**HTTP Response:**

```json
{
  "message": "Skills received successfully",
  "skills": ["python", "javascript"],
  "count": 2
}
```

**Frontend Handling:**

```javascript
try {
  const response = await api.submitSkills(skills);
  console.log(`${response.count} skills submitted`);
} catch (error) {
  console.error("Error submitting skills:", error);
}
```

### Example 2: Get Career Matches

**Request (Frontend):**

```javascript
const matches = await api.getCareerMatches(
  "user123",
  ["Python", "Leadership"],
  ["Technology"],
  {},
);
```

**HTTP Request:**

```
POST /api/match/careers HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "user_id": "user123",
  "skills": ["Python", "Leadership"],
  "interests": ["Technology"],
  "assessment": {}
}
```

**HTTP Response:**

```json
{
  "message": "Career matches found",
  "user_id": "user123",
  "matches": [
    {
      "id": "career_001",
      "name": "Software Engineer",
      "compatibility_score": 85.5,
      "match_percentage": "85.5%"
    },
    {
      "id": "career_004",
      "name": "Cloud Solutions Architect",
      "compatibility_score": 78.2,
      "match_percentage": "78.2%"
    }
  ],
  "match_count": 2
}
```

## Development Workflow

### Adding a New Feature

1. **Backend:**
   - Create route in appropriate file in `routes/`
   - Implement business logic in `services/`
   - Test with curl or Postman

2. **Frontend:**
   - Add API function in `services/api.js`
   - Use in component with async/await
   - Add error handling

3. **Testing:**
   - Verify backend returns correct data
   - Check frontend receives and displays data
   - Test error scenarios

### Example: Adding Quiz Feature

**Backend (routes/quiz.py):**

```python
@bp.route('/get-questions', methods=['GET'])
def get_questions():
    limit = request.args.get('limit', 10, type=int)
    questions = quiz_engine.get_quiz_questions(num_questions=limit)
    return {'questions': questions}, 200
```

**Frontend (services/api.js):**

```javascript
export const getQuestions = (limit = 10) =>
  apiCall(`/quiz/get-questions?limit=${limit}`, "GET");
```

**Usage in Component:**

```javascript
const [questions, setQuestions] = useState([]);

useEffect(() => {
  const fetchQuestions = async () => {
    try {
      const response = await api.getQuestions(10);
      setQuestions(response.questions);
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };

  fetchQuestions();
}, []);
```

## Performance Optimization

### Frontend Optimizations

- Cache API responses in state
- Use React.memo for expensive components
- Lazy load pages with React.lazy
- Optimize bundle size with code splitting

### Backend Optimizations

- Add database indexes for frequent queries
- Implement caching for career data
- Use connection pooling for database
- Enable gzip compression

## Monitoring & Debugging

### Frontend Console

```javascript
// Enable API logging
const originalFetch = fetch;
window.fetch = function (...args) {
  console.log("API Request:", args[0]);
  return originalFetch.apply(this, args).then((response) => {
    console.log("API Response:", response.status);
    return response;
  });
};
```

### Backend Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug('Received request:', request.json)
logger.error('Error processing request:', str(error))
```

## Deployment

### Using Environment Variables

**Production .env:**

```env
REACT_APP_API_URL=https://api.yoursite.com
REACT_APP_ENV=production
```

**Backend Configuration:**

```python
import os
API_ENV = os.getenv('FLASK_ENV', 'development')
```

This comprehensive integration ensures smooth communication between the React frontend and Flask backend.
