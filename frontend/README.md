# AI Career Guidance - Frontend

A modern React-based frontend for the AI Career Guidance application. Helps users discover suitable career paths based on their skills, interests, and quiz performance.

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── components/
│   │   ├── Navbar.jsx      # Navigation component
│   │   ├── Navbar.css      # Navbar styles
│   │   ├── Card.jsx        # Reusable card component
│   │   ├── Card.css        # Card styles
│   │   ├── Chart.jsx       # Data visualization
│   │   └── Chart.css       # Chart styles
│   ├── pages/
│   │   ├── Home.jsx        # Home page
│   │   ├── SkillInput.jsx  # Skills input page
│   │   ├── Quiz.jsx        # Quiz page
│   │   ├── Results.jsx     # Results page
│   │   └── Details.jsx     # Career details page
│   ├── services/
│   │   └── api.js          # API service layer
│   ├── App.jsx             # Main app component
│   ├── App.css             # App styles
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── .env                    # Environment variables
├── package.json            # Dependencies
└── README.md               # This file
```

## Setup & Installation

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

The `REACT_APP_API_URL` should point to your backend API. For local development, it's typically `http://localhost:5000/api`.

### 3. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

## Features

### Pages

**Home**

- Displays trending careers
- Shows API connection status
- Quick navigation to key features

**Skills Input**

- Add and manage user skills
- Submit skills for evaluation
- Real-time skill assessment

**Quiz**

- Interactive career aptitude quiz
- Progress tracking
- Answer submission and explanation
- Score calculation

**Results**

- Career match recommendations
- Compatibility scores
- Chart visualization of matches
- Career comparison

**Career Details**

- Comprehensive career information
- Salary trends by experience level
- Growth opportunities and advancement paths
- Specializations and certifications
- Pros and cons analysis

## API Integration

The frontend communicates with the backend via the API service layer (`src/services/api.js`).

### API Endpoints Used

**Input Routes**

- `POST /input/skills` - Submit skills
- `POST /input/interests` - Submit interests
- `POST /input/profile` - Create user profile

**Quiz Routes**

- `POST /quiz/start` - Start a quiz
- `POST /quiz/submit-answer` - Submit quiz answer
- `GET /quiz/get-question/<id>` - Get specific question
- `POST /quiz/end` - End quiz

**Evaluation Routes**

- `POST /evaluate/skills` - Evaluate skills
- `POST /evaluate/quiz-performance` - Evaluate performance
- `POST /evaluate/overall-assessment` - Get assessment
- `POST /evaluate/strengths-weaknesses` - Analyze skills

**Match Routes**

- `POST /match/careers` - Get career matches
- `GET /match/career-details/<id>` - Get career details
- `POST /match/compatibility-score` - Calculate compatibility
- `GET /match/trending-careers` - Get trending careers
- `GET /match/growth-opportunities/<id>` - Get growth data
- `GET /match/salary-trends/<id>` - Get salary trends

## Components

### Navbar

Navigation component with links to all pages.

### Card

Reusable card component for displaying career information.

### Chart

Data visualization component displaying career compatibility scores.

## Styling

The application uses CSS with a mobile-first responsive design. Main style files:

- `index.css` - Global styles
- `App.css` - Page-specific styles
- Individual component CSS files

## Development

### Adding New Pages

1. Create a new file in `src/pages/`
2. Add the route in `src/App.jsx`
3. Add navigation link in `src/components/Navbar.jsx`

### Adding New API Calls

1. Add the function in `src/services/api.js`
2. Use the consistent `apiCall` pattern
3. Handle errors appropriately

### Styling New Components

Create a companion CSS file with the same name as the component.

## Environment Variables

- `REACT_APP_API_URL` - Backend API base URL (default: `http://localhost:5000/api`)
- `REACT_APP_ENV` - Environment type (development/production)

## Build for Production

```bash
npm run build
```

Creates an optimized production build in the `build/` directory.

## Troubleshooting

### API Connection Issues

- Ensure backend is running on `http://localhost:5000`
- Check the `.env` file for correct `REACT_APP_API_URL`
- Check browser console for CORS errors

### Port Already in Use

- Change port: `PORT=3001 npm start`

### Dependencies Issues

- Clear cache: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements

- User authentication and profiles
- Persistent local storage for user data
- Advanced filtering and search
- Video tutorials and learning resources
- Job listing integration
- Social sharing features
- PWA (Progressive Web App) support
