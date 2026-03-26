# Complete Project Structure

This file documents the complete structure of the AI Career Guidance application.

## Directory Tree

```
ai-career-guidance/
│
├── 📄 QUICKSTART.md                 ← START HERE! How to run everything
├── 📄 INTEGRATION_GUIDE.md          ← Architecture & API details
├── 📄 CONNECTION_STATUS.md          ← Status & checklist
├── 📄 .gitignore                    ← Git ignore rules
│
├── backend/                         ← Flask REST API (Port 5000)
│   ├── 📄 app.py                   ← Main Flask application
│   ├── 📄 requirements.txt          ← Python dependencies
│   ├── 📄 README.md                ← Backend documentation
│   ├── 📄 .env.example             ← Environment template
│   │
│   ├── routes/                     ← API Endpoints
│   │   ├── 📄 __init__.py
│   │   ├── 📄 input.py             ← User input endpoints
│   │   ├── 📄 quiz.py              ← Quiz endpoints
│   │   ├── 📄 evaluate.py          ← Assessment endpoints
│   │   └── 📄 match.py             ← Career matching endpoints
│   │
│   ├── services/                   ← Business Logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 quiz_engine.py       ← Quiz management
│   │   ├── 📄 scoring.py           ← Scoring logic
│   │   ├── 📄 matcher.py           ← Career matching
│   │   └── 📄 trends.py            ← Market trends
│   │
│   ├── llm/                        ← AI Integrations
│   │   ├── 📄 __init__.py
│   │   ├── 📄 question_generator.py ← Generate questions
│   │   └── 📄 explanation.py       ← Generate explanations
│   │
│   ├── data/                       ← Static Data
│   │   ├── 📄 __init__.py
│   │   ├── 📄 careers.json         ← 5 sample careers
│   │   └── 📄 questions.json       ← 10 sample questions
│   │
│   └── db/                         ← Database
│       ├── 📄 __init__.py
│       ├── 📄 init_db.py           ← Database initialization
│       └── 📄 database.db          ← SQLite database (created at runtime)
│
└── frontend/                        ← React App (Port 3000)
    ├── public/
    │   └── 📄 index.html           ← HTML entry point
    │
    ├── src/
    │   ├── 📄 index.js             ← React entry point
    │   ├── 📄 App.jsx              ← Main app component with routing
    │   ├── 📄 App.css              ← Page-specific styles
    │   ├── 📄 index.css            ← Global styles
    │   │
    │   ├── components/             ← Reusable Components
    │   │   ├── 📄 Navbar.jsx       ← Navigation bar
    │   │   ├── 📄 Navbar.css       ← Navbar styles
    │   │   ├── 📄 Card.jsx         ← Reusable card component
    │   │   ├── 📄 Card.css         ← Card styles
    │   │   ├── 📄 Chart.jsx        ← Data visualization
    │   │   └── 📄 Chart.css        ← Chart styles
    │   │
    │   ├── pages/                  ← Page Components
    │   │   ├── 📄 Home.jsx         ← Home page (trending careers)
    │   │   ├── 📄 SkillInput.jsx   ← Skills input page
    │   │   ├── 📄 Quiz.jsx         ← Quiz page
    │   │   ├── 📄 Results.jsx      ← Results page
    │   │   └── 📄 Details.jsx      ← Career details page
    │   │
    │   └── services/               ← API Layer
    │       └── 📄 api.js           ← All API calls
    │
    ├── 📄 package.json             ← Dependencies & scripts
    ├── 📄 .env                     ← Environment variables
    ├── 📄 .env.example             ← Environment template
    └── 📄 README.md                ← Frontend documentation
```

## File Descriptions

### Root Files

| File                   | Purpose                            |
| ---------------------- | ---------------------------------- |
| `QUICKSTART.md`        | Step-by-step guide to run the app  |
| `INTEGRATION_GUIDE.md` | Deep dive into architecture        |
| `CONNECTION_STATUS.md` | Integration status & checklist     |
| `.gitignore`           | Git ignore rules for both projects |

### Backend Files

#### Core

| File               | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| `app.py`           | Flask app initialization, blueprints, CORS config |
| `requirements.txt` | Python dependencies (Flask, CORS, etc.)           |
| `README.md`        | Backend documentation                             |

#### Routes (API Endpoints)

| File                 | Endpoints                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------- |
| `routes/input.py`    | `/input/skills`, `/input/interests`, `/input/profile`                                        |
| `routes/quiz.py`     | `/quiz/start`, `/quiz/submit-answer`, `/quiz/end`                                            |
| `routes/evaluate.py` | `/evaluate/skills`, `/evaluate/quiz-performance`, `/evaluate/overall-assessment`             |
| `routes/match.py`    | `/match/careers`, `/match/career-details`, `/match/trending-careers`, `/match/salary-trends` |

#### Services (Business Logic)

| File                      | Functions                                        |
| ------------------------- | ------------------------------------------------ |
| `services/quiz_engine.py` | Quiz question management, answer validation      |
| `services/scoring.py`     | Skill evaluation, score calculation, assessment  |
| `services/matcher.py`     | Career matching, compatibility scoring           |
| `services/trends.py`      | Market trends, salary data, growth opportunities |

#### LLM (AI Integration)

| File                        | Purpose                               |
| --------------------------- | ------------------------------------- |
| `llm/question_generator.py` | Generate custom quiz questions        |
| `llm/explanation.py`        | Generate AI explanations and insights |

#### Data

| File                  | Contents                            |
| --------------------- | ----------------------------------- |
| `data/careers.json`   | 5 sample careers with detailed info |
| `data/questions.json` | 10 sample quiz questions            |

#### Database

| File             | Purpose                              |
| ---------------- | ------------------------------------ |
| `db/init_db.py`  | Database schema initialization       |
| `db/database.db` | SQLite database (created at runtime) |

### Frontend Files

#### Entry Points

| File                | Purpose                        |
| ------------------- | ------------------------------ |
| `public/index.html` | HTML entry point               |
| `src/index.js`      | React app initialization       |
| `src/App.jsx`       | Main app component with routes |

#### Components

| File                    | Purpose                            |
| ----------------------- | ---------------------------------- |
| `components/Navbar.jsx` | Navigation with React Router links |
| `components/Card.jsx`   | Reusable card for displaying data  |
| `components/Chart.jsx`  | Bar chart for compatibility scores |

#### Pages

| File                   | Purpose        | Features                             |
| ---------------------- | -------------- | ------------------------------------ |
| `pages/Home.jsx`       | Home page      | Trending careers, API status         |
| `pages/SkillInput.jsx` | Skills input   | Add/remove skills, submit to API     |
| `pages/Quiz.jsx`       | Quiz page      | Load questions, track answers, score |
| `pages/Results.jsx`    | Results page   | Show matches, chart, compatibility   |
| `pages/Details.jsx`    | Career details | Full career info, salary, growth     |

#### Services

| File              | Purpose                               |
| ----------------- | ------------------------------------- |
| `services/api.js` | Central API client with 20+ functions |

#### Styles

| File               | Applies To           |
| ------------------ | -------------------- |
| `index.css`        | Global styles        |
| `App.css`          | Page-specific styles |
| `components/*.css` | Component styles     |

#### Configuration

| File           | Purpose                                 |
| -------------- | --------------------------------------- |
| `package.json` | Dependencies: React, React Router, etc. |
| `.env`         | API URL & environment config            |

## Data Flow

### Example: Skills Submission

```
User adds skill "Python"
         ↓
SkillInput.jsx state updated
         ↓
User clicks "Submit Skills"
         ↓
handleSubmitSkills() called
         ↓
await api.submitSkills(skills)
         ↓
fetch POST to /api/input/skills
         ↓
Backend receives request
         ↓
input.py: submit_skills()
         ↓
Validate & process skills
         ↓
Also call: api.evaluateSkills()
         ↓
evaluate.py: evaluate_skills()
         ↓
scoring.py: evaluate_skill_set()
         ↓
Return proficiency scores
         ↓
Display success message & scores
```

## API Endpoints

### Input Routes

```
POST /api/input/skills
POST /api/input/interests
POST /api/input/profile
```

### Quiz Routes

```
POST /api/quiz/start
POST /api/quiz/submit-answer
GET  /api/quiz/get-question/<id>
POST /api/quiz/end
```

### Evaluation Routes

```
POST /api/evaluate/skills
POST /api/evaluate/quiz-performance
POST /api/evaluate/overall-assessment
POST /api/evaluate/strengths-weaknesses
```

### Match Routes

```
POST /api/match/careers
GET  /api/match/career-details/<id>
POST /api/match/compatibility-score
GET  /api/match/trending-careers
GET  /api/match/growth-opportunities/<id>
GET  /api/match/salary-trends/<id>
```

## Technology Stack

### Backend

- **Framework:** Flask
- **Database:** SQLite
- **CORS:** Flask-CORS
- **Language:** Python 3.7+

### Frontend

- **Framework:** React 18
- **Router:** React Router 6
- **Bundler:** Create React App
- **Language:** JavaScript/JSX

### Communication

- **Protocol:** HTTP/REST
- **Format:** JSON
- **Port:** 5000 (backend), 3000 (frontend)

## How to Navigate

1. **Want to run the app?** → Read `QUICKSTART.md`
2. **Want to understand architecture?** → Read `INTEGRATION_GUIDE.md`
3. **Want to modify backend?** → See `backend/README.md`
4. **Want to modify frontend?** → See `frontend/README.md`
5. **Want to check status?** → See `CONNECTION_STATUS.md`

## Key Files to Modify

### To Add a New Career

Edit: `backend/data/careers.json`

### To Add Quiz Questions

Edit: `backend/data/questions.json`

### To Add a New Page

1. Create: `frontend/src/pages/NewPage.jsx`
2. Add route in: `frontend/src/App.jsx`
3. Add link in: `frontend/src/components/Navbar.jsx`

### To Add a New API Endpoint

1. Create route in: `backend/routes/new_routes.py`
2. Register in: `backend/app.py`
3. Add function in: `frontend/src/services/api.js`

## Statistics

| Metric              | Count   |
| ------------------- | ------- |
| Backend Files       | 20+     |
| Frontend Files      | 20+     |
| Documentation       | 4 files |
| API Endpoints       | 20+     |
| Database Tables     | 7       |
| Sample Careers      | 5       |
| Sample Questions    | 10      |
| Total Lines of Code | 5000+   |

## Configuration Files

### Backend (.env)

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///db/database.db
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

## Ports & URLs

| Service        | URL                          | Port |
| -------------- | ---------------------------- | ---- |
| Frontend       | http://localhost:3000        | 3000 |
| Backend API    | http://localhost:5000        | 5000 |
| Backend Health | http://localhost:5000/health | 5000 |

## Getting Started

1. Read: `QUICKSTART.md` (5 min read)
2. Run: `python app.py` in backend/
3. Run: `npm start` in frontend/
4. Open: http://localhost:3000
5. Check: "API Status: ✓ Connected"

---

**Complete, documented, and ready to use!** 🚀
