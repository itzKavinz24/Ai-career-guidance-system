from flask import Blueprint, request, jsonify
from services import quiz_engine

bp = Blueprint('input', __name__, url_prefix='/api/input')

@bp.route('/skills', methods=['POST'])
def submit_skills():
    """
    Receive user skills input
    Expected JSON: {'skills': ['skill1', 'skill2', ...]}
    """
    try:
        data = request.get_json()
        skills = data.get('skills', [])
        
        if not skills:
            return {'error': 'Skills list is empty'}, 400
        
        # Validate and process skills
        processed_skills = [skill.strip().lower() for skill in skills if skill.strip()]
        
        return {
            'message': 'Skills received successfully',
            'skills': processed_skills,
            'count': len(processed_skills)
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/interests', methods=['POST'])
def submit_interests():
    """
    Receive user interests input
    Expected JSON: {'interests': ['interest1', 'interest2', ...]}
    """
    try:
        data = request.get_json()
        interests = data.get('interests', [])
        
        if not interests:
            return {'error': 'Interests list is empty'}, 400
        
        processed_interests = [interest.strip().lower() for interest in interests if interest.strip()]
        
        return {
            'message': 'Interests received successfully',
            'interests': processed_interests,
            'count': len(processed_interests)
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/profile', methods=['POST'])
def create_profile():
    """
    Create user profile with skills and interests
    Expected JSON: {'name': 'user', 'skills': [...], 'interests': [...]}
    """
    try:
        data = request.get_json()
        name = data.get('name')
        skills = data.get('skills', [])
        interests = data.get('interests', [])
        
        if not name or (not skills and not interests):
            return {'error': 'Name and at least skills or interests are required'}, 400
        
        profile = {
            'name': name,
            'skills': skills,
            'interests': interests
        }
        
        return {
            'message': 'Profile created successfully',
            'profile': profile
        }, 201
    except Exception as e:
        return {'error': str(e)}, 500
