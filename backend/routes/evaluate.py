from flask import Blueprint, request, jsonify
from services import scoring

bp = Blueprint('evaluate', __name__, url_prefix='/api/evaluate')

@bp.route('/skills', methods=['POST'])
def evaluate_skills():
    """
    Evaluate user skills and provide proficiency scores
    Expected JSON: {'skills': ['Python', 'JavaScript'], 'user_id': 'user123'}
    """
    try:
        data = request.get_json()
        skills = data.get('skills', [])
        user_id = data.get('user_id')
        
        if not skills:
            return {'error': 'Skills list is required'}, 400
        
        job_id = scoring.start_demand_scoring_job(skills, user_id)

        return {
            'message': 'Demand-based skill scoring started',
            'user_id': user_id,
            'job_id': job_id,
            'status': 'processing'
        }, 202
    except Exception as e:
        return {'error': str(e)}, 500


@bp.route('/skills/<job_id>', methods=['GET'])
def get_skill_evaluation(job_id):
    """
    Fetch background demand-based skill scoring result.
    """
    try:
        job = scoring.get_demand_scoring_job(job_id)
        if not job:
            return {'error': 'Evaluation job not found'}, 404

        response = {
            'job_id': job['job_id'],
            'user_id': job.get('user_id'),
            'status': job['status'],
            'created_at': job.get('created_at'),
            'started_at': job.get('started_at'),
            'completed_at': job.get('completed_at'),
        }

        if job['status'] == 'completed':
            response['evaluated_skills'] = job.get('result', [])
            response['message'] = 'Demand-based scoring completed'
            return response, 200

        if job['status'] == 'failed':
            response['error'] = job.get('error', 'Scoring failed')
            return response, 500

        response['message'] = 'Demand-based scoring in progress'
        return response, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/quiz-performance', methods=['POST'])
def evaluate_quiz_performance():
    """
    Evaluate quiz performance and provide scoring
    Expected JSON: {'user_id': 'user123', 'answers': [...], 'time_taken': 600}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        answers = data.get('answers', [])
        time_taken = data.get('time_taken', 0)
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        performance = scoring.calculate_quiz_score(answers, time_taken)
        
        return {
            'message': 'Quiz performance evaluated',
            'user_id': user_id,
            'performance_score': performance
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/overall-assessment', methods=['POST'])
def overall_assessment():
    """
    Provide overall assessment combining skills, interests, and quiz results
    Expected JSON: {'user_id': 'user123', 'skills_score': 75, 'quiz_score': 80}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        skills_score = data.get('skills_score', 0)
        quiz_score = data.get('quiz_score', 0)
        interests = data.get('interests', [])
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        assessment = scoring.generate_assessment(skills_score, quiz_score, interests)
        
        return {
            'message': 'Overall assessment generated',
            'user_id': user_id,
            'assessment': assessment
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/strengths-weaknesses', methods=['POST'])
def analyze_strengths_weaknesses():
    """
    Analyze user strengths and weaknesses
    Expected JSON: {'user_id': 'user123', 'skills': [...], 'quiz_results': {...}}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        skills = data.get('skills', [])
        quiz_results = data.get('quiz_results', {})
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        analysis = scoring.analyze_strengths_weaknesses(skills, quiz_results)
        
        return {
            'message': 'Strengths and weaknesses analyzed',
            'user_id': user_id,
            'analysis': analysis
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500
