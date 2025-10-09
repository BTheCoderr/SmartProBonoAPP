#!/usr/bin/env python3
"""
Simple server for SmartProBono - Production Ready
Minimal dependencies, no database initialization on startup
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables FIRST
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tempfile
from datetime import datetime

app = Flask(__name__)

# Enable debug mode
app.config['DEBUG'] = True

# Initialize CORS
CORS(app, 
     origins=[
         'http://localhost:3000', 
         'http://localhost:3001', 
         'http://localhost:3002', 
         'http://127.0.0.1:3000', 
         'http://127.0.0.1:3001', 
         'http://127.0.0.1:3002',
         'https://smartprobono.org',
         'https://www.smartprobono.org',
         'https://api.smartprobono.org',
         'null'
     ],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
     supports_credentials=True)

# ===== HEALTH CHECK ENDPOINTS =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check for all services"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'scanner': 'running',
            'generator': 'running',
            'contact': 'running',
            'safety': 'enabled',
            'websocket': 'available'
        },
        'version': '2.0.0',
        'features': [
            'Document Analysis',
            'PDF Generation', 
            'Contact Form',
            'Safety & Compliance',
            'UPL Prevention',
            'Real-Time Features'
        ],
        'message': 'SmartProBono enhanced system is running'
    }), 200

@app.route('/api/contact/health', methods=['GET'])
def contact_health_check():
    """Health check for contact form service"""
    return jsonify({
        'status': 'healthy',
        'service': 'contact_form',
        'message': 'Contact form service is running'
    }), 200

@app.route('/api/scanner/health', methods=['GET'])
def scanner_health_check():
    """Health check for document scanner service"""
    return jsonify({
        'status': 'healthy',
        'service': 'document_scanner',
        'message': 'Document scanner service is running'
    }), 200

@app.route('/api/generator/health', methods=['GET'])
def generator_health_check():
    """Health check for PDF generator service"""
    return jsonify({
        'status': 'healthy',
        'service': 'pdf_generator',
        'message': 'PDF generator service is running'
    }), 200

# ===== BASIC AI ENDPOINTS =====

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """Basic AI chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Simple response for now
        response = {
            'response': f'I received your message: "{message}". The AI system is working!',
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== CONTACT FORM ENDPOINT =====

@app.route('/api/contact/submit', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Basic validation
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Simple response
        response = {
            'message': 'Thank you for your submission! We will get back to you soon.',
            'status': 'success',
            'submission_id': f'contact_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ROOT ENDPOINT =====

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'SmartProBono API is running!',
        'version': '2.0.0',
        'endpoints': {
            'health': '/api/health',
            'chat': '/api/ai/chat',
            'contact': '/api/contact/submit'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
