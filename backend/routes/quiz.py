from flask import Blueprint, request

from services import quiz_engine

bp = Blueprint("quiz", __name__)


@bp.route("/start-quiz", methods=["POST"])
def start_quiz():
    """Initialize adaptive quiz state and return the first question."""
    data = request.get_json(silent=True) or {}
    skills = data.get("skills")
    domain = data.get("domain")

    if not isinstance(skills, list) or not skills:
        return {"error": "skills must be a non-empty array"}, 400
    if not isinstance(domain, str) or not domain.strip():
        return {"error": "domain is required"}, 400

    try:
        state = quiz_engine.initialize_quiz_state(skills=skills, domain=domain)
        first_question = quiz_engine.get_first_question(state)
        return {
            "message": "Quiz started",
            "state": state,
            "question": first_question,
            "quiz_complete": bool(state.get("quiz_complete", False)),
        }, 200
    except Exception:
        return {"error": "Failed to start quiz"}, 500


@bp.route("/next-question", methods=["POST"])
def next_question():
    """Evaluate selected answer and return next adaptive question."""
    data = request.get_json(silent=True) or {}
    state = data.get("state")
    selected_answer = data.get("selected_answer")

    if not isinstance(state, dict):
        return {"error": "state must be an object"}, 400
    if not isinstance(selected_answer, str) or not selected_answer.strip():
        return {"error": "selected_answer is required"}, 400

    try:
        result = quiz_engine.get_next_question(state=state, user_answer=selected_answer)
        return {
            "message": "Next question generated",
            "state": result["state"],
            "question": result["next_question"],
            "is_correct": result["is_correct"],
            "quiz_complete": result["quiz_complete"],
        }, 200
    except ValueError as exc:
        return {"error": str(exc)}, 400
    except Exception:
        return {"error": "Failed to generate next question"}, 500
