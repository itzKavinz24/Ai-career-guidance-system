import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { startQuiz, submitAnswer } from '../services/api';

const Quiz = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [state, setState] = useState(null);
  const [question, setQuestion] = useState(null);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const skills = useMemo(() => location.state?.skills || [], [location.state?.skills]);
  const domain = location.state?.domain || '';
  const assessmentScores = useMemo(() => location.state?.assessmentScores || {}, [location.state?.assessmentScores]);

  useEffect(() => {
    const initialize = async () => {
      if (!skills || skills.length === 0) {
        navigate('/skills');
        return;
      }

      setLoading(true);
      setError('');
      try {
        const response = await startQuiz(skills, domain || 'general', assessmentScores);
        setState(response.state || null);
        setQuestion(response.question || null);
      } catch (e) {
        setError('Failed to load quiz questions. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    initialize();
  }, [skills, domain, navigate, assessmentScores]);

  const handleQuizEnd = (finalCorrect, finalAnswered, finalState = null) => {
    const quizScore = finalCorrect * 20;
    const currentScores = finalState?.skill_scores || state?.skill_scores || {};
    navigate('/results', {
      state: {
        skills,
        domain,
        quizScore,
        totalQuestions: Math.max(finalAnswered, 1),
        currentScores,
      },
    });
  };

  const handleAnswerClick = async (selectedAnswer) => {
    if (!state || !question || submitting) {
      return;
    }

    setSubmitting(true);
    setError('');
    try {
      const response = await submitAnswer(state, selectedAnswer);
      const nextAnsweredCount = answeredCount + 1;
      const nextCorrectCount = correctCount + (response.is_correct ? 1 : 0);

      setAnsweredCount(nextAnsweredCount);
      setCorrectCount(nextCorrectCount);
      setState(response.state || null);

      if (response.quiz_complete || !response.question) {
        handleQuizEnd(nextCorrectCount, nextAnsweredCount, response.state || null);
        return;
      }

      setQuestion(response.question);
    } catch (e) {
      setError('Failed to submit answer. Please retry.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="text-center py-10">Loading quiz...</div>;
  }

  if (error && !question) {
    return (
      <div className="card-surface p-8 text-center space-y-4">
        <p className="text-red-600">{error}</p>
        <button className="btn-primary" onClick={() => navigate('/skills')}>
          Back to Skills
        </button>
      </div>
    );
  }

  if (!question) {
    return <div className="text-center py-10">No question available.</div>;
  }

  const options = Array.isArray(question.options) ? question.options : [];
  const totalQuestions = Math.max(skills.length * 3, answeredCount + 1);
  const progress = ((answeredCount + 1) / totalQuestions) * 100;

  return (
    <div className="space-y-8">
      <section className="card-surface glow-ring p-8 relative overflow-hidden">
        <div className="pointer-events-none absolute -top-10 right-10 h-28 w-28 rounded-full bg-blue-300/30 blur-2xl" />
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="headline-display text-3xl font-bold text-gray-900">Career Aptitude Quiz</h1>
            <p className="text-gray-600 mt-1">Question {answeredCount + 1}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-semibold text-blue-600">{Math.min(100, Math.round(progress))}%</p>
            <p className="text-xs text-gray-500">Complete</p>
          </div>
        </div>

        <div className="w-full bg-indigo-100 rounded-full h-2.5">
          <div
            className="bg-gradient-to-r from-blue-600 via-indigo-500 to-teal-400 h-2.5 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, progress)}%` }}
          />
        </div>
      </section>

      <section className="card-surface p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">{question.question}</h2>

        <div className="grid gap-3">
          {options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerClick(option)}
              disabled={submitting}
              className="text-left p-4 rounded-xl border border-indigo-100 bg-white/75 hover:border-blue-400 hover:bg-blue-50/70 hover:-translate-y-0.5 hover:shadow-md transition-all duration-300 disabled:opacity-50"
            >
              <span className="text-lg font-medium text-gray-900">{option}</span>
            </button>
          ))}
        </div>
      </section>

      {error && (
        <section className="card-surface p-4 text-center">
          <p className="text-red-600">{error}</p>
        </section>
      )}
    </div>
  );
};

export default Quiz;
