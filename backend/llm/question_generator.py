"""Groq-backed question generator with robust JSON parsing and fallback."""

import json
import os
import random
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

_VALID_DIFFICULTIES = {"easy", "medium", "hard"}
_DEFAULT_MODEL = "llama-3.1-8b-instant"


def _debug_enabled() -> bool:
    return os.getenv("GROQ_DEBUG", "false").strip().lower() == "true"


def _attach_meta(questions: List[Dict[str, object]], source: str, error_text: str = "") -> List[Dict[str, object]]:
    enriched: List[Dict[str, object]] = []
    for question in questions:
        item = dict(question)
        item["source"] = source
        if error_text and _debug_enabled():
            item["debug_error"] = error_text
        enriched.append(item)
    return enriched


def _groq_config() -> Dict[str, str]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", _DEFAULT_MODEL).strip() or _DEFAULT_MODEL
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    return {"api_key": api_key, "model": model, "api_url": api_url}


def _fallback_questions(skill: str, domain: str, difficulty: str) -> List[Dict[str, object]]:
    """Generate truly diverse fallback questions using skill/domain-specific templates."""
    safe_skill = skill.strip().lower()
    safe_domain = domain.strip().lower()
    safe_difficulty = difficulty.strip().lower()
    
    # Skill-specific question templates to avoid repetition
    skill_templates = {
        "python": [
            f"What best demonstrates {safe_difficulty} {skill} mastery in {domain}?",
            f"In {domain}, how should you approach a complex {skill} problem?",
            f"Which practice most improves {skill} skills for {domain} roles?",
            f"When debugging {skill} code in {domain}, what's the first step?",
            f"How do you choose the right {skill} approach for {domain} tasks?",
            f"What indicates strong {skill} fundamentals for {domain} work?",
        ],
        "sql": [
            f"How should you design queries for {domain} in {skill}?",
            f"What's the best {skill} strategy for {domain} data scenarios?",
            f"Which {skill} practice improves {domain} performance?",
            f"When optimizing {skill} for {domain}, what matters most?",
            f"What demonstrates {skill} competency in {domain} contexts?",
            f"How do you validate {skill} solutions for {domain} work?",
        ],
        "machine learning": [
            f"How should you approach {skill} for {domain}?",
            f"What's critical in {skill} projects within {domain}?",
            f"Which step is most important in {skill} workflows for {domain}?",
            f"How do you evaluate {skill} models in {domain}?",
            f"What indicates strong {skill} understanding for {domain}?",
            f"When starting a {skill} project in {domain}, what comes first?",
        ],
    }
    
    # Get skill-specific templates or use generic ones
    skill_key = next((k for k in skill_templates if k in safe_skill), None)
    question_seeds = skill_templates.get(skill_key, [
        f"Which approach best demonstrates {safe_difficulty} thinking for {skill} in {domain}?",
        f"When facing a {skill} challenge in {domain}, what should you prioritize?",
        f"How should you handle {skill} tasks in {domain} contexts?",
        f"What indicates strong {skill} fundamentals for {domain}?",
        f"In {domain}, how do you apply {skill} effectively?",
    ])
    
    # Diverse correct answers (not just one pool)
    difficulty_strategies = {
        "easy": [
            "Start with basics, practice fundamentals, build confidence",
            "Learn from examples, follow established patterns, repeat practice",
            "Study core concepts, apply step-by-step, validate understanding",
            "Focus on foundations, use best practices, get feedback",
        ],
        "medium": [
            "Break into parts, test assumptions, iterate from feedback",
            "Clarify scope, choose method, validate measurable results",
            "Consider constraints early, adapt solution, track outcomes",
            "Evaluate trade-offs, implement, review and refactor",
        ],
        "hard": [
            "Design for scale, anticipate edge cases, build robustness",
            "Balance performance with maintainability across constraints",
            "Optimize systematically, profile, measure, refactor based on metrics",
            "Plan architecture, handle failures, ensure long-term quality",
        ],
    }
    
    correct_options = difficulty_strategies.get(safe_difficulty, difficulty_strategies["easy"])
    bad_answers = [
        "Pick first idea without checking context",
        "Optimize speed while ignoring quality",
        "Copy solutions without understanding",
        "Skip planning and code immediately",
        "Ignore feedback and user needs",
        "Rely only on intuition",
        "Focus on one detail, ignore system impact",
        "Avoid testing and validation",
    ]
    
    random.shuffle(question_seeds)
    questions: List[Dict[str, object]] = []
    
    for i, stem in enumerate(question_seeds[:2]):
        correct = correct_options[i % len(correct_options)]
        unique_seed = hash(stem) % len(bad_answers)
        wrong = random.sample(bad_answers, 3)
        options = wrong + [correct]
        random.shuffle(options)
        questions.append({"question": stem, "options": options, "answer": correct})
    
    return _attach_meta(questions, "fallback")


def _extract_json_array(raw_text: str) -> str:
    start = raw_text.find("[")
    end = raw_text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found")
    return raw_text[start : end + 1]


def _normalize(parsed: object) -> List[Dict[str, object]]:
    if not isinstance(parsed, list):
        raise ValueError("Model output must be a list")

    result: List[Dict[str, object]] = []
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

        result.append({"question": question, "options": options, "answer": answer})
        if len(result) == 2:
            break

    if len(result) < 2:
        raise ValueError("Insufficient valid questions")
    return result


def _extract_generated_text(payload: object) -> str:
    if not isinstance(payload, dict):
        raise ValueError("Unexpected Groq response format")

    choices = payload.get("choices", [])
    if not isinstance(choices, list) or not choices:
        raise ValueError("Groq response missing choices")

    first = choices[0]
    if not isinstance(first, dict):
        raise ValueError("Invalid Groq choice format")

    message = first.get("message", {})
    if isinstance(message, dict) and "content" in message:
        return str(message["content"])

    if "text" in first:
        return str(first["text"])

    raise ValueError("No generated text in Groq response")


def generate_questions(skill: str, domain: str, difficulty: str) -> List[Dict[str, object]]:
    """Generate 2 questions for one skill/domain/difficulty using Groq, with fallback."""
    safe_skill = (skill or "problem solving").strip()
    safe_domain = (domain or "career aptitude").strip()
    safe_difficulty = (difficulty or "easy").strip().lower()
    if safe_difficulty not in _VALID_DIFFICULTIES:
        safe_difficulty = "easy"

    groq = _groq_config()
    if not groq["api_key"]:
        print(f"[question_generator] No Groq API key; using fallback for {safe_skill}/{safe_domain}/{safe_difficulty}")
        return _fallback_questions(safe_skill, safe_domain, safe_difficulty)

    prompt = (
        "Generate 2 unique multiple-choice aptitude questions. "
        "Return ONLY valid JSON with no markdown, no code blocks, no explanation. "
        "Use this exact format:\n"
        "[\n"
        '  {"question": "...", "options": ["A", "B", "C", "D"], "answer": "..."},\n'
        '  {"question": "...", "options": ["A", "B", "C", "D"], "answer": "..."}\n'
        "]\n\n"
        f"Skill: {safe_skill}\n"
        f"Domain: {safe_domain}\n"
        f"Difficulty: {safe_difficulty}\n"
        "Each question must:\n"
        "- Test judgment and problem-solving\n"
        "- Have 4 distinct options\n"
        "- Have only 1 correct answer\n"
        "- Be completely different from common quiz patterns\n"
        "Make questions challenging and context-specific."
    )

    for attempt in range(2):  # Retry once on failure
        try:
            body = json.dumps(
                {
                    "model": groq["model"],
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a quiz generator. Return ONLY valid JSON. No explanation.",
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    "temperature": 0.7,
                    "max_tokens": 800,
                }
            )

            response = requests.post(
                groq["api_url"],
                headers={
                    "Authorization": f"Bearer {groq['api_key']}",
                    "Content-Type": "application/json",
                },
                json=json.loads(body),
                timeout=25,
            )

            if response.status_code != 200:
                raise requests.HTTPError(f"HTTP {response.status_code}: {response.text[:200]}", response=response)

            payload = response.json()
            raw_text = _extract_generated_text(payload).strip()
            json_text = _extract_json_array(raw_text)
            parsed = json.loads(json_text)
            result = _attach_meta(_normalize(parsed), "groq")
            print(f"[question_generator] Groq success: {safe_skill}/{safe_domain}/{safe_difficulty}")
            return result
        except (requests.HTTPError, ValueError, json.JSONDecodeError, requests.Timeout) as e:
            error_msg = f"{type(e).__name__}"
            if isinstance(e, requests.HTTPError):
                error_msg += f": {str(e)[:100]}"
            else:
                error_msg += f": {str(e)[:100]}"
            
            if attempt == 0:
                print(f"[question_generator] Groq attempt 1 failed ({error_msg}), retrying...")
            else:
                print(f"[question_generator] Groq attempt 2 failed ({error_msg}), using fallback")
    
    print(f"[question_generator] All attempts failed; using fallback for {safe_skill}/{safe_domain}/{safe_difficulty}")
    return _fallback_questions(safe_skill, safe_domain, safe_difficulty)

