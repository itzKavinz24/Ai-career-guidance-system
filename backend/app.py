from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from routes import input, quiz, evaluate, match
from services import matcher
from services.career_analysis import analyze_careers
from llm.career_recommender import generate_career_recommendations

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(input.bp)
app.register_blueprint(quiz.bp)
app.register_blueprint(evaluate.bp)
app.register_blueprint(match.bp)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'ok'}, 200


@app.route('/simulate', methods=['POST'])
def simulate_what_if():
    """What-if simulation endpoint for skill improvement impact."""
    try:
        data = request.get_json() or {}
        selected_skill = data.get('selected_skill')
        current_scores = data.get('current_scores', {})
        interests = data.get('interests', [])

        simulation = matcher.simulate_skill_improvement(
            selected_skill=selected_skill,
            current_scores=current_scores,
            interests=interests,
        )

        return {
            'message': 'Simulation completed',
            'simulation': simulation,
        }, 200
    except ValueError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/generate-careers', methods=['POST'])
def generate_careers():
    """Generate structured career recommendations using Groq with fallback support."""
    try:
        data = request.get_json() or {}
        skills = data.get('skills', {})
        interests = data.get('interests', [])
        top_match = data.get('top_match', [])

        result = generate_career_recommendations(
            skills=skills,
            interests=interests,
            top_match=top_match,
        )

        return {
            'careers': result.get('careers', []),
            'source': result.get('source', 'fallback'),
        }, 200
    except ValueError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/career-analysis', methods=['POST'])
def career_analysis():
    """Generate career insights from backend-calculated scores with Groq enhancement."""
    try:
        data = request.get_json() or {}
        skills = data.get('skills', {})
        result = analyze_careers(skills=skills)

        return {
            'careers': result.get('careers', []),
            'source': result.get('source', 'fallback'),
        }, 200
    except ValueError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
