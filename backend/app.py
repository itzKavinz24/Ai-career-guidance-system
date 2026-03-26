from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes import input, quiz, evaluate, match

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
