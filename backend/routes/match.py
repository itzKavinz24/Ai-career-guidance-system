from flask import Blueprint, request, jsonify
from services import matcher, trends

bp = Blueprint('match', __name__, url_prefix='/api/match')

@bp.route('/careers', methods=['POST'])
def match_careers():
    """
    Match user profile to suitable careers
    Expected JSON: {'user_id': 'user123', 'skills': [...], 'interests': [...], 'assessment': {...}}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        skills = data.get('skills', [])
        interests = data.get('interests', [])
        assessment = data.get('assessment', {})
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        matched_careers = matcher.find_matching_careers(skills, interests, assessment)
        
        return {
            'message': 'Career matches found',
            'user_id': user_id,
            'matches': matched_careers,
            'match_count': len(matched_careers)
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/career-details/<career_id>', methods=['GET'])
def get_career_details(career_id):
    """
    Get detailed information about a specific career
    """
    try:
        career = matcher.get_career_details(career_id)
        
        if not career:
            return {'error': 'Career not found'}, 404
        
        return {
            'message': 'Career details retrieved',
            'career': career
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/compatibility-score', methods=['POST'])
def calculate_compatibility():
    """
    Calculate compatibility score between user profile and a specific career
    Expected JSON: {'user_id': 'user123', 'career_id': 'career1', 'profile': {...}}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        career_id = data.get('career_id')
        profile = data.get('profile', {})
        
        if not all([user_id, career_id]):
            return {'error': 'User ID and Career ID are required'}, 400
        
        score = matcher.calculate_compatibility_score(profile, career_id)
        
        return {
            'message': 'Compatibility score calculated',
            'user_id': user_id,
            'career_id': career_id,
            'compatibility_score': score
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/trending-careers', methods=['GET'])
def get_trending_careers():
    """
    Get trending careers based on current market data
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        trending = trends.get_trending_careers(page, limit)
        
        return {
            'message': 'Trending careers retrieved',
            'careers': trending,
            'page': page,
            'limit': limit
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/growth-opportunities/<career_id>', methods=['GET'])
def get_growth_opportunities(career_id):
    """
    Get growth opportunities and career progression paths
    """
    try:
        opportunities = trends.get_growth_opportunities(career_id)
        
        if not opportunities:
            return {'error': 'No opportunities found for this career'}, 404
        
        return {
            'message': 'Growth opportunities retrieved',
            'career_id': career_id,
            'opportunities': opportunities
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@bp.route('/salary-trends/<career_id>', methods=['GET'])
def get_salary_trends(career_id):
    """
    Get salary trends for a specific career
    """
    try:
        salary_data = trends.get_salary_trends(career_id)
        
        if not salary_data:
            return {'error': 'Salary data not found for this career'}, 404
        
        return {
            'message': 'Salary trends retrieved',
            'career_id': career_id,
            'salary_trends': salary_data
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500
