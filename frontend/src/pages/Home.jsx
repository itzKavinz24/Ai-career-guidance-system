import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';

const DOMAIN_CARDS = [
  {
    id: 'ai',
    title: 'AI & ML',
    description: 'Work on machine learning, generative AI, and intelligent systems.',
  },
  {
    id: 'web-dev',
    title: 'Full Stack Development',
    description: 'Build responsive frontends and robust backend services.',
  },
  {
    id: 'cyber',
    title: 'Cybersecurity & Cloud',
    description: 'Protect systems, analyze threats, and design secure architectures.',
  },
  {
    id: 'data',
    title: 'Data Science & Analytics',
    description: 'Transform data into decisions through analytics and experimentation.',
  },
];

const TRENDING_CAREERS = [
  {
    id: 'ai-engineer',
    title: 'AI Engineer',
    growth: '+28% growth',
    outlook: 'High demand across product and research teams.',
  },
  {
    id: 'fullstack-dev',
    title: 'Full Stack Developer',
    growth: '+22% growth',
    outlook: 'Core role for most SaaS and startup teams.',
  },
  {
    id: 'security-analyst',
    title: 'Security Analyst',
    growth: '+31% growth',
    outlook: 'Critical as organizations move more workloads to cloud.',
  },
  {
    id: 'data-scientist',
    title: 'Data Scientist',
    growth: '+21% growth',
    outlook: 'Strong demand in data‑mature organizations.',
  },
];

const Home = () => {
  const navigate = useNavigate();
  const domainLoop = [...DOMAIN_CARDS, ...DOMAIN_CARDS];
  const trendingLoop = [...TRENDING_CAREERS, ...TRENDING_CAREERS];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="card-surface glow-ring overflow-hidden py-14 px-6 sm:px-10 relative">
        <div className="pointer-events-none absolute -top-16 -right-10 h-44 w-44 rounded-full bg-blue-300/25 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-20 left-12 h-52 w-52 rounded-full bg-teal-300/25 blur-3xl" />
        <div className="space-y-4">
          <div className="inline-block rounded-full border border-blue-200/70 bg-white/75 px-4 py-2 text-xs font-semibold text-blue-700 shadow-sm backdrop-blur">
            🎯 AI Career Guidance
          </div>
          <h1 className="headline-display text-4xl sm:text-5xl font-bold text-gray-900 text-center sm:text-left leading-tight">
            Find Your Perfect Career Path
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto sm:mx-0 text-center sm:text-left">
            Answer a short quiz, share your skills and interests, and get personalized career recommendations powered by AI.
          </p>
        </div>

        <div className="mt-8 flex flex-wrap gap-3 justify-center sm:justify-start">
          <button
            type="button"
            className="btn-primary"
            onClick={() => navigate('/skills')}
          >
            Get Started →
          </button>
          <button
            type="button"
            className="btn-secondary"
            onClick={() => {
              const el = document.getElementById('domains');
              if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
          >
            Learn More
          </button>
        </div>
      </section>

      {/* Domains Section */}
      <section id="domains" className="space-y-6 py-12">
        <div>
          <h2 className="section-title">Explore Career Domains</h2>
          <p className="section-subtitle">Choose an area that interests you to get started.</p>
        </div>

        <div className="auto-rail" style={{ '--slide-duration': '28s' }}>
          <div className="auto-rail-track">
            {domainLoop.map((domain, idx) => (
              <div key={`${domain.id}-${idx}`} className="auto-rail-item">
                <Card
                  title={domain.title}
                  description={domain.description}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trending Careers Section */}
      <section className="space-y-6 py-12">
        <div>
          <h2 className="section-title">Trending Careers</h2>
          <p className="section-subtitle">Roles with strong long‑term growth and demand.</p>
        </div>

        <div className="auto-rail reverse" style={{ '--slide-duration': '34s' }}>
          <div className="auto-rail-track">
            {trendingLoop.map((career, idx) => (
              <div key={`${career.id}-${idx}`} className="auto-rail-item">
                <div className="card-surface lift-on-hover slide-card p-5 cursor-pointer stagger-in h-full">
                  <h3 className="text-lg font-semibold text-blue-600">{career.title}</h3>
                  <p className="mt-2 text-sm font-medium text-gray-700">{career.growth}</p>
                  <p className="mt-1 text-sm text-gray-600">{career.outlook}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
