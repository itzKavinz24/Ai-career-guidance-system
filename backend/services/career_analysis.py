"""Career analysis service: backend metrics + Groq enrichment."""

import json
import os
from typing import Any, Dict, List, Tuple
from urllib import error as urlerror
from urllib import request as urlrequest


CAREER_SKILL_DATASET: Dict[str, List[str]] = {
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics"],
    "ML Engineer": ["Python", "TensorFlow", "APIs", "Deployment"],
    "Data Analyst": ["SQL", "Excel", "Data Visualization", "Statistics"],
    "Backend Developer": ["Python", "APIs", "Databases", "System Design"],
    "Cloud Engineer": ["Cloud", "Deployment", "Linux", "Networking"],
}


def _normalize_input_skills(skills: Dict[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for key, value in (skills or {}).items():
        skill = str(key).strip()
        if not skill:
            continue
        try:
            score = float(value)
        except (TypeError, ValueError):
            score = 0.0
        score = max(0.0, min(10.0, score))
        normalized[skill] = score
    return normalized


def _calculate_metrics(user_skills: Dict[str, float], required_skills: List[str]) -> Dict[str, Any]:
    if not required_skills:
        return {
            "match": 0,
            "domain_gap": 100,
            "tech_gap": 100,
            "missing_skills": [],
            "matched_skills": [],
        }

    required_count = len(required_skills)
    accumulated = 0.0
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    tech_gap_weight = 0.0

    for skill in required_skills:
        score = float(user_skills.get(skill, 0.0))
        accumulated += (score / 10.0) * 100.0

        if score >= 6.0:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

        tech_gap_weight += max(0.0, 6.0 - score) / 6.0

    match = round(accumulated / required_count)
    domain_gap = max(0, 100 - match)
    tech_gap = round((tech_gap_weight / required_count) * 100.0)

    return {
        "match": int(match),
        "domain_gap": int(domain_gap),
        "tech_gap": int(tech_gap),
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
    }


def _groq_config() -> Dict[str, str]:
    api_key = os.getenv("GROQ_CAREER_API_KEY", os.getenv("GROQ_API_KEY", "")).strip()
    model = os.getenv("GROQ_CAREER_MODEL", os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")).strip() or "llama-3.1-8b-instant"
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    return {"api_key": api_key, "model": model, "api_url": api_url}


def _extract_json_object(raw_text: str) -> str:
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found")
    return raw_text[start : end + 1]


def _extract_generated_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        raise ValueError("Unexpected Groq response")

    choices = payload.get("choices", [])
    if not isinstance(choices, list) or not choices:
        raise ValueError("Groq response has no choices")

    first = choices[0]
    if not isinstance(first, dict):
        raise ValueError("Invalid choice format")

    message = first.get("message", {})
    if isinstance(message, dict) and "content" in message:
        return str(message["content"])
    if "text" in first:
        return str(first["text"])
    raise ValueError("No text in Groq response")


def _fallback_llm_output(missing_skills: List[str], role: str) -> Dict[str, Any]:
    if missing_skills:
        first = missing_skills[0]
        recommendations = [
            f"Strengthen {first} with guided practice and mini projects.",
            "Build one portfolio project that demonstrates real-world problem solving.",
        ]
    else:
        recommendations = [
            "Advance to intermediate projects and deepen system design understanding.",
            "Prepare for interviews with role-specific case studies.",
        ]

    return {
        "explanation": f"Your current profile has a reasonable fit for {role} with clear growth opportunities.",
        "tech_recommendations": recommendations,
        "tools": ["Pandas", "NumPy", "Jupyter"],
        "future_scope": "This role has strong demand and long-term growth potential.",
    }


def _call_groq_for_role(user_skills: Dict[str, float], role: str, match: int, missing_skills: List[str]) -> Tuple[Dict[str, Any], str]:
    groq = _groq_config()
    if not groq["api_key"]:
        return _fallback_llm_output(missing_skills, role), "fallback"

    skill_text = ", ".join(f"{name} ({int(score) if score.is_integer() else round(score, 1)})" for name, score in user_skills.items())
    missing_text = ", ".join(missing_skills) if missing_skills else "None"

    prompt = (
        "You are a career advisor.\n\n"
        f"User Skills:\n{skill_text}\n\n"
        f"For the role {role}:\n"
        f"Match: {match}%\n"
        f"Missing Skills: {missing_text}\n\n"
        "Generate:\n"
        "- Short explanation (why user fits)\n"
        "- Specific tech to learn (VERY IMPORTANT)\n"
        "- Example tools (Pandas, NumPy, TensorFlow etc.)\n"
        "- 2 line future scope\n\n"
        "Return JSON:\n"
        "{\n"
        '  "explanation": "",\n'
        '  "tech_recommendations": [],\n'
        '  "tools": [],\n'
        '  "future_scope": ""\n'
        "}\n"
    )

    try:
        body = json.dumps(
            {
                "model": groq["model"],
                "messages": [
                    {"role": "system", "content": "Return valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 500,
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

        raw = _extract_generated_text(payload).strip()
        parsed = json.loads(_extract_json_object(raw))

        llm_output = {
            "explanation": str(parsed.get("explanation", "")).strip(),
            "tech_recommendations": [str(item).strip() for item in parsed.get("tech_recommendations", []) if str(item).strip()],
            "tools": [str(item).strip() for item in parsed.get("tools", []) if str(item).strip()],
            "future_scope": str(parsed.get("future_scope", "")).strip(),
        }

        if not llm_output["explanation"]:
            llm_output["explanation"] = _fallback_llm_output(missing_skills, role)["explanation"]

        return llm_output, "groq"
    except (urlerror.HTTPError, ValueError, json.JSONDecodeError, TimeoutError):
        return _fallback_llm_output(missing_skills, role), "fallback"
    except Exception:
        return _fallback_llm_output(missing_skills, role), "fallback"


def analyze_careers(skills: Dict[str, Any]) -> Dict[str, Any]:
    normalized_skills = _normalize_input_skills(skills)
    if not normalized_skills:
        raise ValueError("skills must be a non-empty object")

    analyses: List[Dict[str, Any]] = []
    sources: List[str] = []

    for role, required in CAREER_SKILL_DATASET.items():
        metrics = _calculate_metrics(normalized_skills, required)
        llm_output, source = _call_groq_for_role(
            user_skills=normalized_skills,
            role=role,
            match=metrics["match"],
            missing_skills=metrics["missing_skills"],
        )
        sources.append(source)

        analyses.append(
            {
                "title": role,
                "match": metrics["match"],
                "domain_gap": metrics["domain_gap"],
                "tech_gap": metrics["tech_gap"],
                "missing_skills": metrics["missing_skills"],
                "matched_skills": metrics["matched_skills"],
                "llm_output": llm_output,
            }
        )

    analyses.sort(key=lambda item: item.get("match", 0), reverse=True)

    overall_source = "groq" if sources and all(item == "groq" for item in sources) else "fallback"

    return {
        "careers": analyses,
        "source": overall_source,
    }
