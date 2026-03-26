from flask import Blueprint, request, jsonify
from services import quiz_engine

bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

@bp.route('/start', methods=['POST'])
def start_quiz():
    """
    Start a new quiz session
    Expected JSON: {'user_id': 'user123', 'difficulty': 'medium'}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        difficulty = data.get('difficulty', 'medium')
        skills = data.get('skills', [])
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        questions = quiz_engine.get_skill_based_questions(
            skills=skills,
            difficulty=difficulty,
            num_questions=10
        )
        
        return {
            'message': 'Quiz started',
            'user_id': user_id,
            'difficulty': difficulty,
            'skills_used': skills,
            'total_questions': len(questions),
            'questions': questions
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    """
    Submit an answer to a quiz question
    Expected JSON: {'user_id': 'user123', 'question_id': 'q1', 'answer': 'option_a'}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        
        if not all([user_id, question_id, answer]):
            return {'error': 'User ID, question ID, and answer are required'}, 400
        
        # Validate and record the answer
        is_correct = quiz_engine.validate_answer(question_id, answer)
        quiz_engine.record_answer(user_id, question_id, answer, is_correct)
        
        return {
            'message': 'Answer recorded',
            'question_id': question_id,
            'is_correct': is_correct
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/get-question/<question_id>', methods=['GET'])
def get_question(question_id):
    """
    Get a specific question by ID
    """
    try:
        question = quiz_engine.get_question(question_id)
        
        if not question:
            return {'error': 'Question not found'}, 404
        
        return {
            'message': 'Question retrieved',
            'question': question
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/end', methods=['POST'])
def end_quiz():
    """
    End the quiz and get results
    Expected JSON: {'user_id': 'user123'}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        results = quiz_engine.calculate_results(user_id)
        
        return {
            'message': 'Quiz ended',
            'results': results
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500
