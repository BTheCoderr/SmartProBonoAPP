from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.legal_ai import bp as legal_ai
from routes.contracts import contracts
from routes.performance import performance
from routes.uploads import uploads
from dotenv import load_dotenv
import os
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS for both development and production
default_origins = ['http://localhost:3000', 'https://smartprobono.netlify.app']
allowed_origins = os.environ.get('ALLOWED_ORIGINS', ','.join(default_origins)).split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins, "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Register blueprints
app.register_blueprint(legal_ai)
app.register_blueprint(contracts)
app.register_blueprint(performance)
app.register_blueprint(uploads)

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
    os.makedirs('data/feedback')
    os.makedirs('data/conversations')

@app.route('/')
def home():
    return 'SmartProBono API is running!'

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = request.json
        # Add timestamp
        feedback_data['timestamp'] = datetime.now().isoformat()
        
        # Save feedback to a JSON file
        filename = f"data/feedback/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(feedback_data, f, indent=2)
            
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/analytics', methods=['GET'])
def get_feedback_analytics():
    try:
        feedback_files = os.listdir('data/feedback')
        all_feedback = []
        
        for file in feedback_files:
            if file.endswith('.json'):
                with open(f'data/feedback/{file}', 'r') as f:
                    feedback = json.load(f)
                    all_feedback.append(feedback)
        
        # Calculate analytics
        analytics = {
            'total_feedback': len(all_feedback),
            'average_rating': sum(f['rating'] for f in all_feedback) / len(all_feedback) if all_feedback else 0,
            'accuracy_breakdown': {
                'high': sum(1 for f in all_feedback if f['accuracy'] == 'high'),
                'medium': sum(1 for f in all_feedback if f['accuracy'] == 'medium'),
                'low': sum(1 for f in all_feedback if f['accuracy'] == 'low')
            },
            'helpfulness_breakdown': {
                'very': sum(1 for f in all_feedback if f['helpfulness'] == 'very'),
                'somewhat': sum(1 for f in all_feedback if f['helpfulness'] == 'somewhat'),
                'not': sum(1 for f in all_feedback if f['helpfulness'] == 'not')
            },
            'clarity_breakdown': {
                'clear': sum(1 for f in all_feedback if f['clarity'] == 'clear'),
                'moderate': sum(1 for f in all_feedback if f['clarity'] == 'moderate'),
                'unclear': sum(1 for f in all_feedback if f['clarity'] == 'unclear')
            },
            'recent_feedback': sorted(all_feedback, key=lambda x: x['timestamp'], reverse=True)[:10]
        }
        
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations', methods=['POST'])
def save_conversation():
    try:
        conversation_data = request.json
        # Add timestamp if not present
        if 'timestamp' not in conversation_data:
            conversation_data['timestamp'] = datetime.now().isoformat()
        
        # Save conversation to a JSON file
        filename = f"data/conversations/conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)
            
        return jsonify({'message': 'Conversation saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<user_id>', methods=['GET'])
def get_conversations(user_id):
    try:
        conversation_files = os.listdir('data/conversations')
        user_conversations = []
        
        for file in conversation_files:
            if file.endswith('.json'):
                with open(f'data/conversations/{file}', 'r') as f:
                    conversation = json.load(f)
                    if conversation.get('user_id') == user_id:
                        user_conversations.append(conversation)
        
        return jsonify(sorted(user_conversations, key=lambda x: x['timestamp'], reverse=True)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)


