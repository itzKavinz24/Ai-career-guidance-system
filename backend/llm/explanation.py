"""Optional explanation helpers for quiz and career guidance responses."""

from typing import Dict


def explain_answer(question_text: str, selected_answer: str, correct_answer: str) -> Dict[str, object]:
    is_correct = (selected_answer or "").strip() == (correct_answer or "").strip()
    return {
        "question": question_text,
        "selected_answer": selected_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "message": "Correct choice." if is_correct else "Review the concept and try again.",
    }
