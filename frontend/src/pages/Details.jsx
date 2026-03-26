import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const mockCareerMeta = {
  'ai-engineer': {
    title: 'AI Engineer',
    description: 'Design and deploy ML systems that power intelligent products',
    icon: '🤖',
    salary: '$100k - $160k',
    skills: ['Python', 'Machine Learning', 'TensorFlow', 'Cloud'],
    roadmap: [
      'Master Python and data structures',
      'Complete ML fundamentals course',
      'Build 3 end-to-end projects',
      'Learn MLOps and deployment',
      'Contribute to open source',
    ],
  },
  'data-scientist': {
    title: 'Data Scientist',
    description: 'Turn data into actionable insights and models',
    icon: '📊',
    salary: '$95k - $150k',
    skills: ['Python', 'SQL', 'Statistics', 'Data Visualization'],
    roadmap: [
      'Master SQL and data cleaning',
      'Study statistics and probability',
      'Build 3 analysis projects',
      'Learn A/B testing',
      'Present insights effectively',
    ],
  },
  'fullstack-dev': {
    title: 'Full‑Stack Developer',
    description: 'Build complete applications from frontend to backend',
    icon: '💻',
    salary: '$90k - $140k',
    skills: ['JavaScript', 'React', 'Node.js', 'Databases'],
    roadmap: [
      'Master HTML, CSS, JavaScript',
      'Learn React framework',
      'Pick a backend stack',
      'Deploy to production',
      'Learn DevOps basics',
    ],
  },
  'security-analyst': {
    title: 'Security Analyst',
    description: 'Protect systems from threats and vulnerabilities',
    icon: '🔐',
    salary: '$85k - $135k',
    skills: ['Networking', 'Linux', 'Threat Detection', 'Security Tools'],
    roadmap: [
      'Learn networking fundamentals',
      'Study common vulnerabilities',
      'Practice using security tools',
      'Get Security+ certification',
      'Specialize in a domain',
    ],
  },
};

const Details = () => {
  const { careerID } = useParams();
  const navigate = useNavigate();

  const meta = mockCareerMeta[careerID] || mockCareerMeta['ai-engineer'];

  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="card-surface p-8 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
        <div className="flex items-start gap-4">
          <span className="text-6xl">{meta.icon}</span>
          <div className="flex-1">
            <h1 className="headline-display text-4xl font-bold text-gray-900">{meta.title}</h1>
            <p className="text-lg text-gray-600 mt-2">{meta.description}</p>
            <div className="flex gap-3 mt-4">
              <div className="rounded-lg bg-white/80 px-4 py-2 border border-blue-200">
                <p className="text-xs text-gray-600 font-semibold">SALARY RANGE</p>
                <p className="text-sm font-bold text-gray-900 mt-1">{meta.salary}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Required */}
      <section className="card-surface p-6">
        <h2 className="section-title mb-4">Key Skills</h2>
        <div className="flex flex-wrap gap-2">
          {meta.skills.map((skill) => (
            <span key={skill} className="pill">{skill}</span>
          ))}
        </div>
      </section>

      {/* Roadmap */}
      <section className="card-surface p-6">
        <h2 className="section-title mb-6">Learning Roadmap</h2>
        <ol className="space-y-4">
          {meta.roadmap.map((step, index) => (
            <li key={step} className="flex gap-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-600 flex-shrink-0">
                {index + 1}
              </div>
              <span className="pt-1 text-gray-700">{step}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          type="button"
          className="btn-secondary flex-1"
          onClick={() => navigate(-1)}
        >
          ← Back
        </button>
        <button
          type="button"
          className="btn-primary flex-1"
          onClick={() => navigate('/results')}
        >
          View More Matches →
        </button>
      </div>
    </div>
  );
};

export default Details;
