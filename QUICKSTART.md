# Quick Start Guide - Running Frontend & Backend Together

## Prerequisites

- **Node.js** (v14+) and npm installed
- **Python** (v3.7+) installed
- **pip** (Python package manager) installed

## Setup Instructions

### Step 1: Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python db/init_db.py
```

You should see:

```
Database initialized at db/database.db
```

### Step 2: Frontend Setup

Navigate to the frontend directory (in a new terminal):

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

This installs React, React Router, and other dependencies listed in `package.json`.

### Step 3: Configuration Check

**Frontend .env file** (`frontend/.env`):

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

**Backend CORS** (Already configured in `backend/app.py`):

```python
CORS(app)  # Allows requests from frontend
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**✓ Backend is running at:** `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

The browser will automatically open to:

**✓ Frontend is running at:** `http://localhost:3000`

## Testing the Connection

### Method 1: Web Browser

1. Open `http://localhost:3000` in your browser
2. Look at the **Home page**
3. You should see "API Status: ✓ Connected" in green
4. Trending careers should load automatically

### Method 2: Command Line

**Test Backend Health:**

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{ "status": "healthy" }
```

**Test Skills API:**

```bash
curl -X POST http://localhost:5000/api/input/skills \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "JavaScript"]}'
```

Expected response:

```json
{
  "message": "Skills received successfully",
  "skills": ["python", "javascript"],
  "count": 2
}
```

## Using the Application

### 1. Home Page

- View trending careers
- Check API connection status
- See sample career data

### 2. Skills Page

- Add your skills (e.g., "Python", "Leadership", "Data Analysis")
- Skills are automatically evaluated by the backend
- Get proficiency scores for each skill

### 3. Quiz Page

- Click "Start Quiz" to begin
- Answer career aptitude questions
- Get instant feedback after completion

### 4. Results Page

- View your quiz score
- See recommended careers based on your performance
- View career compatibility chart

### 5. Career Details

- Click on a recommended career
- View detailed career information
- See salary trends by experience level
- Review growth opportunities and specializations

## Troubleshooting

### "API Status: ✗ Offline"

**Check 1: Is backend running?**

```bash
curl http://localhost:5000/health
```

- If it fails, start the backend

**Check 2: Correct API URL?**

- Check `frontend/.env` has: `REACT_APP_API_URL=http://localhost:5000/api`
- Restart frontend after changing .env

**Check 3: CORS Issues?**

- Check browser console (F12 → Console tab)
- Look for CORS errors
- Ensure backend has `from flask_cors import CORS` and `CORS(app)`

### "Port 5000 already in use"

```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux

# Or use a different port
python app.py --port 5001
# Then update frontend .env to use that port
```

### "Dependencies not found"

**Backend:**

```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

**Frontend:**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Database errors"

```bash
cd backend
python db/init_db.py  # Reinitialize database
```

### "Port 3000 already in use"

```bash
# Use a different port
PORT=3001 npm start
```

## Project Structure

```
ai-career-guidance/
├── backend/
│   ├── app.py                 # Main Flask app
│   ├── requirements.txt       # Python dependencies
│   ├── routes/               # API endpoints
│   ├── services/             # Business logic
│   ├── data/                 # JSON data files
│   └── db/                   # Database files
│
└── frontend/
    ├── public/
    │   └── index.html        # HTML entry point
    ├── src/
    │   ├── components/       # React components
    │   ├── pages/            # Page components
    │   ├── services/         # API service layer
    │   ├── App.jsx           # Main app component
    │   └── index.js          # React entry point
    ├── package.json          # Node.js dependencies
    ├── .env                  # Environment variables
    └── README.md             # Frontend documentation
```

## Key URLs

| Service        | URL                          | Status        |
| -------------- | ---------------------------- | ------------- |
| Frontend       | http://localhost:3000        | Your app      |
| Backend API    | http://localhost:5000        | REST API      |
| Backend Health | http://localhost:5000/health | Health check  |
| API Base       | http://localhost:5000/api    | All endpoints |

## Common Tasks

### Clear Frontend Cache

```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Reset Database

```bash
cd backend
rm db/database.db
python db/init_db.py
```

### View Backend Logs

- Check terminal where `python app.py` is running
- All requests and errors are logged

### View Frontend Logs

- Open browser Developer Tools (F12)
- Go to Console tab
- All API calls and errors are logged

## Next Steps

1. **Explore the Application**
   - Test all pages and features
   - Try adding skills and taking the quiz

2. **Customize the Data**
   - Edit `backend/data/careers.json` to add more careers
   - Edit `backend/data/questions.json` to add more quiz questions

3. **Add New Features**
   - Create new API endpoints in `backend/routes/`
   - Create new pages in `frontend/src/pages/`
   - Add new API calls in `frontend/src/services/api.js`

4. **Deploy**
   - Build frontend: `npm run build`
   - Deploy to hosting (Vercel, Netlify)
   - Deploy backend to server (Heroku, AWS, GCP)

## Documentation

- **Integration Guide:** See `INTEGRATION_GUIDE.md`
- **Backend README:** See `backend/README.md`
- **Frontend README:** See `frontend/README.md`

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Look at console errors (F12 in browser)
3. Check backend terminal for errors
4. Review integration guide for architectural details

**Happy coding! 🚀**
