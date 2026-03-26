"""Groq-backed career recommendation generator with strict JSON parsing and fallback."""

import json
import os
from typing import Any, Dict, List
from urllib import error as urlerror
from urllib import request as urlrequest


_DEFAULT_MODEL = "llama-3.1-8b-instant"
_REQUIRED_KEYS = [
    "title",
    "match_reason",
    "required_skills",
    "matched_skills",
    "missing_skills",
    "career_goal",
    "future_scope",
    "suggestion",
]


def _groq_config() -> Dict[str, str]:
    # Keep career recommendation key isolated from other Groq-powered features.
    api_key = os.getenv("GROQ_CAREER_API_KEY", os.getenv("GROQ_API_KEY", "")).strip()
    model = os.getenv("GROQ_CAREER_MODEL", os.getenv("GROQ_MODEL", _DEFAULT_MODEL)).strip() or _DEFAULT_MODEL
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    return {"api_key": api_key, "model": model, "api_url": api_url}


def _format_skills(skills: Dict[str, Any]) -> str:
    parts: List[str] = []
    for name, score in skills.items():
        try:
            numeric = int(float(score))
        except (ValueError, TypeError):
            numeric = 0
        numeric = max(0, min(10, numeric))
        parts.append(f"{name} ({numeric}/10)")
    return ", ".join(parts)


def _normalized_skill_scores(skills: Dict[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for name, score in skills.items():
        key = str(name).strip().lower()
        if not key:
            continue
        try:
            numeric = float(score)
        except (ValueError, TypeError):
            numeric = 0.0

        # Accept either 0-10 or 0-100 input and normalize to 0-10.
        if numeric > 10:
            numeric = numeric / 10.0
        numeric = max(0.0, min(10.0, numeric))
        normalized[key] = numeric
    return normalized


def _domain_role_catalog(interest_text_full: str) -> List[Dict[str, Any]]:
    if any(keyword in interest_text_full for keyword in ["data", "ai", "ml", "analytics"]):
        return [
            {"title": "Data Scientist", "required": ["python", "sql", "statistics"], "future": "Very high demand in AI-driven decision systems."},
            {"title": "Machine Learning Engineer", "required": ["python", "machine learning", "data structures"], "future": "Strong growth with increasing model deployment needs."},
            {"title": "AI Engineer", "required": ["python", "machine learning", "problem solving"], "future": "Expanding scope across automation and generative AI products."},
            {"title": "Data Analyst", "required": ["sql", "excel", "data visualization"], "future": "Steady growth across business intelligence teams."},
            {"title": "Business Intelligence Analyst", "required": ["sql", "data visualization", "business analysis"], "future": "Consistent demand in analytics-heavy organizations."},
        ]

    if any(keyword in interest_text_full for keyword in ["security", "cyber", "network"]):
        return [
            {"title": "Security Analyst", "required": ["networking", "linux", "problem solving"], "future": "High demand as enterprise security needs keep rising."},
            {"title": "SOC Analyst", "required": ["networking", "incident response", "linux"], "future": "Growing need for real-time threat monitoring."},
            {"title": "Cloud Security Engineer", "required": ["cloud", "security", "linux"], "future": "Strong growth with cloud-first architectures."},
            {"title": "Network Security Engineer", "required": ["networking", "security", "firewalls"], "future": "Stable demand in infrastructure security teams."},
            {"title": "Cybersecurity Consultant", "required": ["security", "risk assessment", "communication"], "future": "Rising consulting opportunities across sectors."},
        ]

    if any(keyword in interest_text_full for keyword in ["design", "ux", "ui", "product"]):
        return [
            {"title": "UX Designer", "required": ["user research", "prototyping", "communication"], "future": "High demand in product-led digital companies."},
            {"title": "UI Designer", "required": ["design systems", "visual design", "prototyping"], "future": "Growing need for accessible interface design."},
            {"title": "Product Designer", "required": ["user research", "ui design", "problem solving"], "future": "Strong growth in startup and SaaS ecosystems."},
            {"title": "Interaction Designer", "required": ["prototyping", "ux", "design systems"], "future": "Increasing demand in app and platform experiences."},
            {"title": "Design Researcher", "required": ["user research", "analytics", "communication"], "future": "Rising strategic role in product teams."},
        ]

    return [
        {"title": "Software Engineer", "required": ["python", "problem solving", "data structures"], "future": "Strong long-term demand across technology companies."},
        {"title": "Full Stack Developer", "required": ["javascript", "react", "node.js"], "future": "Consistent openings for end-to-end product teams."},
        {"title": "Cloud Engineer", "required": ["cloud", "linux", "networking"], "future": "High growth with ongoing cloud migration."},
        {"title": "Business Analyst", "required": ["business analysis", "communication", "problem solving"], "future": "Stable demand in transformation initiatives."},
        {"title": "QA Engineer", "required": ["testing", "automation", "problem solving"], "future": "Steady need in quality-first delivery teams."},
    ]


def _fallback_careers(skills: Dict[str, Any], interests: List[str], top_match: List[str]) -> List[Dict[str, Any]]:
    skill_names = [str(skill).strip() for skill in skills.keys() if str(skill).strip()]
    primary_skills = skill_names[:3]
    score_map = _normalized_skill_scores(skills)
    interest_text_full = " ".join(interests).lower()
    catalog = _domain_role_catalog(interest_text_full)
    role_lookup = {item["title"]: item for item in catalog}

    domain_defaults = [item["title"] for item in catalog]

    # Merge incoming top matches with domain defaults, keep order and uniqueness.
    base_roles: List[str] = []
    for role in top_match + domain_defaults:
        cleaned = str(role).strip()
        if cleaned and cleaned not in base_roles:
            base_roles.append(cleaned)

    interest_text = ", ".join(interests[:3]) if interests else "technology"

    careers: List[Dict[str, Any]] = []
    scored_roles = []
    for role in base_roles:
        meta = role_lookup.get(role, {"title": role, "required": primary_skills or ["problem solving"], "future": "Strong demand with steady long-term growth."})
        required = [str(item).strip().lower() for item in meta.get("required", []) if str(item).strip()]
        if not required:
            required = ["problem solving"]

        weighted = [score_map.get(skill, 0.0) for skill in required]
        average_score = round(sum(weighted) / len(weighted), 2)
        matched = [skill for skill in required if score_map.get(skill, 0.0) >= 6.0]
        missing = [skill for skill in required if score_map.get(skill, 0.0) < 6.0]

        if average_score >= 7.5:
            alignment = "strongly align"
        elif average_score >= 5.5:
            alignment = "partially align"
        else:
            alignment = "need improvement for"

        suggestion = (
            "Focus on improving " + ", ".join(missing[:2]) + " through projects and targeted practice."
            if missing
            else "Strengthen advanced projects and interview readiness for this role."
        )

        scored_roles.append(
            {
                "title": meta.get("title", role),
                "match_score": average_score,
                "match_reason": f"Your skills and interest in {interest_text} {alignment} {meta.get('title', role)}.",
                "required_skills": [item.title() for item in required],
                "matched_skills": [item.title() for item in matched],
                "missing_skills": [item.title() for item in missing],
                "career_goal": f"Contribute to impactful outcomes as a {meta.get('title', role)}.",
                "future_scope": meta.get("future", "Strong demand with steady long-term growth."),
                "suggestion": suggestion,
            }
        )

    scored_roles.sort(key=lambda item: item.get("match_score", 0), reverse=True)
    careers = [
        {
            "title": item["title"],
            "match_reason": item["match_reason"],
            "required_skills": item["required_skills"],
            "matched_skills": item["matched_skills"],
            "missing_skills": item["missing_skills"],
            "career_goal": item["career_goal"],
            "future_scope": item["future_scope"],
            "suggestion": item["suggestion"],
        }
        for item in scored_roles[:5]
    ]
    return careers


def _extract_json_object(raw_text: str) -> str:
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model output")
    return raw_text[start : end + 1]


def _ensure_list_of_strings(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _normalize_careers(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ValueError("Top-level model output must be an object")

    careers = payload.get("careers", [])
    if not isinstance(careers, list):
        raise ValueError("'careers' must be a list")

    normalized: List[Dict[str, Any]] = []
    for item in careers:
        if not isinstance(item, dict):
            continue

        normalized_item = {
            "title": str(item.get("title", "")).strip(),
            "match_reason": str(item.get("match_reason", "")).strip(),
            "required_skills": _ensure_list_of_strings(item.get("required_skills", [])),
            "matched_skills": _ensure_list_of_strings(item.get("matched_skills", [])),
            "missing_skills": _ensure_list_of_strings(item.get("missing_skills", [])),
            "career_goal": str(item.get("career_goal", "")).strip(),
            "future_scope": str(item.get("future_scope", "")).strip(),
            "suggestion": str(item.get("suggestion", "")).strip(),
        }

        if not normalized_item["title"]:
            continue
        normalized.append(normalized_item)
        if len(normalized) == 5:
            break

    if not normalized:
        raise ValueError("No valid career entries found")
    return normalized


def _extract_generated_text(payload: Any) -> str:
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


def _build_prompt(skills: Dict[str, Any], interests: List[str], top_match: List[str]) -> str:
    skills_text = _format_skills(skills)
    interests_text = ", ".join(interests[:5]) if interests else "General"
    top_match_text = ", ".join(top_match[:5]) if top_match else "None"

    schema = {
        "careers": [
            {
                "title": "",
                "match_reason": "",
                "required_skills": [],
                "matched_skills": [],
                "missing_skills": [],
                "career_goal": "",
                "future_scope": "",
                "suggestion": "",
            }
        ]
    }

    return (
        "Based on the following user profile, generate concise career recommendations.\n"
        f"Skills: {skills_text}\n"
        f"Interests: {interests_text}\n"
        f"Current top matches: {top_match_text}\n\n"
        "Generate 3 to 5 similar job roles. For each role include:\n"
        "1) career goal\n"
        "2) required skills\n"
        "3) skill match quality\n"
        "4) future scope\n"
        "5) improvement suggestion\n\n"
        "Return STRICT JSON only. No markdown. No extra keys.\n"
        f"JSON schema: {json.dumps(schema)}"
    )


def generate_career_recommendations(skills: Dict[str, Any], interests: List[str], top_match: List[str]) -> Dict[str, Any]:
    """Generate explainable career recommendations using Groq with fallback."""
    if not isinstance(skills, dict) or not skills:
        raise ValueError("skills must be a non-empty object")

    interests = _ensure_list_of_strings(interests)
    top_match = _ensure_list_of_strings(top_match)

    groq = _groq_config()
    if not groq["api_key"]:
        return {"careers": _fallback_careers(skills, interests, top_match), "source": "fallback"}

    prompt = _build_prompt(skills, interests, top_match)

    try:
        body = json.dumps(
            {
                "model": groq["model"],
                "messages": [
                    {"role": "system", "content": "You output strict valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 900,
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

        with urlrequest.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))

        raw_text = _extract_generated_text(payload).strip()
        json_text = _extract_json_object(raw_text)
        parsed = json.loads(json_text)
        careers = _normalize_careers(parsed)
        return {"careers": careers, "source": "groq"}
    except (urlerror.HTTPError, ValueError, json.JSONDecodeError, TimeoutError):
        return {"careers": _fallback_careers(skills, interests, top_match), "source": "fallback"}
    except Exception:
        return {"careers": _fallback_careers(skills, interests, top_match), "source": "fallback"}
