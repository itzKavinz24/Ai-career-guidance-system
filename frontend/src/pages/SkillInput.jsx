import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const INTEREST_OPTIONS = [
  'Artificial Intelligence & ML',
  'Web & Mobile Development',
  'Cybersecurity & Cloud',
  'Data Science & Analytics',
  'Product & UX',
];

const SkillInput = () => {
  const [skills, setSkills] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [domain, setDomain] = useState(INTEREST_OPTIONS[0]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const navigate = useNavigate();

  const handleAddSkill = () => {
    const trimmed = inputValue.trim();
    if (!trimmed) return;
    if (skills.includes(trimmed)) {
      setMessage({ type: 'error', text: 'Skill already added' });
      return;
    }
    setSkills([...skills, trimmed]);
    setInputValue('');
    setMessage(null);
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  const handleStartQuiz = async () => {
    if (skills.length === 0) {
      setMessage({ type: 'error', text: 'Please add at least one skill before continuing.' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      // Simulate API call (you can integrate with backend later)
      await new Promise((resolve) => setTimeout(resolve, 500));
      
      // Navigate to quiz with skills and domain
      navigate('/quiz', {
        state: {
          skills,
          domain,
          source: 'skills',
        },
      });
    } catch (e) {
      console.error(e);
      setMessage({ type: 'error', text: 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <section className="card-surface p-8">
        <h1 className="headline-display text-3xl font-bold text-gray-900 mb-2">Tell us about yourself</h1>
        <p className="text-gray-600">We'll use your skills and interests to give you personalized career recommendations.</p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Skills Section */}
        <section className="card-surface p-6">
          <h2 className="section-title mb-2">Your Skills</h2>
          <p className="section-subtitle mb-4">Add technologies and strengths you're comfortable with (e.g., Python, React, Leadership)</p>

          <div className="space-y-3">
            <div className="flex gap-2">
              <input
                type="text"
                className="input-field flex-1"
                placeholder="e.g. Python, React, SQL..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddSkill();
                  }
                }}
                disabled={loading}
              />
              <button type="button" className="btn-secondary px-4" onClick={handleAddSkill} disabled={loading}>
                Add
              </button>
            </div>

            <div className="min-h-[6rem] rounded-lg bg-gray-50 p-3">
              {skills.length === 0 ? (
                <p className="text-sm text-gray-500">No skills added yet. Start with 3–5 skills.</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <span key={skill} className="tag">
                      {skill}
                      <button
                        type="button"
                        className="tag-remove"
                        onClick={() => handleRemoveSkill(skill)}
                        disabled={loading}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <p className="text-xs text-gray-500">
              {skills.length > 0 ? `${skills.length} skill${skills.length > 1 ? 's' : ''} added` : 'No skills yet'}
            </p>
          </div>
        </section>

        {/* Domain Section */}
        <section className="card-surface p-6">
          <h2 className="section-title mb-2">Interest Area</h2>
          <p className="section-subtitle mb-4">What field are you most interested in?</p>

          <div className="space-y-4">
            <select
              className="select-field"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              disabled={loading}
            >
              {INTEREST_OPTIONS.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>

            <div className="rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p className="text-sm text-blue-900">
                <span className="font-semibold">💡 Tip:</span> The more skills you add, the better your personalized recommendations will be.
              </p>
            </div>
          </div>
        </section>
      </div>

      {/* Submit Section */}
      <div className="space-y-4">
        {message && (
          <div className={message.type === 'error' ? 'message-error' : 'message-success'}>
            {message.text}
          </div>
        )}

        <div className="flex gap-3">
          <button
            type="button"
            className="btn-primary flex-1 py-3 text-base"
            onClick={handleStartQuiz}
            disabled={loading || skills.length === 0}
          >
            {loading ? 'Starting...' : 'Continue to Quiz →'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SkillInput;
