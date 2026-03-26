import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from services import trends


_SCORING_EXECUTOR = ThreadPoolExecutor(max_workers=2)
_SCORING_LOCK = threading.Lock()
_SCORING_JOBS = {}


def _normalize_skill(skill):
    return (skill or '').strip().lower()


def _tokenize(skill):
    return set(_normalize_skill(skill).replace('/', ' ').replace('-', ' ').split())


def _build_demand_index():
    demand_data = trends.get_in_demand_skills()
    demand_index = {}
    max_frequency = 1

    for item in demand_data:
        skill = _normalize_skill(item.get('skill', ''))
        frequency = int(item.get('frequency', 0))
        if skill:
            demand_index[skill] = frequency
            max_frequency = max(max_frequency, frequency)

    return demand_index, max_frequency


def _skill_demand_ratio(skill, demand_index, max_frequency):
    normalized_skill = _normalize_skill(skill)
    if not normalized_skill or not demand_index:
        return 0.0

    exact_frequency = demand_index.get(normalized_skill)
    if exact_frequency is not None:
        return exact_frequency / max_frequency

    # Fuzzy token overlap for skills not exactly in the index.
    skill_tokens = _tokenize(normalized_skill)
    best_ratio = 0.0

    for demand_skill, frequency in demand_index.items():
        demand_tokens = _tokenize(demand_skill)
        if not skill_tokens or not demand_tokens:
            continue

        overlap = len(skill_tokens & demand_tokens)
        if overlap == 0:
            continue

        token_ratio = overlap / len(skill_tokens)
        weighted_ratio = token_ratio * (frequency / max_frequency)
        best_ratio = max(best_ratio, weighted_ratio)

    return best_ratio


def _demand_reasoning(skill, raw_ratio):
    if raw_ratio >= 0.8:
        return f"{skill} is strongly represented across fast-growing careers, so demand is very high."
    if raw_ratio >= 0.5:
        return f"{skill} appears in several in-demand roles and has solid market traction."
    if raw_ratio >= 0.25:
        return f"{skill} has moderate demand and can become stronger when paired with complementary skills."
    return f"{skill} currently has lower direct demand signal in this dataset; consider adjacent high-demand skills."


def _compute_relative_demand_scores(skills):
    # Simulate asynchronous demand-based scoring work.
    time.sleep(1.0)

    demand_index, max_frequency = _build_demand_index()
    scored = []

    for skill in skills:
        raw_ratio = _skill_demand_ratio(skill, demand_index, max_frequency)
        demand_score = round(raw_ratio * 100, 2)
        scored.append({
            'skill': skill,
            'demand_score': demand_score,
            'raw_ratio': raw_ratio,
        })

    highest_score = max((item['demand_score'] for item in scored), default=1)
    if highest_score <= 0:
        highest_score = 1

    evaluated = []
    for item in scored:
        relative_score = round((item['demand_score'] / highest_score) * 100, 2)
        evaluated.append({
            'skill': item['skill'],
            'relative_demand_score': relative_score,
            'market_demand_score': item['demand_score'],
            'level': get_proficiency_level(relative_score),
            'reasoning': _demand_reasoning(item['skill'], item['raw_ratio']),
            'scoring_basis': 'relative_market_demand',
        })

    evaluated.sort(key=lambda x: x['relative_demand_score'], reverse=True)
    return evaluated


def _run_scoring_job(job_id, skills):
    with _SCORING_LOCK:
        _SCORING_JOBS[job_id]['status'] = 'processing'
        _SCORING_JOBS[job_id]['started_at'] = datetime.utcnow().isoformat()

    try:
        result = _compute_relative_demand_scores(skills)
        with _SCORING_LOCK:
            _SCORING_JOBS[job_id]['status'] = 'completed'
            _SCORING_JOBS[job_id]['completed_at'] = datetime.utcnow().isoformat()
            _SCORING_JOBS[job_id]['result'] = result
    except Exception as error:
        with _SCORING_LOCK:
            _SCORING_JOBS[job_id]['status'] = 'failed'
            _SCORING_JOBS[job_id]['completed_at'] = datetime.utcnow().isoformat()
            _SCORING_JOBS[job_id]['error'] = str(error)


def start_demand_scoring_job(skills, user_id=None):
    """Start background demand scoring and return a job id."""
    job_id = str(uuid.uuid4())
    payload = {
        'job_id': job_id,
        'user_id': user_id,
        'status': 'queued',
        'created_at': datetime.utcnow().isoformat(),
        'skills': skills,
        'result': None,
        'error': None,
    }

    with _SCORING_LOCK:
        _SCORING_JOBS[job_id] = payload

    _SCORING_EXECUTOR.submit(_run_scoring_job, job_id, skills)
    return job_id


def get_demand_scoring_job(job_id):
    with _SCORING_LOCK:
        job = _SCORING_JOBS.get(job_id)
        if not job:
            return None
        return dict(job)


def evaluate_skill_set(skills):
    """
    Evaluate skills against market demand.

    This is kept synchronous for compatibility with existing callers,
    while the route can use start_demand_scoring_job for true background work.
    """
    return _compute_relative_demand_scores(skills)

def get_proficiency_level(score):
    """
    Get proficiency level based on score
    
    Args:
        score: Proficiency score (0-100)
    
    Returns:
        Proficiency level string
    """
    if score >= 90:
        return 'Expert'
    elif score >= 75:
        return 'Advanced'
    elif score >= 60:
        return 'Intermediate'
    elif score >= 40:
        return 'Beginner'
    else:
        return 'Novice'

def calculate_quiz_score(answers, time_taken=0):
    """
    Calculate quiz score based on answers and time taken
    
    Args:
        answers: List of answer records
        time_taken: Time taken in seconds
    
    Returns:
        Score dictionary
    """
    total = len(answers)
    correct = sum(1 for a in answers if a.get('is_correct', False))
    
    base_score = (correct / total * 100) if total > 0 else 0
    
    # Bonus points for faster completion (within reasonable time)
    time_bonus = 0
    if time_taken > 0:
        avg_time_per_question = time_taken / total if total > 0 else 0
        if avg_time_per_question < 30:  # Less than 30 seconds per question
            time_bonus = 5
    
    final_score = min(100, base_score + time_bonus)
    
    return {
        'base_score': round(base_score, 2),
        'time_taken': time_taken,
        'time_bonus': time_bonus,
        'final_score': round(final_score, 2),
        'percentage': round(final_score, 2)
    }

def generate_assessment(skills_score, quiz_score, interests):
    """
    Generate overall assessment combining multiple factors
    
    Args:
        skills_score: Score from skills evaluation
        quiz_score: Score from quiz
        interests: List of interests
    
    Returns:
        Assessment dictionary
    """
    avg_score = (skills_score + quiz_score) / 2
    
    assessment = {
        'overall_score': round(avg_score, 2),
        'skills_score': skills_score,
        'quiz_score': quiz_score,
        'readiness_level': get_readiness_level(avg_score),
        'assessment_date': __import__('datetime').datetime.now().isoformat(),
        'interests_count': len(interests)
    }
    
    return assessment

def get_readiness_level(score):
    """
    Get readiness level for career guidance
    
    Args:
        score: Overall assessment score
    
    Returns:
        Readiness level string
    """
    if score >= 85:
        return 'Highly Ready'
    elif score >= 70:
        return 'Ready'
    elif score >= 55:
        return 'Moderately Ready'
    elif score >= 40:
        return 'Developing'
    else:
        return 'Early Stage'

def analyze_strengths_weaknesses(skills, quiz_results):
    """
    Analyze user strengths and weaknesses
    
    Args:
        skills: List of skills with proficiency scores
        quiz_results: Quiz performance data
    
    Returns:
        Analysis dictionary with strengths and weaknesses
    """
    # Find strong skills
    evaluated_skills = evaluate_skill_set(skills)
    strong_skills = [s for s in evaluated_skills if s['relative_demand_score'] >= 75]
    weak_skills = [s for s in evaluated_skills if s['relative_demand_score'] < 60]
    
    # Find strong and weak quiz topics
    strong_topics = quiz_results.get('strong_areas', [])
    weak_topics = quiz_results.get('weak_areas', [])
    
    return {
        'strengths': {
            'skills': [s['skill'] for s in strong_skills],
            'quiz_topics': strong_topics,
            'overall_strengths': len(strong_skills) + len(strong_topics)
        },
        'weaknesses': {
            'skills': [s['skill'] for s in weak_skills],
            'quiz_topics': weak_topics,
            'overall_weaknesses': len(weak_skills) + len(weak_topics)
        },
        'development_areas': weak_skills + weak_topics,
        'recommendations': generate_recommendations(weak_skills, weak_topics)
    }

def generate_recommendations(weak_skills, weak_topics):
    """
    Generate recommendations for improvement
    
    Args:
        weak_skills: List of weak skills
        weak_topics: List of weak quiz topics
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    for skill in weak_skills:
        recommendations.append(f"Improve {skill['skill']} through practice and training courses")
    
    for topic in weak_topics:
        recommendations.append(f"Study and strengthen knowledge in {topic}")
    
    if not recommendations:
        recommendations.append("Continue building on your strong foundation")
    
    return recommendations
