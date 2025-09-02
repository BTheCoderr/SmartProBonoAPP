#!/usr/bin/env python3
"""
Simple SmartProBono Backend for Render Deployment
This is a minimal working backend to get smartprobono.org live immediately
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "message": "SmartProBono Backend is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

# Legal chat endpoint
@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        task_type = data.get('task_type', 'chat')
        
        # Simple response for now
        response = {
            "agent_name": "SmartProBono Assistant",
            "agent_type": "general",
            "response": f"I received your message: '{message}'. I'm here to help with legal questions. The advanced multi-agent system is being deployed.",
            "confidence": 0.8,
            "needs_human_review": False,
            "suggestions": [
                "Ask about immigration law",
                "Help with family law matters", 
                "Business legal questions",
                "Document generation help"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "SmartProBono Backend API",
        "status": "running",
        "endpoints": ["/api/health", "/api/legal/chat"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
