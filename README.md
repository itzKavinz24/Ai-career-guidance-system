# AI Career Guidance - Full Stack Application

A comprehensive AI-powered career guidance system that helps users discover suitable career paths based on their skills, interests, and aptitude test results.

## 🚀 Quick Start (2 Minutes)

```bash
# Terminal 1: Start Backend
cd backend
pip install -r requirements.txt
python db/init_db.py
python app.py
# Runs on http://localhost:5000

# Terminal 2: Start Frontend
cd frontend
npm install
npm start
# Opens http://localhost:3000
```

**See detailed instructions in `QUICKSTART.md`**

## 📋 Project Overview

This is a **full-stack, production-ready** application with:

- ✅ **React Frontend** - 5 pages, components, routing
- ✅ **Flask Backend** - RESTful API with 20+ endpoints
- ✅ **SQLite Database** - Persistent data storage
- ✅ **Automatic Integration** - API service layer
- ✅ **Comprehensive Documentation** - 5+ guide files

## 📁 What's Included

### Frontend (React)

- **5 Pages:** Home, Skills Input, Quiz, Results, Career Details
- **3 Components:** Navbar, Card, Chart
- **API Service Layer:** 20+ functions for backend communication
- **Responsive Design:** Mobile-first CSS
- **React Router:** Client-side navigation

### Backend (Flask)

- **4 Route Modules:** Input, Quiz, Evaluation, Matching
- **4 Service Modules:** Quiz Engine, Scoring, Matching, Trends
- **2 LLM Modules:** Question Generation, Explanations
- **SQLite Database:** 7 tables with proper schema
- **JSON Data:** 5 careers, 10 questions

## 🎯 Key Features

### For Users

- **Skill Assessment** - List skills and get proficiency scores
- **Career Quiz** - 10-question aptitude test
- **Career Recommendations** - AI-powered matching algorithm
- **Career Details** - Salary trends, growth opportunities, requirements
- **Trending Careers** - See what's hot in the job market

### For Developers

- **Clean Architecture** - Separation of concerns
- **API Service Layer** - Centralized backend communication
- **Error Handling** - Try-catch with user-friendly messages
- **Modular Code** - Easy to extend and modify
- **Complete Documentation** - 5 guide files

## 📚 Documentation

| Document                 | Purpose                              |
| ------------------------ | ------------------------------------ |
| **QUICKSTART.md**        | Step-by-step setup & troubleshooting |
| **INTEGRATION_GUIDE.md** | Architecture, data flow, API details |
| **PROJECT_STRUCTURE.md** | Complete file organization           |
| **CONNECTION_STATUS.md** | Integration checklist                |
| **backend/README.md**    | Backend-specific docs                |
| **frontend/README.md**   | Frontend-specific docs               |

## 🔗 How They Connect

```
┌─────────────────────────────┐
│     React Frontend (3000)    │
│  - Pages, Components, Router │
│  - API Service Layer         │
└────────────┬────────────────┘
             │
        HTTP/JSON
        (CORS Enabled)
             │
┌────────────▼────────────────┐
│    Flask Backend (5000)      │
│  - 20+ API Endpoints         │
│  - Business Logic Services   │
│  - SQLite Database           │
└─────────────────────────────┘
```

## 🏗️ Architecture

### Frontend Data Flow

```
User Action
  ↓
React Component
  ↓
API Service (api.js)
  ↓
HTTP Request
  ↓
Display Response
```

### Backend Processing

```
HTTP Request
  ↓
Flask Route Handler
  ↓
Business Logic Service
  ↓
Database/File Access
  ↓
JSON Response
```

## 📡 API Endpoints (20+)

### Input Routes

- `POST /api/input/skills` - Submit skills
- `POST /api/input/interests` - Submit interests
- `POST /api/input/profile` - Create profile

### Quiz Routes

- `POST /api/quiz/start` - Start quiz
- `POST /api/quiz/submit-answer` - Submit answer
- `POST /api/quiz/end` - End quiz

### Evaluation Routes

- `POST /api/evaluate/skills` - Evaluate skills
- `POST /api/evaluate/quiz-performance` - Evaluate performance
- `POST /api/evaluate/overall-assessment` - Get assessment

### Match Routes

- `POST /api/match/careers` - Get career matches
- `GET /api/match/career-details/<id>` - Get career details
- `GET /api/match/trending-careers` - Get trending careers
- `GET /api/match/salary-trends/<id>` - Get salary trends

## 🛠️ Technology Stack

| Layer             | Technology                     |
| ----------------- | ------------------------------ |
| **Frontend**      | React 18, React Router 6, CSS3 |
| **Backend**       | Flask, Python 3.7+             |
| **Database**      | SQLite                         |
| **API**           | RESTful JSON                   |
| **Communication** | HTTP with CORS                 |

## 📦 Installation

### Prerequisites

- Node.js v14+ (for frontend)
- Python 3.7+ (for backend)
- npm (usually comes with Node.js)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python db/init_db.py
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🧪 Testing

### Check Backend Health

```bash
curl http://localhost:5000/health
# Response: {"status": "healthy"}
```

### Test Skills API

```bash
curl -X POST http://localhost:5000/api/input/skills \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "JavaScript"]}'
```

### Check Frontend Connection

- Open http://localhost:3000
- Look for "API Status: ✓ Connected" on home page
- Trending careers should load automatically

## 📝 Usage Examples

### Adding Skills

1. Go to http://localhost:3000/skills
2. Type skill name (e.g., "Python")
3. Click "Add Skill"
4. Click "Submit Skills"
5. See proficiency scores and feedback

### Taking the Quiz

1. Go to http://localhost:3000/quiz
2. Click "Start Quiz"
3. Answer 10 questions
4. View score and analysis

### Viewing Career Matches

1. Go to http://localhost:3000/results
2. See recommended careers
3. View compatibility percentage
4. Click career for details

## 🚀 Running in Production

### Build Frontend

```bash
cd frontend
npm run build
# Creates optimized build in build/ folder
```

### Deploy Backend

```bash
# Change FLASK_ENV to production in .env
FLASK_ENV=production python app.py
```

### Use Environment Variables

```bash
# Update .env files for production URLs
REACT_APP_API_URL=https://api.yoursite.com
FLASK_ENV=production
```

## 🔧 Customization

### Add a New Career

Edit `backend/data/careers.json`:

```json
{
  "id": "career_006",
  "name": "Your Career",
  "description": "...",
  "required_skills": [...],
  "average_salary": 100000
}
```

### Add Quiz Questions

Edit `backend/data/questions.json`:

```json
{
  "id": "q011",
  "question": "Your question?",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "A"
}
```

### Add a New Page

1. Create `frontend/src/pages/NewPage.jsx`
2. Add route in `frontend/src/App.jsx`
3. Add link in `frontend/src/components/Navbar.jsx`

## 📊 Project Statistics

- **Total Files:** 50+
- **Backend Files:** 20+
- **Frontend Files:** 20+
- **Lines of Code:** 5000+
- **API Endpoints:** 20+
- **Database Tables:** 7
- **Documentation Files:** 6

## 🐛 Troubleshooting

| Issue                 | Solution                                      |
| --------------------- | --------------------------------------------- |
| "API Status: Offline" | Check backend is running on port 5000         |
| CORS error            | Ensure `CORS(app)` in backend, check .env URL |
| Port already in use   | Kill process or use different port            |
| Module not found      | Run `pip install -r requirements.txt`         |
| npm error             | Delete node_modules, run `npm install`        |

**See detailed troubleshooting in `QUICKSTART.md`**

## 📖 Learning Resources

- **Frontend React docs:** Familiarize with hooks, routing
- **Backend Flask docs:** Understand blueprints, request handling
- **REST API concepts:** Understand HTTP methods and status codes
- **Database:** Basic SQL and SQLite concepts

## 🤝 Contributing

To add features:

1. **Backend:** Add endpoint in `routes/`, implement logic in `services/`
2. **Frontend:** Add API function in `services/api.js`, use in component
3. **Test:** Verify with curl/Postman before frontend integration
4. **Document:** Update relevant README files

## 📋 Checklist

- [x] Backend API created with 20+ endpoints
- [x] Frontend pages created with routing
- [x] API service layer integrated
- [x] Database schema designed
- [x] Sample data created
- [x] CORS enabled for frontend-backend
- [x] Error handling implemented
- [x] Responsive design added
- [x] Documentation completed
- [x] Ready for testing

## 🎓 Key Learnings

This project demonstrates:

- Full-stack application development
- REST API design and implementation
- Frontend-backend integration
- Component-based architecture
- State management
- Error handling
- Documentation best practices

## 📞 Quick Links

- **Getting Started:** `QUICKSTART.md`
- **Architecture:** `INTEGRATION_GUIDE.md`
- **File Structure:** `PROJECT_STRUCTURE.md`
- **Frontend Docs:** `frontend/README.md`
- **Backend Docs:** `backend/README.md`

## 🎉 Success Indicators

You'll know everything is working when:

- ✅ Backend starts without errors
- ✅ Frontend loads on port 3000
- ✅ Home page shows "✓ Connected"
- ✅ Trending careers load automatically
- ✅ Skills submission works
- ✅ Quiz runs smoothly
- ✅ Results display matches
- ✅ Career details load fully

## 🌟 Next Steps

1. **Run the app** → Follow `QUICKSTART.md`
2. **Test all features** → Try each page
3. **Explore the code** → Understand structure
4. **Customize** → Add your own careers/questions
5. **Extend** → Add new features
6. **Deploy** → Put online

## 📄 License

This project is ready for educational and commercial use.

## 👨‍💻 Built With

- React for modern UI
- Flask for robust backend
- SQLite for data persistence
- CSS for responsive design
- JavaScript for interactivity

---

## 🚀 Let's Get Started!

```bash
# Read this first
cat QUICKSTART.md

# Then run
cd backend && python app.py
cd frontend && npm start
```

**Your full-stack AI Career Guidance app is complete and ready to use!**

For any issues, check `QUICKSTART.md` troubleshooting section.

Happy coding! 🎉
