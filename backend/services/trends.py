import json

# Load careers data
def _load_careers():
    """Load careers from JSON file"""
    try:
        with open('data/careers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

CAREERS_DB = _load_careers()

def get_trending_careers(page=1, limit=10):
    """
    Get trending careers based on job outlook and growth rate
    
    Args:
        page: Page number for pagination
        limit: Number of results per page
    
    Returns:
        List of trending careers
    """
    # Sort by growth rate or job outlook
    sorted_careers = sorted(
        CAREERS_DB,
        key=lambda c: float(c.get('growth_rate', 0)),
        reverse=True
    )
    
    start = (page - 1) * limit
    end = start + limit
    
    trending = []
    for career in sorted_careers[start:end]:
        trending.append({
            'id': career.get('id'),
            'name': career.get('name'),
            'growth_rate': career.get('growth_rate'),
            'job_outlook': career.get('job_outlook'),
            'openings_per_year': career.get('openings_per_year', 'N/A')
        })
    
    return trending

def get_growth_opportunities(career_id):
    """
    Get growth opportunities and advancement paths for a career
    
    Args:
        career_id: Career ID
    
    Returns:
        Dictionary with growth opportunities
    """
    career = next((c for c in CAREERS_DB if c.get('id') == career_id), None)
    if not career:
        return None
    
    advancement_paths = career.get('advancement_paths', [])
    specializations = career.get('specializations', [])
    
    return {
        'career_id': career_id,
        'career_name': career.get('name'),
        'advancement_paths': advancement_paths,
        'specializations': specializations,
        'additional_certifications': career.get('additional_certifications', []),
        'further_education': career.get('further_education_options', []),
        'growth_potential': career.get('growth_potential', 'Moderate')
    }

def get_salary_trends(career_id):
    """
    Get salary trends for a specific career over different experience levels
    
    Args:
        career_id: Career ID
    
    Returns:
        Salary trend data
    """
    career = next((c for c in CAREERS_DB if c.get('id') == career_id), None)
    if not career:
        return None
    
    salary_by_experience = {
        'entry_level': career.get('entry_salary', 'N/A'),
        'mid_level': career.get('average_salary', 'N/A'),
        'senior_level': career.get('senior_salary', 'N/A'),
        'experienced': career.get('experienced_salary', 'N/A')
    }
    
    return {
        'career_id': career_id,
        'career_name': career.get('name'),
        'salary_by_experience': salary_by_experience,
        'salary_growth_rate': career.get('salary_growth_rate', 'N/A'),
        'currency': career.get('currency', 'USD')
    }

def get_in_demand_skills():
    """
    Get skills that are most in-demand across all careers
    
    Returns:
        List of in-demand skills with frequency
    """
    skill_frequency = {}
    
    for career in CAREERS_DB:
        skills = career.get('required_skills', [])
        for skill in skills:
            skill_lower = skill.lower()
            skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
    
    # Sort by frequency
    sorted_skills = sorted(
        skill_frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [{
        'skill': skill,
        'frequency': count,
        'demand_level': get_demand_level(count / len(CAREERS_DB))
    } for skill, count in sorted_skills[:20]]

def get_demand_level(frequency_ratio):
    """
    Get demand level based on frequency ratio
    
    Args:
        frequency_ratio: Ratio of appearances
    
    Returns:
        Demand level string
    """
    if frequency_ratio >= 0.8:
        return 'Extremely High'
    elif frequency_ratio >= 0.6:
        return 'Very High'
    elif frequency_ratio >= 0.4:
        return 'High'
    elif frequency_ratio >= 0.2:
        return 'Moderate'
    else:
        return 'Low'

def get_emerging_careers():
    """
    Get emerging careers with high growth rates
    
    Returns:
        List of emerging careers
    """
    emerging = []
    
    for career in CAREERS_DB:
        growth_rate = float(career.get('growth_rate', 0))
        job_outlook = career.get('job_outlook', '')
        
        if growth_rate >= 15 or 'faster than average' in job_outlook.lower():
            emerging.append({
                'id': career.get('id'),
                'name': career.get('name'),
                'growth_rate': growth_rate,
                'why_emerging': career.get('why_emerging', 'High growth potential')
            })
    
    return sorted(emerging, key=lambda x: x['growth_rate'], reverse=True)

def get_industry_trends():
    """
    Get trends across industries
    
    Returns:
        Dictionary of industry trends
    """
    industry_data = {}
    
    for career in CAREERS_DB:
        industry = career.get('industry', 'General')
        if industry not in industry_data:
            industry_data[industry] = {
                'careers': [],
                'avg_salary': 0,
                'total_growth': 0
            }
        
        industry_data[industry]['careers'].append(career.get('name'))
        industry_data[industry]['total_growth'] += float(career.get('growth_rate', 0))
    
    # Calculate averages
    for industry in industry_data:
        if industry_data[industry]['careers']:
            industry_data[industry]['avg_growth'] = round(
                industry_data[industry]['total_growth'] / 
                len(industry_data[industry]['careers']),
                2
            )
    
    return industry_data
