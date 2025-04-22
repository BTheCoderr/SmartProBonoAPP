from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Import routes
from routes.legal_ai import bp as legal_ai
from routes.contracts import contracts
from routes.performance import performance

# Conditionally import uploads if available
try:
    from routes.uploads import uploads
    has_uploads = True
except ImportError:
    logger.warning("Could not import uploads blueprint. Cloudinary integration may not be available.")
    has_uploads = False

# Configure CORS for both development and production
default_origins = ['http://localhost:3000', 'https://smartprobono.netlify.app']
allowed_origins = os.environ.get('ALLOWED_ORIGINS', ','.join(default_origins)).split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins, "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Register blueprints
app.register_blueprint(legal_ai)
app.register_blueprint(contracts)
app.register_blueprint(performance)
if has_uploads:
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
        if not feedback_data:
            return jsonify({'error': 'No feedback data provided'}), 400
            
        # Add timestamp
        feedback_data['timestamp'] = datetime.now().isoformat()
        
        # Save feedback to a JSON file
        filename = f"data/feedback/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(feedback_data, f, indent=2)
            
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
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
                    if feedback:  # Ensure feedback is not None
                        all_feedback.append(feedback)
        
        # Handle empty feedback list
        if not all_feedback:
            return jsonify({
                'total_feedback': 0,
                'average_rating': 0,
                'accuracy_breakdown': {'high': 0, 'medium': 0, 'low': 0},
                'helpfulness_breakdown': {'very': 0, 'somewhat': 0, 'not': 0},
                'clarity_breakdown': {'clear': 0, 'moderate': 0, 'unclear': 0},
                'recent_feedback': []
            }), 200
            
        # Calculate analytics
        analytics = {
            'total_feedback': len(all_feedback),
            'average_rating': sum(f.get('rating', 0) for f in all_feedback) / len(all_feedback),
            'accuracy_breakdown': {
                'high': sum(1 for f in all_feedback if f.get('accuracy') == 'high'),
                'medium': sum(1 for f in all_feedback if f.get('accuracy') == 'medium'),
                'low': sum(1 for f in all_feedback if f.get('accuracy') == 'low')
            },
            'helpfulness_breakdown': {
                'very': sum(1 for f in all_feedback if f.get('helpfulness') == 'very'),
                'somewhat': sum(1 for f in all_feedback if f.get('helpfulness') == 'somewhat'),
                'not': sum(1 for f in all_feedback if f.get('helpfulness') == 'not')
            },
            'clarity_breakdown': {
                'clear': sum(1 for f in all_feedback if f.get('clarity') == 'clear'),
                'moderate': sum(1 for f in all_feedback if f.get('clarity') == 'moderate'),
                'unclear': sum(1 for f in all_feedback if f.get('clarity') == 'unclear')
            },
            'recent_feedback': sorted(all_feedback, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
        }
        
        return jsonify(analytics), 200
    except Exception as e:
        logger.error(f"Error getting feedback analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations', methods=['POST'])
def save_conversation():
    try:
        conversation_data = request.json
        if not conversation_data:
            return jsonify({'error': 'No conversation data provided'}), 400
            
        # Add timestamp if not present
        if 'timestamp' not in conversation_data:
            conversation_data['timestamp'] = datetime.now().isoformat()
        
        # Save conversation to a JSON file
        filename = f"data/conversations/conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)
            
        return jsonify({'message': 'Conversation saved successfully'}), 200
    except Exception as e:
        logger.error(f"Error saving conversation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<user_id>', methods=['GET'])
def get_conversations(user_id):
    try:
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        conversation_files = os.listdir('data/conversations')
        user_conversations = []
        
        for file in conversation_files:
            if file.endswith('.json'):
                with open(f'data/conversations/{file}', 'r') as f:
                    conversation = json.load(f)
                    if conversation and conversation.get('user_id') == user_id:
                        user_conversations.append(conversation)
        
        return jsonify(sorted(user_conversations, key=lambda x: x.get('timestamp', ''), reverse=True)), 200
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)


