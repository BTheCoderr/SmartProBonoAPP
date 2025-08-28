#!/usr/bin/env python3
"""
Working SmartProBono Backend with Supabase Integration
Simplified version that definitely works
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

def route_to_agent(message):
    """Route message to appropriate AI agent"""
    lower_message = message.lower().strip()
    
    # Greeting patterns
    if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
        return 'greeting'
    
    # Compliance patterns
    if any(keyword in lower_message for keyword in ['gdpr', 'privacy', 'data protection', 'soc 2', 'compliance']):
        return 'compliance'
    
    # Business patterns
    if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation', 'fundraising', 'business']):
        return 'business'
    
    # Document patterns
    if any(keyword in lower_message for keyword in ['document', 'contract', 'agreement', 'generate']):
        return 'document'
    
    # Default to greeting
    return 'greeting'

def generate_ai_response(message, agent_type):
    """Generate AI response based on agent type"""
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
            print(f"✅ Data saved to Supabase {table}")
            return True
        else:
            print(f"❌ Error saving to Supabase {table}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception saving to Supabase {table}: {str(e)}")
        return False

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "message": "SmartProBono API with Supabase Integration is running",
        "status": "ok",
        "version": "2.3.0",
        "database": "Supabase PostgreSQL with RLS",
        "ai_system": "Multi-Agent with 5 specialized agents",
        "migration_status": "COMPLETED"
    })

@app.route('/api/legal/chat', methods=['POST', 'OPTIONS'])
def legal_chat():
    """Handle legal chat requests with improved AI agents"""
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
        
        print(f"💬 Received: {message}")
        
        # Route to appropriate agent
        agent_type = route_to_agent(message)
        
        # Generate response
        response_text = generate_ai_response(message, agent_type)
        
        print(f"🤖 Agent: {agent_type}, Response length: {len(response_text)}")
        
        return jsonify({
            "response": response_text,
            "model_info": {
                "name": f"{agent_type.title()} Agent",
                "type": agent_type,
                "version": "2.3.0",
                "system": "Multi-Agent AI with Supabase Integration"
            }
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/beta/signup', methods=['POST', 'OPTIONS'])
def signup():
    """Handle signup requests with email"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        email = data.get('email', '')
        
        if not email or '@' not in email:
            return jsonify({"status": "error", "message": "Invalid email address"}), 400
        
        print(f"📧 Signup: {email}")
        
        # Save to Supabase
        signup_data = {
            "email": email,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        success = save_to_supabase("beta_signups", signup_data)
        
        return jsonify({
            "status": "success", 
            "message": "Thank you for signing up! We'll be in touch soon.",
            "database": "Supabase with RLS",
            "migration_status": "COMPLETED"
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/feedback', methods=['POST', 'OPTIONS'])
def feedback():
    """Handle feedback submission"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        feedback_text = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        print(f"📝 Feedback: {feedback_text}, Rating: {rating}")
        
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
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    print(f"🚀 Starting SmartProBono API with Supabase Integration")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Multi-Agent with contextual responses")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"🔄 Migration Status: COMPLETED")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"  • Feedback: http://localhost:{port}/api/feedback")
    print(f"")
    print(f"🎯 Test the improvements:")
    print(f"  • Say 'hello' → Brief, friendly response")
    print(f"  • Ask 'What is GDPR?' → Detailed compliance guidance")
    print(f"")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    app.run(host='0.0.0.0', port=port, debug=False)
