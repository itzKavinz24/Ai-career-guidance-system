"""Claude-powered question generator for adaptive career quizzes."""

import json
import os
from typing import Dict, List

from dotenv import load_dotenv

try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover - fallback path for missing dependency
    Anthropic = None

load_dotenv()

_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
_CLIENT = Anthropic(api_key=_API_KEY) if Anthropic and _API_KEY else None

_VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def _fallback_questions(skill: str, domain: str, difficulty: str) -> List[Dict[str, object]]:
    """Return deterministic fallback questions when API/JSON parsing fails."""
    prompt_scope = f"{skill} in {domain}" if domain else skill
    return [
        {
            "question": f"Which activity best shows practical {prompt_scope} ability at {difficulty} level?",
            "options": [
                "Break a complex task into smaller steps and execute them",
                "Wait for full instructions before starting",
                "Avoid experimenting with new approaches",
                "Focus only on speed over quality",
            ],
            "answer": "Break a complex task into smaller steps and execute them",
        },
        {
            "question": f"When solving a {prompt_scope} challenge, what is the best first step for {difficulty} learners?",
            "options": [
                "Clarify the problem goals and constraints",
                "Skip planning and start coding immediately",
                "Copy a solution without understanding it",
                "Ignore feedback from users or mentors",
            ],
            "answer": "Clarify the problem goals and constraints",
        },
    ]


def _extract_json_array(raw_text: str) -> str:
    """Trim non-JSON wrapper text and keep only the first JSON array."""
    start = raw_text.find("[")
    end = raw_text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in model output")
    return raw_text[start : end + 1]


def _normalize_questions(parsed: object) -> List[Dict[str, object]]:
    """Validate/normalize Claude output to exactly two safe question objects."""
    if not isinstance(parsed, list):
        raise ValueError("Claude output is not a list")

    normalized: List[Dict[str, object]] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            continue

        options = [str(option).strip() for option in options]
        if not all(options):
            continue

        if answer not in options:
            answer = options[0]

        normalized.append({"question": question, "options": options, "answer": answer})
        if len(normalized) == 2:
            break

    if len(normalized) < 2:
        raise ValueError("Insufficient valid questions in Claude output")

    return normalized


def generate_questions(skill: str, domain: str, difficulty: str) -> List[Dict[str, object]]:
    """Generate two multiple-choice questions for a single skill and difficulty."""
    safe_skill = (skill or "general problem solving").strip()
    safe_domain = (domain or "career aptitude").strip()
    safe_difficulty = (difficulty or "easy").strip().lower()
    if safe_difficulty not in _VALID_DIFFICULTIES:
        safe_difficulty = "easy"

    if _CLIENT is None:
        return _fallback_questions(safe_skill, safe_domain, safe_difficulty)

    prompt = (
        "You are generating a career aptitude quiz."
        " Return STRICT JSON only, no markdown and no explanation."
        " Output must be a JSON array with exactly 2 objects."
        " Each object must have keys: question, options, answer."
        " options must be an array of exactly 4 strings."
        " answer must exactly match one option string."
        f" Domain: {safe_domain}. Skill: {safe_skill}. Difficulty: {safe_difficulty}."
    )

    try:
        response = _CLIENT.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=700,
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
        )

        text_chunks = []
        for block in response.content:
            if getattr(block, "type", "") == "text":
                text_chunks.append(block.text)

        raw_text = "\n".join(text_chunks).strip()
        json_array_text = _extract_json_array(raw_text)
        parsed = json.loads(json_array_text)
        return _normalize_questions(parsed)
    except Exception:
        return _fallback_questions(safe_skill, safe_domain, safe_difficulty)
