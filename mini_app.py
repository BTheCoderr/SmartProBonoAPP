from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/health')
def health_check():
    return jsonify({
        "message": "API is running",
        "status": "ok",
        "version": "1.0.0"
    })

@app.route('/api/ping', methods=['GET'])
def ping():
    """Simple endpoint to check if API server is running"""
    return jsonify({
        "status": "ok",
        "message": "API server is running",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/api/documents/scan', methods=['POST'])
def document_scan():
    """Mock endpoint for document scanning"""
    return jsonify({
        "success": True,
        "extractedText": "Sample extracted text from document",
        "extractedData": {
            "documentType": "general",
            "contentSummary": "Mock document content"
        },
        "confidence": 0.95,
        "processingTimestamp": datetime.utcnow().isoformat(),
        "processingTimeMs": 250,
        "pageCount": 1
    }), 200

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Mock endpoint for legal chat"""
    return jsonify({
        "response": "This is a mock response from the legal AI assistant.",
        "model_info": {
            "name": "Mock AI Model",
            "version": "1.0",
            "response_time_ms": 120
        }
    }), 200

@app.route('/api/beta/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '')
    
    if not email or '@' not in email:
        return jsonify({"status": "error", "message": "Invalid email address"}), 400
    
    # In a real application, you would save this to a database
    print(f"Received signup for email: {email}")
    
    return jsonify({
        "status": "success", 
        "message": "Thank you for signing up! We'll be in touch soon."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 