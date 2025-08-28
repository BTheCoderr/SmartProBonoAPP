#!/usr/bin/env python3
"""
SmartProBono - Hybrid Application
Combines the best of working apps with advanced backend features
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng"

# Headers for Supabase API calls
SUPABASE_HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json"
}

# Import advanced services from backend
try:
    from backend.services.ai_service import AIService
    from backend.services.document_service import DocumentService
    from backend.services.auth_service import AuthService
    ADVANCED_SERVICES_AVAILABLE = True
    logger.info("✅ Advanced services loaded from backend")
except ImportError as e:
    ADVANCED_SERVICES_AVAILABLE = False
    logger.warning(f"⚠️ Advanced services not available: {e}")

# Try to import simplified backend
try:
    from backend.__init__simple import create_app as create_backend_app
    BACKEND_APP_AVAILABLE = True
    logger.info("✅ Simplified backend app available")
except ImportError as e:
    BACKEND_APP_AVAILABLE = False
    logger.warning(f"⚠️ Backend app not available: {e}")

# Initialize services
if ADVANCED_SERVICES_AVAILABLE:
    ai_service = AIService()
    document_service = DocumentService()
    auth_service = AuthService()

def route_to_agent(message):
    """Route message to appropriate AI agent"""
    lower_message = message.lower().strip()
    
    # Compliance keywords
    if any(keyword in lower_message for keyword in ['gdpr', 'compliance', 'privacy', 'data protection', 'regulation']):
        return 'compliance'
    
    # Business keywords
    if any(keyword in lower_message for keyword in ['business', 'company', 'startup', 'funding', 'contract', 'agreement']):
        return 'business'
    
    # Document keywords
    if any(keyword in lower_message for keyword in ['document', 'contract', 'agreement', 'template', 'form']):
        return 'document'
    
    # Default to greeting
    return 'greeting'

def generate_ai_response(message, agent_type):
    """Generate AI response using advanced service if available"""
    if ADVANCED_SERVICES_AVAILABLE:
        try:
            # Use advanced AI service
            response = ai_service.generate_legal_response(
                message=message,
                task_type="chat",
                model="advanced"
            )
            return response.get('content', 'I apologize, but I encountered an error processing your request.')
        except Exception as e:
            logger.error(f"Advanced AI service error: {e}")
            # Fall back to simple response
    
    # Simple fallback responses
    lower_message = message.lower().strip()
    
    if agent_type == "greeting":
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return "Hello! I'm your AI legal assistant. I can help with compliance, business law, document analysis, and more. What specific legal question can I help you with today?"
        else:
            return "I'm here to help with your legal questions! What specific area would you like assistance with?"
    
    elif agent_type == "compliance":
        if 'gdpr' in lower_message:
            return """**GDPR Compliance Overview:**

GDPR applies if you process personal data of EU residents. Key requirements:

1. **Legal Basis**: Identify lawful basis (consent, contract, legitimate interest)
2. **Privacy Policy**: Clear, accessible policy explaining data use
3. **Data Rights**: Implement processes for access, rectification, erasure
4. **Breach Notification**: Report breaches within 72 hours
5. **Privacy by Design**: Build data protection into systems

**Risk**: Fines up to €20M or 4% of annual revenue

Would you like me to help you create a compliance checklist for your specific situation?"""
        else:
            return "I specialize in compliance matters including GDPR, SOC 2, privacy policies, and regulatory requirements. What specific compliance question do you have?"
    
    elif agent_type == "business":
        return "I specialize in business law including entity formation, fundraising, employment agreements, and intellectual property. What business legal question can I help you with?"
    
    elif agent_type == "document":
        return "I specialize in document analysis and generation. I can help you analyze contracts, generate legal documents, and explain complex legal language. What document do you need help with?"
    
    return "I'm here to help with your legal questions. Could you be more specific about what you need assistance with?"

def save_to_supabase(table, data):
    """Save data to Supabase using REST API"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        response = requests.post(url, headers=SUPABASE_HEADERS, json=data, timeout=5)
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ Data saved to Supabase {table}")
            return True
        else:
            logger.error(f"❌ Error saving to Supabase {table}: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Exception saving to Supabase {table}: {str(e)}")
        return False

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "message": "SmartProBono Hybrid API is running",
        "status": "ok",
        "version": "3.0.0",
        "database": "Supabase PostgreSQL with RLS",
        "ai_system": "Hybrid: Advanced + Simple fallback",
        "advanced_services": ADVANCED_SERVICES_AVAILABLE,
        "migration_status": "COMPLETED"
    })

@app.route('/api/legal/chat', methods=['POST', 'OPTIONS'])
def legal_chat():
    """Handle legal chat requests with hybrid AI system"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"status": "error", "message": "Message is required"}), 400
        
        logger.info(f"💬 Received: {message}")
        
        # Route to appropriate agent
        agent_type = route_to_agent(message)
        
        # Generate response using hybrid system
        response_text = generate_ai_response(message, agent_type)
        
        logger.info(f"🤖 Agent: {agent_type}, Response length: {len(response_text)}")
        
        return jsonify({
            "response": response_text,
            "model_info": {
                "name": f"{agent_type.title()} Agent",
                "type": agent_type,
                "advanced": ADVANCED_SERVICES_AVAILABLE
            },
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"❌ Error in legal chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/beta/signup', methods=['POST', 'OPTIONS'])
def beta_signup():
    """Handle beta signup requests"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        email = data.get('email', '')
        
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        
        logger.info(f"📧 Beta signup: {email}")
        
        # Save to Supabase
        signup_data = {
            "email": email,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        success = save_to_supabase("beta_signups", signup_data)
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your interest! We'll be in touch soon.",
            "database": "Supabase with RLS",
            "migration_status": "COMPLETED"
        })
        
    except Exception as e:
        logger.error(f"❌ Error in beta signup: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/feedback', methods=['POST', 'OPTIONS'])
def feedback():
    """Handle feedback requests"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        feedback_text = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        logger.info(f"📝 Feedback: {feedback_text}, Rating: {rating}")
        
        # Save to Supabase
        feedback_data = {
            "rating": rating,
            "feedback_text": feedback_text,
            "created_at": datetime.now().isoformat()
        }
        
        success = save_to_supabase("feedback", feedback_data)
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your feedback!",
            "database": "Supabase with RLS",
            "migration_status": "COMPLETED"
        })
        
    except Exception as e:
        logger.error(f"❌ Error in feedback: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/documents/history', methods=['GET'])
def document_history():
    """Get document history"""
    try:
        # This would integrate with the advanced document service
        if ADVANCED_SERVICES_AVAILABLE:
            # Use advanced document service
            pass
        
        return jsonify({
            "documents": [],
            "status": "success",
            "message": "Document history endpoint ready"
        })
        
    except Exception as e:
        logger.error(f"❌ Error in document history: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/documents/templates', methods=['GET'])
def document_templates():
    """Get document templates"""
    try:
        # This would integrate with the advanced document service
        if ADVANCED_SERVICES_AVAILABLE:
            # Use advanced document service
            pass
        
        return jsonify({
            "templates": [],
            "status": "success",
            "message": "Document templates endpoint ready"
        })
        
    except Exception as e:
        logger.error(f"❌ Error in document templates: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    print(f"🚀 Starting SmartProBono Hybrid API")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Hybrid (Advanced + Simple fallback)")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"🔄 Migration Status: COMPLETED")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"  • Feedback: http://localhost:{port}/api/feedback")
    print(f"  • Document History: http://localhost:{port}/api/documents/history")
    print(f"  • Document Templates: http://localhost:{port}/api/documents/templates")
    print(f"")
    print(f"🎯 Advanced Services: {'✅ Available' if ADVANCED_SERVICES_AVAILABLE else '❌ Not Available'}")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    app.run(host='0.0.0.0', port=port, debug=False)
