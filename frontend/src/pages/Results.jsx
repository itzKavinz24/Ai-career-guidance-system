import React, { useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const mockCareers = [
  {
    id: 'ai-engineer',
    name: 'AI Engineer',
    description: 'Design and deploy intelligent systems',
    icon: '🤖',
    match: 92,
  },
  {
    id: 'data-scientist',
    name: 'Data Scientist',
    description: 'Extract insights from data',
    icon: '📊',
    match: 88,
  },
  {
    id: 'fullstack-dev',
    name: 'Full‑Stack Developer',
    description: 'Build complete web applications',
    icon: '💻',
    match: 85,
  },
  {
    id: 'security-analyst',
    name: 'Security Analyst',
    description: 'Protect systems and networks',
    icon: '🔐',
    match: 78,
  },
  {
    id: 'product-manager',
    name: 'Product Manager',
    description: 'Lead product strategy and vision',
    icon: '📱',
    match: 82,
  },
  {
    id: 'ux-designer',
    name: 'UX Designer',
    description: 'Create beautiful user experiences',
    icon: '🎨',
    match: 79,
  },
];

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const skills = useMemo(() => location.state?.skills || [], [location.state?.skills]);
  const domain = location.state?.domain || 'General';
  const quizScore = location.state?.quizScore || 0;
  const totalQuestions = location.state?.totalQuestions || 5;

  const percentage = Math.round((quizScore / (totalQuestions * 20)) * 100) || 0;

  // Sort careers by match score
  const topCareers = useMemo(() => {
    return [...mockCareers].sort((a, b) => b.match - a.match);
  }, []);

  return (
    <div className="space-y-12">
      {/* Summary Card */}
      <section className="card-surface p-8 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="headline-display text-3xl font-bold text-gray-900 mb-2">
              Your Career Results 🎉
            </h1>
            <p className="text-gray-600">Based on your skills and quiz answers</p>
          </div>
          <div className="text-right">
            <p className="text-5xl font-bold text-blue-600">{percentage}%</p>
            <p className="text-sm text-gray-600 mt-1">Match Score</p>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-3 gap-4">
          <div className="rounded-lg bg-white/80 p-3 border border-blue-200">
            <p className="text-xs text-gray-600 font-semibold">SKILLS PROVIDED</p>
            <p className="text-lg font-bold text-gray-900 mt-1">{skills.length}</p>
          </div>
          <div className="rounded-lg bg-white/80 p-3 border border-blue-200">
            <p className="text-xs text-gray-600 font-semibold">INTEREST AREA</p>
            <p className="text-sm font-bold text-gray-900 mt-1 truncate">{domain}</p>
          </div>
          <div className="rounded-lg bg-white/80 p-3 border border-blue-200">
            <p className="text-xs text-gray-600 font-semibold">READINESS</p>
            <p className="text-lg font-bold text-gray-900 mt-1">
              {percentage >= 80 ? '✨ High' : percentage >= 60 ? '🌱 Medium' : '🚀 Emerging'}
            </p>
          </div>
        </div>
      </section>

      {/* Top Matches */}
      <section>
        <div className="mb-6">
          <h2 className="section-title">Best Career Matches</h2>
          <p className="section-subtitle mt-2">Ranked by compatibility with your profile</p>
        </div>

        <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {topCareers.map((career) => (
            <div
              key={career.id}
              className="bg-white rounded-xl shadow-md hover:shadow-lg hover:scale-105 transition-transform duration-300 border border-gray-200 p-6 cursor-pointer"
              onClick={() => navigate(`/career/${career.id}`, { state: { skills, domain } })}
            >
              <div className="flex items-start justify-between mb-4">
                <span className="text-4xl">{career.icon}</span>
                <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-3 py-1 border border-blue-100">
                  <span className="text-sm font-bold text-blue-700">{career.match}%</span>
                </span>
              </div>
              <h3 className="text-lg font-bold text-blue-700">{career.name}</h3>
              <p className="text-sm text-gray-600 mt-2">{career.description}</p>
              <button className="mt-4 w-full py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-sm font-semibold text-gray-700 transition">
                View Details →
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Skills Summary */}
      {skills.length > 0 && (
        <section className="card-surface p-6">
          <h3 className="font-bold text-gray-900 mb-4">Your Skills</h3>
          <div className="flex flex-wrap gap-2">
            {skills.map((skill) => (
              <span key={skill} className="tag">{skill}</span>
            ))}
          </div>
        </section>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          type="button"
          className="btn-secondary flex-1"
          onClick={() => navigate('/skills')}
        >
          ← Retake Assessment
        </button>
        <button
          type="button"
          className="btn-primary flex-1"
          onClick={() => navigate('/')}
        >
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default Results;
