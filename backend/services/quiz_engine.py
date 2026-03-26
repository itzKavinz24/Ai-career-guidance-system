import json
import os
from datetime import datetime

# Load questions from JSON file
def _load_questions():
    """Load questions from JSON file"""
    try:
        with open('data/questions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

QUESTIONS_DB = _load_questions()
USER_RESPONSES = {}


def _topic_matches_skills(topic, skills):
    """Return True when a question topic is relevant to at least one skill."""
    topic_text = (topic or '').lower()
    normalized_skills = [(skill or '').lower() for skill in skills]

    # Basic topic-to-skill keyword expansion for broader matching.
    topic_keywords = {
        'programming': ['python', 'javascript', 'java', 'c++', 'coding', 'software'],
        'web-development': ['web', 'frontend', 'backend', 'javascript', 'react', 'css'],
        'database': ['sql', 'database', 'data analysis', 'analytics'],
        'machine-learning': ['machine learning', 'ml', 'ai', 'data science'],
        'cloud-computing': ['cloud', 'aws', 'azure', 'gcp', 'devops'],
        'problem-solving': ['problem solving', 'logic', 'critical thinking'],
        'career-aptitude': ['career', 'communication', 'leadership', 'management'],
    }

    keyword_pool = set([topic_text])
    keyword_pool.update(topic_keywords.get(topic_text, []))

    for skill in normalized_skills:
        if not skill:
            continue
        for keyword in keyword_pool:
            if keyword and (keyword in skill or skill in keyword):
                return True
    return False

def get_quiz_questions(difficulty='medium', num_questions=10):
    """
    Get quiz questions filtered by difficulty
    
    Args:
        difficulty: 'easy', 'medium', 'hard'
        num_questions: Number of questions to return
    
    Returns:
        List of questions
    """
    filtered = [q for q in QUESTIONS_DB if q.get('difficulty') == difficulty]
    return filtered[:num_questions]


def get_skill_based_questions(skills, difficulty='medium', num_questions=10):
    """
    Get questions prioritized by skill-relevant topics.

    Args:
        skills: List of user-entered skills
        difficulty: desired difficulty
        num_questions: total questions to return

    Returns:
        List of skill-specific questions with fallback questions
    """
    if not skills:
        return get_quiz_questions(difficulty=difficulty, num_questions=num_questions)

    difficulty_filtered = [q for q in QUESTIONS_DB if q.get('difficulty') == difficulty]
    relevant = [q for q in difficulty_filtered if _topic_matches_skills(q.get('topic', ''), skills)]

    selected = relevant[:num_questions]
    if len(selected) < num_questions:
        seen_ids = {q.get('id') for q in selected}
        fallback_pool = [q for q in difficulty_filtered if q.get('id') not in seen_ids]
        selected.extend(fallback_pool[: max(0, num_questions - len(selected))])

    # Final fallback across all difficulties if dataset is small.
    if len(selected) < num_questions:
        seen_ids = {q.get('id') for q in selected}
        all_fallback = [q for q in QUESTIONS_DB if q.get('id') not in seen_ids]
        selected.extend(all_fallback[: max(0, num_questions - len(selected))])

    return selected[:num_questions]

def validate_answer(question_id, answer):
    """
    Validate if the answer is correct
    
    Args:
        question_id: ID of the question
        answer: User's answer
    
    Returns:
        Boolean indicating if answer is correct
    """
    for question in QUESTIONS_DB:
        if question.get('id') == question_id:
            correct_answer = question.get('correct_answer')
            is_correct = answer.lower() == correct_answer.lower()
            return is_correct
    return False

def get_question(question_id):
    """
    Get a specific question by ID
    
    Args:
        question_id: ID of the question
    
    Returns:
        Question object or None
    """
    for question in QUESTIONS_DB:
        if question.get('id') == question_id:
            return question
    return None

def record_answer(user_id, question_id, answer, is_correct):
    """
    Record user's answer
    
    Args:
        user_id: User ID
        question_id: Question ID
        answer: User's answer
        is_correct: Whether answer is correct
    """
    if user_id not in USER_RESPONSES:
        USER_RESPONSES[user_id] = []
    
    USER_RESPONSES[user_id].append({
        'question_id': question_id,
        'answer': answer,
        'is_correct': is_correct,
        'timestamp': datetime.now().isoformat()
    })

def calculate_results(user_id):
    """
    Calculate quiz results for a user
    
    Args:
        user_id: User ID
    
    Returns:
        Results dictionary with scores
    """
    if user_id not in USER_RESPONSES:
        return {
            'user_id': user_id,
            'total_questions': 0,
            'correct_answers': 0,
            'score': 0,
            'percentage': 0
        }
    
    responses = USER_RESPONSES[user_id]
    total = len(responses)
    correct = sum(1 for r in responses if r['is_correct'])
    percentage = (correct / total * 100) if total > 0 else 0
    
    return {
        'user_id': user_id,
        'total_questions': total,
        'correct_answers': correct,
        'score': correct,
        'percentage': round(percentage, 2)
    }

def get_quiz_analysis(user_id):
    """
    Get detailed analysis of quiz performance
    
    Args:
        user_id: User ID
    
    Returns:
        Detailed analysis dictionary
    """
    if user_id not in USER_RESPONSES:
        return None
    
    responses = USER_RESPONSES[user_id]
    
    # Categorize by topic
    topics = {}
    for response in responses:
        question = get_question(response['question_id'])
        if question:
            topic = question.get('topic', 'general')
            if topic not in topics:
                topics[topic] = {'correct': 0, 'total': 0}
            topics[topic]['total'] += 1
            if response['is_correct']:
                topics[topic]['correct'] += 1
    
    return {
        'user_id': user_id,
        'topics': topics,
        'strong_areas': [k for k, v in topics.items() if v['correct'] == v['total']],
        'weak_areas': [k for k, v in topics.items() if v['correct'] < v['total'] * 0.5]
    }
