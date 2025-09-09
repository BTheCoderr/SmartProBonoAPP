#!/usr/bin/env python3
"""
Simple test server for Legal AI Integration
This server only includes the legal AI routes for testing
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the legal_ai_backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'legal_ai_backend'))

# Add the backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3002'])

# Import the legal AI route
try:
    from backend.routes.legal_ai import bp as legal_ai_bp
    app.register_blueprint(legal_ai_bp, url_prefix='/api/legal')
    print("✅ Legal AI routes registered")
except ImportError as e:
    print(f"❌ Legal AI routes not available: {e}")

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Legal AI Test Server",
        "endpoints": [
            "POST /api/legal/legal-analysis",
            "POST /api/legal/chat",
            "GET /api/legal/models"
        ]
    })

@app.route('/test')
def test_endpoint():
    return jsonify({
        "message": "Legal AI Test Server is running",
        "legal_ai_available": "LEGAL_AI_AVAILABLE" in globals()
    })

if __name__ == '__main__':
    print("🚀 Starting Legal AI Test Server...")
    print("Available endpoints:")
    print("  POST /api/legal/legal-analysis - Main legal analysis endpoint")
    print("  POST /api/legal/chat - Basic chat endpoint")
    print("  GET /api/legal/models - Available models")
    print("  GET /test - Test endpoint")
    print()
    app.run(host='0.0.0.0', port=3001, debug=True)
