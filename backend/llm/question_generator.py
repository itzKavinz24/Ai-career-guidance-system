"""Groq-backed question generator with robust JSON parsing and fallback."""

import json
import os
import random
from urllib import error as urlerror
from urllib import request as urlrequest
from typing import Dict, List

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
    prompt_scope = f"{skill} in {domain}" if domain else skill
    difficulty_context = {
        "easy": "basic",
        "medium": "intermediate",
        "hard": "advanced",
    }.get(difficulty, "basic")

    question_stems = [
        f"Which choice best demonstrates {difficulty_context} {prompt_scope} decision-making?",
        f"In a {prompt_scope} scenario, what is the strongest {difficulty} approach?",
        f"What action most improves outcomes in {difficulty_context} {prompt_scope} tasks?",
        f"When facing a {prompt_scope} challenge, what should you prioritize first?",
        f"Which behavior reflects strong {difficulty_context} thinking for {prompt_scope}?",
    ]
    correct_options = [
        "Break the problem into steps, test assumptions, and iterate with feedback",
        "Clarify requirements, choose a method, then validate with measurable results",
        "Identify constraints early and adapt the solution based on evidence",
        "Evaluate trade-offs, then implement and review outcomes systematically",
    ]
    distractors = [
        "Pick the first idea and avoid revisiting it even if it fails",
        "Optimize only for speed while ignoring quality and constraints",
        "Copy a prior solution without checking whether context has changed",
        "Delay all decisions until someone else chooses for you",
        "Ignore user feedback to keep the implementation unchanged",
        "Avoid planning and start execution immediately with no checks",
        "Rely on intuition only and skip data or validation",
        "Focus on one detail and ignore system-level impact",
    ]

    random.shuffle(question_stems)
    questions: List[Dict[str, object]] = []
    for stem in question_stems[:2]:
        correct = random.choice(correct_options)
        wrong = random.sample(distractors, 3)
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
        return _fallback_questions(safe_skill, safe_domain, safe_difficulty)

    prompt = (
        "Generate aptitude quiz questions. "
        "Return STRICT JSON only with no markdown and no explanation. "
        "Output must be a JSON array with exactly 2 objects. "
        "Each object requires keys: question, options, answer. "
        "options must have exactly 4 strings and answer must match one option exactly. "
        f"Skill: {safe_skill}. Domain: {safe_domain}. Difficulty: {safe_difficulty}."
    )

    try:
        body = json.dumps(
            {
                "model": groq["model"],
                "messages": [
                    {
                        "role": "system",
                        "content": "You output strict JSON only.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "temperature": 0.4,
                "max_tokens": 700,
            }
        ).encode("utf-8")

        req = urlrequest.Request(
            groq["api_url"],
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {groq['api_key']}",
                "Content-Type": "application/json",
            },
        )

        with urlrequest.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

        raw_text = _extract_generated_text(payload).strip()

        json_text = _extract_json_array(raw_text)
        parsed = json.loads(json_text)
        return _attach_meta(_normalize(parsed), "groq")
    except urlerror.HTTPError as exc:
        return _attach_meta(
            _fallback_questions(safe_skill, safe_domain, safe_difficulty),
            "fallback",
            f"groq_http_error:{exc.code}",
        )
    except Exception as exc:
        return _attach_meta(
            _fallback_questions(safe_skill, safe_domain, safe_difficulty),
            "fallback",
            f"groq_exception:{exc}",
        )
