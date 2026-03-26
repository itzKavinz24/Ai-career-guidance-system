import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getCareerAnalysis, simulateWhatIf } from '../services/api';

const fallbackCareers = [
  {
    id: 'ai-engineer',
    name: 'AI Engineer',
    description: 'Design and deploy intelligent systems',
    icon: '🤖',
    match: 92,
    futureScope: 'Very high demand across AI product teams and automation roles.',
    requiredSkills: ['Python', 'Machine Learning', 'Data Structures'],
    matchedSkills: ['Python'],
    missingSkills: ['Machine Learning', 'Data Structures'],
  },
  {
    id: 'data-scientist',
    name: 'Data Scientist',
    description: 'Extract insights from data',
    icon: '📊',
    match: 88,
    futureScope: 'High growth with strong demand in analytics and AI-driven industries.',
    requiredSkills: ['Python', 'SQL', 'Statistics'],
    matchedSkills: ['Python', 'SQL'],
    missingSkills: ['Statistics'],
  },
  {
    id: 'fullstack-dev',
    name: 'Full‑Stack Developer',
    description: 'Build complete web applications',
    icon: '💻',
    match: 85,
    futureScope: 'Stable hiring demand with strong remote and startup opportunities.',
    requiredSkills: ['JavaScript', 'React', 'Node.js'],
    matchedSkills: ['JavaScript'],
    missingSkills: ['React', 'Node.js'],
  },
  {
    id: 'security-analyst',
    name: 'Security Analyst',
    description: 'Protect systems and networks',
    icon: '🔐',
    match: 78,
    futureScope: 'Cybersecurity demand continues to grow due to expanding threats.',
    requiredSkills: ['Networking', 'Security Fundamentals', 'Linux'],
    matchedSkills: ['Problem Solving'],
    missingSkills: ['Networking', 'Linux'],
  },
  {
    id: 'product-manager',
    name: 'Product Manager',
    description: 'Lead product strategy and vision',
    icon: '📱',
    match: 82,
    futureScope: 'Consistent demand in digital products and platform businesses.',
    requiredSkills: ['Communication', 'Data Literacy', 'Roadmapping'],
    matchedSkills: ['Problem Solving'],
    missingSkills: ['Communication', 'Roadmapping'],
  },
  {
    id: 'ux-designer',
    name: 'UX Designer',
    description: 'Create beautiful user experiences',
    icon: '🎨',
    match: 79,
    futureScope: 'Growing scope in product-led companies and design-heavy teams.',
    requiredSkills: ['User Research', 'Design Systems', 'Prototyping'],
    matchedSkills: [],
    missingSkills: ['User Research', 'Design Systems', 'Prototyping'],
  },
];

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const skills = useMemo(() => location.state?.skills || [], [location.state?.skills]);
  const domain = location.state?.domain || 'General';
  const quizScore = location.state?.quizScore || 0;
  const totalQuestions = location.state?.totalQuestions || 5;
  const [selectedSkill, setSelectedSkill] = useState('');
  const [simulationResult, setSimulationResult] = useState(null);
  const [simulating, setSimulating] = useState(false);
  const [simulationError, setSimulationError] = useState('');
  const [generatedCareers, setGeneratedCareers] = useState([]);
  const [careersLoading, setCareersLoading] = useState(false);
  const [careersError, setCareersError] = useState('');
  const [careersSource, setCareersSource] = useState('fallback');

  const quizPercentage = Math.round((quizScore / (totalQuestions * 20)) * 100) || 0;

  const skillOptions = useMemo(() => {
    if (skills.length > 0) {
      return skills;
    }
    return ['Python', 'SQL', 'JavaScript', 'Problem Solving'];
  }, [skills]);

  const currentScores = useMemo(() => {
    const base = location.state?.currentScores;
    if (base && typeof base === 'object' && Object.keys(base).length > 0) {
      return base;
    }

    return skillOptions.reduce((acc, skill) => {
      acc[skill] = quizPercentage;
      return acc;
    }, {});
  }, [location.state?.currentScores, skillOptions, quizPercentage]);

  const handleSimulate = async () => {
    const skill = selectedSkill || skillOptions[0];
    if (!skill) {
      return;
    }

    setSimulating(true);
    setSimulationError('');
    try {
      const response = await simulateWhatIf(skill, currentScores, [domain]);
      setSimulationResult(response.simulation || null);
    } catch (error) {
      setSimulationError('Simulation failed. Please try again.');
    } finally {
      setSimulating(false);
    }
  };

  useEffect(() => {
    const loadCareerResults = async () => {
      if (!skillOptions.length) {
        setGeneratedCareers([]);
        return;
      }

      setCareersLoading(true);
      setCareersError('');
      try {
        const normalizedSkills = Object.entries(currentScores).reduce((acc, [skill, score]) => {
          const numeric = Number(score);
          const zeroToHundred = Number.isNaN(numeric) ? 0 : Math.max(0, Math.min(100, numeric));
          acc[skill] = Math.round((zeroToHundred / 10) * 10) / 10;
          return acc;
        }, {});

        const response = await getCareerAnalysis(normalizedSkills);

        const mapped = Array.isArray(response.careers)
          ? response.careers.map((career, index) => {
              const matchedSkills = Array.isArray(career.matched_skills) ? career.matched_skills : [];
              const missingSkills = Array.isArray(career.missing_skills) ? career.missing_skills : [];
              const requiredSkills = [...matchedSkills, ...missingSkills];
              const derivedMatch = Number.isFinite(Number(career.match))
                ? Math.max(0, Math.min(100, Math.round(Number(career.match))))
                : Math.max(55, quizPercentage - 5 + index * 2);

              const explanation =
                career.llm_output?.explanation
                || career.match_reason
                || career.career_goal
                || 'Recommended based on your quiz profile';

              return {
                id: `generated-${index + 1}`,
                name: career.title || `Career ${index + 1}`,
                description: explanation,
                icon: '✨',
                match: Math.max(0, Math.min(100, derivedMatch)),
                futureScope: career.llm_output?.future_scope || career.future_scope || 'Steady market demand expected in this domain.',
                requiredSkills,
                matchedSkills,
                missingSkills,
                suggestion:
                  (Array.isArray(career.llm_output?.tech_recommendations) && career.llm_output.tech_recommendations.join(' '))
                  || career.suggestion
                  || 'Improve missing skills and build project experience.',
                detailsAvailable: false,
              };
            })
          : [];

        if (mapped.length > 0) {
          setGeneratedCareers(mapped);
          setCareersSource(response.source || 'groq');
        } else {
          setGeneratedCareers([]);
          setCareersSource('fallback');
        }
      } catch (error) {
        setGeneratedCareers([]);
        setCareersSource('fallback');
        setCareersError('Could not load LLM-based matches. Showing baseline matches.');
      } finally {
        setCareersLoading(false);
      }
    };

    loadCareerResults();
  }, [currentScores, quizPercentage, skillOptions]);

  // Sort careers by match score
  const topCareers = useMemo(() => {
    const source = generatedCareers.length > 0 ? generatedCareers : fallbackCareers;
    return [...source].sort((a, b) => b.match - a.match);
  }, [generatedCareers]);

  // Final visible percentage should depend on result matches after generation.
  const resultPercentage = useMemo(() => {
    if (!topCareers.length) {
      return quizPercentage;
    }
    const considered = topCareers.slice(0, 3);
    const average = considered.reduce((sum, career) => sum + (career.match || 0), 0) / considered.length;
    return Math.round(average);
  }, [topCareers, quizPercentage]);

  const benchmarkScore = 80;
  const techGapAgainstTop = Math.max(0, benchmarkScore - resultPercentage);

  const averageDomainGap = useMemo(() => {
    if (!topCareers.length) {
      return 0;
    }
    const totalGap = topCareers
      .slice(0, 3)
      .reduce((sum, career) => sum + Math.max(0, benchmarkScore - (career.match || 0)), 0);
    return Math.round(totalGap / Math.min(3, topCareers.length));
  }, [topCareers]);

  const commonMissingSkills = useMemo(() => {
    const frequency = {};
    topCareers.slice(0, 3).forEach((career) => {
      (career.missingSkills || []).forEach((skill) => {
        frequency[skill] = (frequency[skill] || 0) + 1;
      });
    });
    return Object.keys(frequency)
      .sort((a, b) => frequency[b] - frequency[a])
      .slice(0, 4);
  }, [topCareers]);

  const personalizedDirection = useMemo(() => {
    const region = domain || 'General';
    if (resultPercentage >= 80) {
      return `You are highly ready for ${region}-focused roles. Prioritize advanced projects and interview prep.`;
    }
    if (resultPercentage >= 60) {
      return `You are in the growth zone for ${region}. Closing skill gaps now can move you to top-tier matches.`;
    }
    return `You are in the foundation stage for ${region}. Build core skills first, then target role-specific projects.`;
  }, [domain, resultPercentage]);

  const futureScopeSummary = useMemo(() => {
    const first = topCareers[0]?.futureScope;
    if (first) {
      return first;
    }
    return resultPercentage >= 70
      ? 'Strong future scope if you continue consistent upskilling.'
      : 'Good future scope, but skill acceleration is needed to stay competitive.';
  }, [topCareers, resultPercentage]);

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
            <p className="text-5xl font-bold text-blue-600">{resultPercentage}%</p>
            <p className="text-sm text-gray-600 mt-1">Match Score</p>
            <p className="text-xs text-gray-500 mt-1">Quiz: {quizPercentage}%</p>
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
              {resultPercentage >= 80 ? '✨ High' : resultPercentage >= 60 ? '🌱 Medium' : '🚀 Emerging'}
            </p>
          </div>
        </div>
      </section>

      {/* Personalized Intelligence */}
      <section className="bg-white rounded-xl shadow-md p-6">
        <div className="mb-4">
          <h2 className="section-title">Result Intelligence</h2>
          <p className="section-subtitle mt-2">
            Suggestions based on your score ({resultPercentage}%) and interest area ({domain}).
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="rounded-lg border border-gray-200 p-4">
            <p className="text-xs text-gray-500 font-semibold">REGION OF INTEREST</p>
            <p className="text-lg font-bold text-gray-900 mt-1">{domain}</p>
          </div>
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
            <p className="text-xs text-amber-700 font-semibold">DOMAIN GAP</p>
            <p className="text-lg font-bold text-amber-700 mt-1">{averageDomainGap}%</p>
          </div>
          <div className="rounded-lg border border-red-200 bg-red-50 p-4">
            <p className="text-xs text-red-700 font-semibold">TECH GAP VS TOP CANDIDATES</p>
            <p className="text-lg font-bold text-red-700 mt-1">{techGapAgainstTop}%</p>
          </div>
          <div className="rounded-lg border border-green-200 bg-green-50 p-4">
            <p className="text-xs text-green-700 font-semibold">FUTURE SCOPE</p>
            <p className="text-sm font-semibold text-green-700 mt-1">{resultPercentage >= 70 ? 'High' : 'Moderate-High'}</p>
          </div>
        </div>

        <div className="mt-4 rounded-lg border border-gray-200 p-4">
          <p className="text-sm font-semibold text-gray-900">Suggested Direction</p>
          <p className="text-sm text-gray-700 mt-1">{personalizedDirection}</p>
        </div>

        <div className="mt-4 rounded-lg border border-blue-200 bg-blue-50 p-4">
          <p className="text-sm font-semibold text-blue-800">Future Scope Insight</p>
          <p className="text-sm text-blue-700 mt-1">{futureScopeSummary}</p>
        </div>

        {commonMissingSkills.length > 0 && (
          <div className="mt-4 rounded-lg border border-gray-200 p-4">
            <p className="text-sm font-semibold text-gray-900 mb-2">Priority Skill Gaps</p>
            <div className="flex flex-wrap gap-2">
              {commonMissingSkills.map((skill) => (
                <span key={skill} className="rounded-full border border-red-200 bg-red-50 px-3 py-1 text-sm text-red-700">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Top Matches */}
      <section>
        <div className="mb-6">
          <h2 className="section-title">Best Career Matches</h2>
          <p className="section-subtitle mt-2">
            Ranked by compatibility with your profile
            {careersLoading ? ' • updating from quiz results...' : ` • source: ${careersSource}`}
          </p>
          {careersError && <p className="text-sm text-amber-700 mt-2">{careersError}</p>}
        </div>

        <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {topCareers.map((career) => (
            <div
              key={career.id}
              className="bg-white rounded-xl shadow-md hover:shadow-lg hover:scale-105 transition-transform duration-300 border border-gray-200 p-6 cursor-pointer"
              onClick={() => {
                if (career.detailsAvailable !== false) {
                  navigate(`/career/${career.id}`, { state: { skills, domain } });
                }
              }}
            >
              <div className="flex items-start justify-between mb-4">
                <span className="text-4xl">{career.icon}</span>
                <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-3 py-1 border border-blue-100">
                  <span className="text-sm font-bold text-blue-700">{career.match}%</span>
                </span>
              </div>
              <h3 className="text-lg font-bold text-blue-700">{career.name}</h3>
              <p className="text-sm text-gray-600 mt-2">{career.description}</p>

              <div className="mt-3 grid grid-cols-2 gap-2">
                <div className="rounded-md bg-amber-50 border border-amber-200 p-2">
                  <p className="text-[10px] font-semibold text-amber-700">DOMAIN GAP</p>
                  <p className="text-xs font-bold text-amber-700">{Math.max(0, benchmarkScore - (career.match || 0))}%</p>
                </div>
                <div className="rounded-md bg-red-50 border border-red-200 p-2">
                  <p className="text-[10px] font-semibold text-red-700">TECH GAP</p>
                  <p className="text-xs font-bold text-red-700">
                    {career.requiredSkills?.length
                      ? Math.round(((career.missingSkills?.length || 0) / career.requiredSkills.length) * 100)
                      : Math.max(0, benchmarkScore - (career.match || 0))}%
                  </p>
                </div>
              </div>

              <div className="mt-3 rounded-md bg-green-50 border border-green-200 p-3">
                <p className="text-[10px] font-semibold text-green-700">FUTURE SCOPE</p>
                <p className="text-xs text-green-700 mt-1">{career.futureScope || 'Good scope with continuous upskilling.'}</p>
              </div>

              <button className="mt-4 w-full py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-sm font-semibold text-gray-700 transition">
                {career.detailsAvailable === false ? 'AI Suggestion' : 'View Details →'}
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

      {/* What If Simulation */}
      <section className="bg-white rounded-xl shadow-md p-6">
        <div className="mb-4">
          <h3 className="text-xl font-bold text-gray-900">What If You Improve?</h3>
          <p className="text-sm text-gray-600 mt-1">
            Simulate how improving one skill can change your career outcomes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 items-end">
          <div className="md:col-span-2">
            <label htmlFor="skill-simulation" className="block text-sm font-semibold text-gray-700 mb-2">
              Select Skill
            </label>
            <select
              id="skill-simulation"
              value={selectedSkill}
              onChange={(e) => setSelectedSkill(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Choose a skill</option>
              {skillOptions.map((skill) => (
                <option key={skill} value={skill}>
                  {skill}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            onClick={handleSimulate}
            disabled={simulating || skillOptions.length === 0}
            className="w-full rounded-lg bg-blue-600 text-white px-4 py-2 font-semibold hover:bg-blue-700 disabled:opacity-50"
          >
            {simulating ? 'Simulating...' : 'Simulate'}
          </button>
        </div>

        {simulationError && (
          <p className="mt-4 text-sm text-red-600">{simulationError}</p>
        )}

        {simulationResult && (
          <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="rounded-lg border border-gray-200 p-4">
              <p className="text-xs font-semibold text-gray-500">OLD MATCH %</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{simulationResult.old_match_percentage}%</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-4">
              <p className="text-xs font-semibold text-gray-500">NEW MATCH %</p>
              <p className="text-2xl font-bold text-blue-700 mt-1">{simulationResult.new_match_percentage}%</p>
            </div>
            <div className="rounded-lg border border-green-200 bg-green-50 p-4">
              <p className="text-xs font-semibold text-green-700">IMPROVEMENT %</p>
              <p className="text-2xl font-bold text-green-700 mt-1">+{simulationResult.improvement_percentage}%</p>
            </div>

            <div className="sm:col-span-3 rounded-lg border border-gray-200 p-4">
              <p className="text-xs font-semibold text-gray-500 mb-2">NEW POSSIBLE JOB ROLES</p>
              {simulationResult.new_possible_job_roles?.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {simulationResult.new_possible_job_roles.map((role) => (
                    <span key={role} className="rounded-full border border-green-200 bg-green-50 px-3 py-1 text-sm text-green-700">
                      {role}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-600">
                  No additional roles unlocked yet. Keep improving for bigger jumps.
                </p>
              )}
            </div>

            <div className="sm:col-span-3 rounded-lg border border-blue-200 bg-blue-50 p-4">
              <p className="text-xs font-semibold text-blue-700 mb-3">TOP SIMULATED CAREERS</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {(simulationResult.top_matches_after_simulation || []).slice(0, 3).map((career) => (
                  <div key={career.id} className="rounded-lg bg-white border border-blue-100 p-3">
                    <p className="text-sm font-bold text-gray-900">{career.name}</p>
                    <p className="text-xs text-gray-500 mt-1">Projected Match</p>
                    <p className="text-lg font-bold text-blue-700 mt-1">{career.score}%</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </section>

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
