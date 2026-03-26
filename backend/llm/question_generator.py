"""
LLM-based question generator for career aptitude testing
Uses AI to generate contextual career-related questions
"""

def generate_custom_questions(topic, difficulty='medium', num_questions=5):
    """
    Generate custom quiz questions using LLM
    
    Args:
        topic: Career or skill topic
        difficulty: 'easy', 'medium', 'hard'
        num_questions: Number of questions to generate
    
    Returns:
        List of generated questions
    """
    # This would integrate with OpenAI API or similar
    # For now, returning a template structure
    
    questions = []
    for i in range(num_questions):
        question = {
            'id': f'generated_{topic}_{i}',
            'topic': topic,
            'difficulty': difficulty,
            'question': f'Sample question about {topic} at {difficulty} level - {i+1}',
            'options': [
                'Option A',
                'Option B',
                'Option C',
                'Option D'
            ],
            'correct_answer': 'Option A',
            'explanation': f'This question tests knowledge of {topic}',
            'generated': True
        }
        questions.append(question)
    
    return questions

def generate_adaptive_questions(user_performance, difficulty_level='medium'):
    """
    Generate questions adaptively based on user performance
    
    Args:
        user_performance: User's performance data
        difficulty_level: Current difficulty level
    
    Returns:
        List of adaptively generated questions
    """
    if user_performance >= 0.8:
        next_difficulty = 'hard'
    elif user_performance >= 0.6:
        next_difficulty = 'medium'
    else:
        next_difficulty = 'easy'
    
    questions = generate_custom_questions(
        topic='Career Aptitude',
        difficulty=next_difficulty,
        num_questions=3
    )
    
    return questions

def generate_skill_assessment_questions(skills, num_questions=10):
    """
    Generate skill assessment questions based on provided skills
    
    Args:
        skills: List of skills to assess
        num_questions: Number of questions per skill
    
    Returns:
        List of skill assessment questions
    """
    questions = []
    
    for skill in skills:
        skill_questions = generate_custom_questions(
            topic=skill,
            difficulty='medium',
            num_questions=num_questions // len(skills) if skills else num_questions
        )
        questions.extend(skill_questions)
    
    return questions

def generate_career_compatibility_questions(career, num_questions=5):
    """
    Generate questions to assess compatibility with a specific career
    
    Args:
        career: Career name or ID
        num_questions: Number of questions
    
    Returns:
        List of compatibility assessment questions
    """
    questions = generate_custom_questions(
        topic=f'{career} compatibility',
        difficulty='medium',
        num_questions=num_questions
    )
    
    return questions

def improve_question_quality(question, feedback=None):
    """
    Use LLM to improve question quality based on feedback
    
    Args:
        question: Question dictionary
        feedback: Optional feedback on the question
    
    Returns:
        Improved question dictionary
    """
    improved = question.copy()
    
    if feedback:
        improved['feedback_incorporated'] = True
        improved['revised_question'] = f"{question['question']} [REVISED]"
    
    return improved

def generate_follow_up_questions(initial_answer, analysis_results, num_questions=3):
    """
    Generate follow-up questions based on initial answers and analysis
    
    Args:
        initial_answer: User's initial answer/response
        analysis_results: Analysis of that response
        num_questions: Number of follow-up questions
    
    Returns:
        List of follow-up questions
    """
    follow_ups = []
    
    # Generate questions to explore areas of weakness or interest
    topics = analysis_results.get('focus_areas', ['Career Aptitude'])
    
    for topic in topics[:num_questions]:
        question = {
            'id': f'followup_{topic}',
            'is_follow_up': True,
            'original_topic': initial_answer,
            'follow_up_topic': topic,
            'question': f'Tell us more about {topic}'
        }
        follow_ups.append(question)
    
    return follow_ups
