import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { evaluateSkills, getSkillEvaluation } from "../services/api";

const INTEREST_OPTIONS = [
  "Artificial Intelligence & ML",
  "Web & Mobile Development",
  "Cybersecurity & Cloud",
  "Data Science & Analytics",
  "Product & UX",
];

// ✅ Valid skills list
const SKILL_OPTIONS = [
  "Python",
  "Java",
  "C++",
  "JavaScript",
  "React",
  "Node.js",
  "SQL",
  "MongoDB",
  "Machine Learning",
  "Deep Learning",
  "Data Structures",
  "Algorithms",
  "HTML",
  "CSS",
  "Git",
];

const SkillInput = () => {
  const [skills, setSkills] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [domain, setDomain] = useState(INTEREST_OPTIONS[0]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const navigate = useNavigate();

  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const fetchAssessmentScores = async (skillsList) => {
    const userId = `user-${Date.now()}`;
    const started = await evaluateSkills(skillsList, userId);
    const jobId = started?.job_id;

    if (!jobId) {
      return {};
    }

    for (let attempt = 0; attempt < 12; attempt += 1) {
      const job = await getSkillEvaluation(jobId);
      if (job?.status === "completed") {
        const evaluated = Array.isArray(job.evaluated_skills) ? job.evaluated_skills : [];
        return evaluated.reduce((acc, item) => {
          const skill = String(item?.skill || "").trim();
          const score = Number(item?.relative_demand_score ?? 0);
          if (skill) {
            acc[skill] = Number.isFinite(score) ? Math.max(0, Math.min(100, score)) : 0;
          }
          return acc;
        }, {});
      }

      if (job?.status === "failed") {
        return {};
      }

      await wait(900);
    }

    return {};
  };

  // 🔍 Handle typing + suggestions
  const handleChange = (value) => {
    setInputValue(value);

    if (value.length > 0) {
      const filtered = SKILL_OPTIONS.filter((skill) =>
        skill.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filtered);
    } else {
      setSuggestions([]);
    }
  };

  // ✅ Select from dropdown
  const handleSelectSkill = (skill) => {
    if (skills.includes(skill)) {
      setMessage({ type: "error", text: "Skill already added" });
      return;
    }

    setSkills([...skills, skill]);
    setInputValue("");
    setSuggestions([]);
    setMessage(null);
  };

  // ❌ Strict validation
  const handleAddSkill = () => {
    const trimmed = inputValue.trim();

    if (!SKILL_OPTIONS.includes(trimmed)) {
      setMessage({
        type: "error",
        text: "Please select a valid skill from suggestions.",
      });
      return;
    }

    if (skills.includes(trimmed)) {
      setMessage({ type: "error", text: "Skill already added" });
      return;
    }

    setSkills([...skills, trimmed]);
    setInputValue("");
    setSuggestions([]);
    setMessage(null);
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  const handleStartQuiz = async () => {
    if (skills.length === 0) {
      setMessage({
        type: "error",
        text: "Please add at least one skill before continuing.",
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const assessmentScores = await fetchAssessmentScores(skills);

      navigate("/quiz", {
        state: {
          skills,
          domain,
          assessmentScores,
          source: "skills",
        },
      });
    } catch (e) {
      console.error(e);
      setMessage({
        type: "error",
        text: "Something went wrong. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <section className="card-surface glow-ring p-8 relative overflow-hidden">
        <div className="pointer-events-none absolute -top-12 -right-10 h-32 w-32 rounded-full bg-indigo-300/25 blur-2xl" />
        <h1 className="headline-display text-3xl font-bold mb-2">
          Tell us about yourself
        </h1>
        <p className="text-gray-600">
          We'll use your skills and interests to personalize recommendations.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Skills */}
        <section className="card-surface p-6">
          <h2 className="mb-2 font-semibold text-slate-800">Your Skills</h2>

          <div className="space-y-3">
            <div className="flex gap-2 relative">
              <input
                type="text"
                className="input-field flex-1"
                placeholder="Type skill (e.g. Python)"
                value={inputValue}
                onChange={(e) => handleChange(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddSkill();
                  }
                }}
              />

              <button
                type="button"
                className="btn-secondary px-4"
                onClick={handleAddSkill}
              >
                Add
              </button>

              {/* 🔥 Suggestions Dropdown */}
              {suggestions.length > 0 && (
                <div className="absolute top-12 left-0 w-full bg-white/95 border border-blue-100 rounded-xl shadow-xl max-h-44 overflow-y-auto z-10 backdrop-blur">
                  {suggestions.map((skill) => (
                    <div
                      key={skill}
                      className="px-3 py-2 cursor-pointer hover:bg-blue-50 transition-all duration-300"
                      onClick={() => handleSelectSkill(skill)}
                    >
                      {skill}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Selected skills */}
            <div className="min-h-[6rem] bg-white/70 border border-indigo-100 p-3 rounded-xl backdrop-blur-sm">
              {skills.length === 0 ? (
                <p className="text-sm text-gray-500">
                  No skills added yet.
                </p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="chip px-3 py-1 rounded-full flex items-center gap-2"
                    >
                      {skill}
                      <button className="text-red-500" onClick={() => handleRemoveSkill(skill)}>
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Domain */}
        <section className="card-surface p-6">
          <h2 className="mb-2 font-semibold text-slate-800">Interest Area</h2>

          <select
            className="select-field w-full"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
          >
            {INTEREST_OPTIONS.map((opt) => (
              <option key={opt}>{opt}</option>
            ))}
          </select>
        </section>
      </div>

      {/* Submit */}
      <button
        className="btn-primary w-full py-3"
        onClick={handleStartQuiz}
        disabled={loading}
      >
        {loading ? 'Preparing Quiz...' : 'Continue →'}
      </button>

      {message && (
        <div className={message.type === 'error' ? 'message-error' : 'message-success'}>{message.text}</div>
      )}
    </div>
  );
};

export default SkillInput;