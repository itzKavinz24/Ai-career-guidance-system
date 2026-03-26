import json
import os

# Load careers data from JSON file
def _load_careers():
    """Load careers from JSON file"""
    try:
        with open('data/careers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

CAREERS_DB = _load_careers()

def find_matching_careers(skills, interests, assessment):
    """
    Find careers matching user's skills, interests, and assessment
    
    Args:
        skills: List of user skills
        interests: List of user interests
        assessment: Assessment results dictionary
    
    Returns:
        List of matched careers sorted by compatibility score
    """
    matched_careers = []
    
    for career in CAREERS_DB:
        score = calculate_compatibility_score(
            {'skills': skills, 'interests': interests},
            career
        )
        
        if score >= 40:  # Minimum threshold
            matched_careers.append({
                'id': career.get('id'),
                'name': career.get('name'),
                'compatibility_score': score,
                'match_percentage': f"{score}%"
            })
    
    # Sort by compatibility score (descending)
    matched_careers.sort(key=lambda x: x['compatibility_score'], reverse=True)
    
    return matched_careers

def get_career_details(career_id):
    """
    Get detailed information about a specific career
    
    Args:
        career_id: Career ID
    
    Returns:
        Career details dictionary or None
    """
    for career in CAREERS_DB:
        if career.get('id') == career_id:
            return {
                'id': career.get('id'),
                'name': career.get('name'),
                'description': career.get('description'),
                'required_skills': career.get('required_skills', []),
                'required_education': career.get('required_education'),
                'average_salary': career.get('average_salary'),
                'job_outlook': career.get('job_outlook'),
                'work_environment': career.get('work_environment'),
                'pros': career.get('pros', []),
                'cons': career.get('cons', [])
            }
    return None

def calculate_compatibility_score(user_profile, career):
    """
    Calculate compatibility score between user profile and a career
    
    Args:
        user_profile: User profile dictionary with skills and interests
        career: Career object (or career_id string)
    
    Returns:
        Compatibility score (0-100)
    """
    if isinstance(career, str):
        # If career_id is passed, fetch the career
        career = next((c for c in CAREERS_DB if c.get('id') == career), None)
        if not career:
            return 0
    
    user_skills = [s.lower() for s in user_profile.get('skills', [])]
    user_interests = [i.lower() for i in user_profile.get('interests', [])]
    
    career_skills = [s.lower() for s in career.get('required_skills', [])]
    career_interests = career.get('related_interests', [])
    career_interests = [i.lower() for i in career_interests]
    
    # Calculate skill match
    skill_match = 0
    if career_skills:
        skill_overlap = len(set(user_skills) & set(career_skills))
        skill_match = (skill_overlap / len(career_skills)) * 100
    
    # Calculate interest match
    interest_match = 0
    if career_interests:
        interest_overlap = len(set(user_interests) & set(career_interests))
        interest_match = (interest_overlap / len(career_interests)) * 100
    
    # Weighted average (70% skills, 30% interests)
    compatibility_score = (skill_match * 0.7) + (interest_match * 0.3)
    
    return round(compatibility_score, 2)

def get_career_path_recommendations(current_career_id):
    """
    Get recommended career advancement paths from current career
    
    Args:
        current_career_id: Current career ID
    
    Returns:
        List of recommended next careers
    """
    current_career = next((c for c in CAREERS_DB if c.get('id') == current_career_id), None)
    if not current_career:
        return []
    
    current_skills = set(s.lower() for s in current_career.get('required_skills', []))
    
    recommendations = []
    for career in CAREERS_DB:
        if career.get('id') != current_career_id:
            career_skills = set(s.lower() for s in career.get('required_skills', []))
            skill_overlap = len(current_skills & career_skills)
            
            if skill_overlap >= len(current_skills) * 0.6:  # At least 60% skill overlap
                recommendations.append({
                    'id': career.get('id'),
                    'name': career.get('name'),
                    'overlapping_skills': list(current_skills & career_skills),
                    'new_skills_needed': list(career_skills - current_skills)
                })
    
    return recommendations

def filter_careers_by_salary_range(min_salary, max_salary):
    """
    Filter careers by salary range
    
    Args:
        min_salary: Minimum salary
        max_salary: Maximum salary
    
    Returns:
        List of careers within salary range
    """
    filtered = []
    for career in CAREERS_DB:
        avg_salary = career.get('average_salary', 0)
        if min_salary <= avg_salary <= max_salary:
            filtered.append({
                'id': career.get('id'),
                'name': career.get('name'),
                'average_salary': avg_salary
            })
    
    return filtered
