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

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="card-surface py-12 px-6 sm:px-10">
        <div className="space-y-4">
          <div className="inline-block rounded-full bg-blue-50 px-4 py-2 text-xs font-semibold text-blue-600 border border-blue-200">
            🎯 AI Career Guidance
          </div>
          <h1 className="headline-display text-4xl sm:text-5xl font-bold text-gray-900 text-center sm:text-left">
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

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {DOMAIN_CARDS.map((domain) => (
            <Card
              key={domain.id}
              title={domain.title}
              description={domain.description}
            />
          ))}
        </div>
      </section>

      {/* Trending Careers Section */}
      <section className="space-y-6 py-12">
        <div>
          <h2 className="section-title">Trending Careers</h2>
          <p className="section-subtitle">Roles with strong long‑term growth and demand.</p>
        </div>

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {TRENDING_CAREERS.map((career) => (
            <div
              key={career.id}
              className="bg-white rounded-xl shadow-md hover:shadow-lg hover:scale-105 transition-transform duration-300 border border-gray-200 p-5 cursor-pointer"
            >
              <h3 className="text-lg font-semibold text-blue-600">{career.title}</h3>
              <p className="mt-2 text-sm font-medium text-gray-700">{career.growth}</p>
              <p className="mt-1 text-sm text-gray-600">{career.outlook}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;
