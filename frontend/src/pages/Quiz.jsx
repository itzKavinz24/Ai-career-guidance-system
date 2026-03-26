import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const mockQuestions = [
  {
    id: 1,
    question: 'What motivates you most in a career?',
    options: ['Problem-solving', 'Creative expression', 'Helping others', 'Financial success'],
  },
  {
    id: 2,
    question: 'How do you prefer to work?',
    options: ['Independently', 'In a team', 'With mentorship', 'Leading others'],
  },
  {
    id: 3,
    question: 'What is your biggest strength?',
    options: ['Technical skills', 'Communication', 'Analytical thinking', 'Leadership'],
  },
  {
    id: 4,
    question: 'What aspect of work do you enjoy most?',
    options: ['Building things', 'Analyzing data', 'Teaching others', 'Managing projects'],
  },
  {
    id: 5,
    question: 'How do you handle challenges?',
    options: ['Break down and solve', 'Seek help', 'Iterate quickly', 'Plan thoroughly'],
  },
];

const Quiz = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [questions] = useState(mockQuestions);
  const [loading, setLoading] = useState(false);

  const skills = useMemo(() => location.state?.skills || [], [location.state?.skills]);
  const domain = location.state?.domain || '';

  useEffect(() => {
    if (!skills || skills.length === 0) {
      navigate('/skills');
    }
  }, [skills, navigate]);

  const handleAnswerClick = (selectedIndex) => {
    // Calculate score based on answer
    if (selectedIndex === 0) {
      setScore((prev) => prev + 20);
    }

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      handleQuizEnd();
    }
  };

  const handleQuizEnd = async () => {
    setLoading(true);
    // Simulate quiz completion
    await new Promise((resolve) => setTimeout(resolve, 500));
    
    navigate('/results', {
      state: {
        skills,
        domain,
        quizScore: score,
        totalQuestions: questions.length,
      },
    });
  };

  if (questions.length === 0) {
    return <div className="text-center py-10">Loading quiz...</div>;
  }

  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="space-y-8">
      <section className="card-surface p-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="headline-display text-3xl font-bold text-gray-900">Career Aptitude Quiz</h1>
            <p className="text-gray-600 mt-1">Question {currentQuestion + 1} of {questions.length}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-semibold text-blue-600">{Math.round(progress)}%</p>
            <p className="text-xs text-gray-500">Complete</p>
          </div>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-gradient-to-r from-blue-500 to-cyan-400 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </section>

      <section className="card-surface p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">{currentQ.question}</h2>

        <div className="grid gap-3">
          {currentQ.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerClick(index)}
              disabled={loading}
              className="text-left p-4 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all duration-200 disabled:opacity-50"
            >
              <span className="text-lg font-medium text-gray-900">{option}</span>
            </button>
          ))}
        </div>
      </section>

      {loading && (
        <section className="card-surface p-8 text-center">
          <p className="text-gray-600">Analyzing your responses...</p>
        </section>
      )}
    </div>
  );
};

export default Quiz;
