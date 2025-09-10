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

# Import the unified API route
try:
    from backend.routes.unified_api import bp as unified_api_bp
    app.register_blueprint(unified_api_bp)
    print("✅ Unified API routes registered")
except ImportError as e:
    print(f"❌ Unified API routes not available: {e}")

# Import the legacy legal AI route for backward compatibility
try:
    from backend.routes.legal_ai import bp as legal_ai_bp
    app.register_blueprint(legal_ai_bp, url_prefix='/api/legal')
    print("✅ Legacy Legal AI routes registered")
except ImportError as e:
    print(f"❌ Legacy Legal AI routes not available: {e}")

# Import the Virtual Paralegal CRM routes
try:
    from backend.routes.virtual_paralegal_crm import bp as virtual_paralegal_crm_bp
    app.register_blueprint(virtual_paralegal_crm_bp)
    print("✅ Virtual Paralegal CRM routes registered")
except ImportError as e:
    print(f"❌ Virtual Paralegal CRM routes not available: {e}")

# Import the AI Virtual Paralegal routes
try:
    from backend.routes.ai_virtual_paralegal import bp as ai_virtual_paralegal_bp
    app.register_blueprint(ai_virtual_paralegal_bp)
    print("✅ AI Virtual Paralegal routes registered")
except ImportError as e:
    print(f"❌ AI Virtual Paralegal routes not available: {e}")

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Legal AI Test Server",
        "endpoints": [
            "GET /api/v1/health - Health check",
            "POST /api/v1/legal/analyze - Unified legal analysis",
            "POST /api/v1/ai/chat - AI chat",
            "POST /api/v1/documents/scan - Document scanning",
            "POST /api/legal/legal-analysis - Legacy legal analysis",
            "POST /api/legal/chat - Legacy chat"
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
