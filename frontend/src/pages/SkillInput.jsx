import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

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
      await new Promise((resolve) => setTimeout(resolve, 500));

      navigate("/quiz", {
        state: {
          skills,
          domain,
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
      <section className="card-surface p-8">
        <h1 className="text-3xl font-bold mb-2">
          Tell us about yourself
        </h1>
        <p className="text-gray-600">
          We'll use your skills and interests to personalize recommendations.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Skills */}
        <section className="card-surface p-6">
          <h2 className="mb-2 font-semibold">Your Skills</h2>

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
                <div className="absolute top-12 left-0 w-full bg-white border rounded-lg shadow-lg max-h-40 overflow-y-auto z-10">
                  {suggestions.map((skill) => (
                    <div
                      key={skill}
                      className="px-3 py-2 cursor-pointer hover:bg-brand-100 transition-all duration-300"
                      onClick={() => handleSelectSkill(skill)}
                    >
                      {skill}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Selected skills */}
            <div className="min-h-[6rem] bg-gray-50 p-3 rounded-lg">
              {skills.length === 0 ? (
                <p className="text-sm text-gray-500">
                  No skills added yet.
                </p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="bg-brand-500 text-white px-3 py-1 rounded-full flex items-center gap-2"
                    >
                      {skill}
                      <button onClick={() => handleRemoveSkill(skill)}>
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
          <h2 className="mb-2 font-semibold">Interest Area</h2>

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
      >
        Continue →
      </button>

      {message && (
        <div className="text-red-500 text-sm">{message.text}</div>
      )}
    </div>
  );
};

export default SkillInput;