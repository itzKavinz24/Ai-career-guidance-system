// services/api.js - API service for all backend communication

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000/api";

const QUIZ_BASE_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";

// Utility function for API calls with error handling
const apiCall = async (endpoint, method = "GET", data = null) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
};

const quizApiCall = async (endpoint, method = "GET", data = null) => {
  const url = `${QUIZ_BASE_URL}${endpoint}`;
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(
      `Quiz API Error: ${response.status} ${response.statusText}`,
    );
  }
  return response.json();
};

// Input Routes
export const submitSkills = (skills) =>
  apiCall("/input/skills", "POST", { skills });

export const submitInterests = (interests) =>
  apiCall("/input/interests", "POST", { interests });

export const createProfile = (name, skills, interests) =>
  apiCall("/input/profile", "POST", { name, skills, interests });

// Adaptive Quiz Routes (direct backend endpoints)
export const startQuiz = (skills = [], domain = "general") =>
  quizApiCall("/start-quiz", "POST", { skills, domain });

export const submitAnswer = (state, selectedAnswer) =>
  quizApiCall("/next-question", "POST", {
    state,
    selected_answer: selectedAnswer,
  });

// Evaluation Routes
export const evaluateSkills = (skills, userId) =>
  apiCall("/evaluate/skills", "POST", { skills, user_id: userId });

export const getSkillEvaluation = (jobId) =>
  apiCall(`/evaluate/skills/${jobId}`, "GET");

export const evaluateQuizPerformance = (userId, answers, timeTaken) =>
  apiCall("/evaluate/quiz-performance", "POST", {
    user_id: userId,
    answers,
    time_taken: timeTaken,
  });

export const getOverallAssessment = (
  userId,
  skillsScore,
  quizScore,
  interests,
) =>
  apiCall("/evaluate/overall-assessment", "POST", {
    user_id: userId,
    skills_score: skillsScore,
    quiz_score: quizScore,
    interests,
  });

export const analyzeStrengthsWeaknesses = (userId, skills, quizResults) =>
  apiCall("/evaluate/strengths-weaknesses", "POST", {
    user_id: userId,
    skills,
    quiz_results: quizResults,
  });

// Match Routes
export const getCareerMatches = (userId, skills, interests, assessment) =>
  apiCall("/match/careers", "POST", {
    user_id: userId,
    skills,
    interests,
    assessment,
  });

export const getCareerDetails = (careerId) =>
  apiCall(`/match/career-details/${careerId}`, "GET");

export const calculateCompatibility = (userId, careerId, profile) =>
  apiCall("/match/compatibility-score", "POST", {
    user_id: userId,
    career_id: careerId,
    profile,
  });

export const getTrendingCareers = (page = 1, limit = 10) =>
  apiCall(`/match/trending-careers?page=${page}&limit=${limit}`, "GET");

export const getGrowthOpportunities = (careerId) =>
  apiCall(`/match/growth-opportunities/${careerId}`, "GET");

export const getSalaryTrends = (careerId) =>
  apiCall(`/match/salary-trends/${careerId}`, "GET");

export const simulateWhatIf = (selectedSkill, currentScores, interests = []) =>
  quizApiCall("/simulate", "POST", {
    selected_skill: selectedSkill,
    current_scores: currentScores,
    interests,
  });

export const generateCareers = (skills, interests = [], topMatch = []) =>
  quizApiCall("/generate-careers", "POST", {
    skills,
    interests,
    top_match: topMatch,
  });

export const getCareerAnalysis = (skills) =>
  quizApiCall("/career-analysis", "POST", {
    skills,
  });

// Health check (direct backend call, outside /api routes)
export const checkHealth = async () => {
  try {
    const response = await fetch("http://localhost:5000/health", {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Health check error:", error);
    return { status: "offline", error: error.message };
  }
};
