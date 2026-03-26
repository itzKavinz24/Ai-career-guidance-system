"""Adaptive quiz engine for dynamic skill-based questioning."""

from typing import Dict, List, Optional

from llm.question_generator import generate_questions

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]


def initialize_quiz_state(skills: List[str], domain: str) -> Dict[str, object]:
    """Create a fresh adaptive quiz state."""
    normalized_skills = [str(skill).strip() for skill in (skills or []) if str(skill).strip()]
    if not normalized_skills:
        normalized_skills = ["problem solving"]

    return {
        "skills": normalized_skills,
        "domain": (domain or "general").strip() or "general",
        "current_skill_index": 0,
        "current_skill": normalized_skills[0],
        "difficulty_level": "easy",
        "correct_count": 0,
        "wrong_count": 0,
        "repeat_fail_count": 0,
        "question_buffer": [],
        "current_question": None,
        "quiz_complete": False,
    }


def _difficulty_index(level: str) -> int:
    try:
        return DIFFICULTY_LEVELS.index(level)
    except ValueError:
        return 0


def _move_to_next_skill(state: Dict[str, object]) -> bool:
    """Advance to next skill. Return False when no skills remain."""
    next_index = int(state.get("current_skill_index", 0)) + 1
    skills = state.get("skills", [])
    if not isinstance(skills, list) or next_index >= len(skills):
        state["quiz_complete"] = True
        state["current_question"] = None
        state["question_buffer"] = []
        return False

    state["current_skill_index"] = next_index
    state["current_skill"] = skills[next_index]
    state["difficulty_level"] = "easy"
    state["repeat_fail_count"] = 0
    state["question_buffer"] = []
    return True


def _pull_question_for_state(state: Dict[str, object]) -> Optional[Dict[str, object]]:
    """Fetch or reuse question buffer and return one question."""
    if state.get("quiz_complete"):
        state["current_question"] = None
        return None

    buffer = state.get("question_buffer", [])
    if not isinstance(buffer, list):
        buffer = []

    if not buffer:
        buffer = generate_questions(
            skill=str(state.get("current_skill", "problem solving")),
            domain=str(state.get("domain", "general")),
            difficulty=str(state.get("difficulty_level", "easy")),
        )

    if not buffer:
        state["current_question"] = None
        state["question_buffer"] = []
        return None

    next_question = buffer.pop(0)
    state["question_buffer"] = buffer
    state["current_question"] = next_question
    return next_question


def get_first_question(state: Dict[str, object]) -> Optional[Dict[str, object]]:
    """Return the first question for a fresh quiz state."""
    return _pull_question_for_state(state)


def get_next_question(state: Dict[str, object], user_answer: str) -> Dict[str, object]:
    """Advance adaptive state and return next question after evaluating user answer."""
    if not isinstance(state, dict):
        raise ValueError("state must be an object")

    current_question = state.get("current_question")
    if not isinstance(current_question, dict):
        raise ValueError("state.current_question is required")

    selected = (user_answer or "").strip()
    expected = str(current_question.get("answer", "")).strip()
    is_correct = selected == expected and selected != ""

    if is_correct:
        state["correct_count"] = int(state.get("correct_count", 0)) + 1
        state["repeat_fail_count"] = 0

        current_idx = _difficulty_index(str(state.get("difficulty_level", "easy")))
        if current_idx < len(DIFFICULTY_LEVELS) - 1:
            state["difficulty_level"] = DIFFICULTY_LEVELS[current_idx + 1]
            state["question_buffer"] = []
        else:
            _move_to_next_skill(state)
    else:
        state["wrong_count"] = int(state.get("wrong_count", 0)) + 1
        repeat_fail_count = int(state.get("repeat_fail_count", 0)) + 1
        state["repeat_fail_count"] = repeat_fail_count

        if repeat_fail_count >= 2:
            _move_to_next_skill(state)
        else:
            # First failure repeats same difficulty once.
            state["question_buffer"] = []

    next_question = _pull_question_for_state(state)
    return {
        "state": state,
        "next_question": next_question,
        "is_correct": is_correct,
        "quiz_complete": bool(state.get("quiz_complete", False)),
    }
