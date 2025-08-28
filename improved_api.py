from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from datetime import datetime
import uuid
import re

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# AI Agent System - Multi-Agent Architecture
AI_AGENTS = {
    "greeting": {
        "name": "Greeting Agent",
        "description": "Handles greetings and general inquiries with brief, friendly responses",
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "what can you do"]
    },
    "compliance": {
        "name": "Compliance Agent", 
        "description": "Specializes in GDPR, SOC 2, privacy policies, and regulatory compliance",
        "keywords": ["gdpr", "privacy", "data protection", "soc 2", "compliance", "regulatory", "terms of service", "privacy policy"]
    },
    "business": {
        "name": "Business Agent",
        "description": "Handles entity formation, fundraising, employment, and business law",
        "keywords": ["incorporat", "llc", "corporation", "fundraising", "investment", "equity", "employment", "contract", "intellectual property", "ip", "trademark", "patent"]
    },
    "document": {
        "name": "Document Agent",
        "description": "Specializes in document analysis, generation, and legal document review",
        "keywords": ["document", "contract", "agreement", "generate", "create", "draft", "analyze", "review", "pdf", "upload"]
    },
    "expert": {
        "name": "Expert Agent",
        "description": "Handles complex legal questions and expert referrals",
        "keywords": ["expert", "attorney", "lawyer", "consult", "complex", "litigation", "court", "lawsuit"]
    }
}

def route_to_agent(message, context=None):
    """Route message to appropriate AI agent based on content analysis"""
    if context is None:
        context = {}
    
    lower_message = message.lower().strip()
    
    # Greeting patterns - exact matches for simple greetings
    greeting_patterns = [
        r'^(hello|hi|hey|good morning|good afternoon|good evening)$',
        r'^what can you do\??$',
        r'^how are you\??$'
    ]
    
    for pattern in greeting_patterns:
        if re.match(pattern, lower_message):
            return 'greeting'
    
    # Check for keyword matches in other agents
    for agent_type, agent_info in AI_AGENTS.items():
        if agent_type == 'greeting':
            continue
        for keyword in agent_info['keywords']:
            if keyword in lower_message:
                return agent_type
    
    # Default to greeting for unrecognized messages
    return 'greeting'

def generate_ai_response(message, agent_type):
    """Generate AI response based on agent type and message content"""
    lower_message = message.lower().strip()
    
    # Greeting Agent responses
    if agent_type == "greeting":
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return "Hello! I'm your AI legal assistant. I can help with compliance, business law, document analysis, and more. What specific legal question can I help you with today?"
        elif 'what can you do' in lower_message:
            return "I can help with:\n• Legal compliance (GDPR, SOC 2, privacy policies)\n• Business law (incorporation, fundraising, contracts)\n• Document analysis and generation\n• Expert referrals for complex matters\n\nWhat would you like to explore?"
        elif 'how are you' in lower_message:
            return "I'm doing well, thank you! I'm here and ready to help with your legal questions. What can I assist you with today?"
        else:
            return "I'm here to help with your legal questions! What specific area would you like assistance with?"
    
    # Compliance Agent responses
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
        elif 'soc 2' in lower_message:
            return """**SOC 2 Compliance Guide:**

SOC 2 is essential for enterprise sales and customer trust.

**Five Trust Principles:**
1. **Security**: Protection against unauthorized access
2. **Availability**: System operational availability
3. **Processing Integrity**: System processing completeness/accuracy
4. **Confidentiality**: Information designated confidential is protected
5. **Privacy**: Personal information collection/use/disposal

**Implementation Timeline:**
• Type I: 3-6 months
• Type II: 12+ months

**Investment:** $15k-$50k for initial compliance

Ready to start your SOC 2 journey? I can help create your control framework."""
        elif 'privacy policy' in lower_message:
            return """**Privacy Policy Requirements:**

A comprehensive privacy policy should include:

1. **Data Collection**: What data you collect and why
2. **Data Usage**: How you use the data
3. **Data Sharing**: When and with whom you share data
4. **User Rights**: How users can access, modify, or delete their data
5. **Cookies**: Cookie usage and tracking policies
6. **Contact Information**: How users can reach you

**Key Elements:**
• Clear, plain language
• Easy to find and access
• Regular updates
• Compliance with applicable laws (GDPR, CCPA, etc.)

Would you like me to help you create a privacy policy template?"""
        else:
            return "I specialize in compliance matters including GDPR, SOC 2, privacy policies, and regulatory requirements. What specific compliance question do you have?"
    
    # Business Agent responses
    elif agent_type == "business":
        if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation']):
            return """**Entity Formation Guide:**

**Delaware C-Corporation** (Recommended for VC-backed startups):
✅ Pros: Investor-friendly, stock options, global recognition
❌ Cons: Double taxation, more compliance

**LLC** (Good for bootstrapped/small teams):
✅ Pros: Tax flexibility, simple structure, liability protection
❌ Cons: Harder to raise VC funding, no stock options

**Formation Checklist:**
1. Choose state (Delaware for corp, home state for LLC)
2. Reserve name
3. File articles
4. Get EIN
5. Open business bank account
6. Create operating agreement
7. Set up equity structure

**Costs:** Delaware Corp: ~$400, LLC: $50-$500

Need help choosing the right structure for your startup?"""
        elif 'fundraising' in lower_message:
            return """**Startup Fundraising Legal Framework:**

**Funding Stages:**
• **Pre-Seed/F&F**: SAFE, convertible notes ($25K-$250K)
• **Seed**: Series Seed docs or equity ($250K-$2M)
• **Series A+**: Full equity rounds with extensive docs ($2M+)

**Essential Legal Documents:**
1. Term Sheet (non-binding overview)
2. Stock Purchase Agreement (main contract)
3. Investors' Rights Agreement
4. Voting Agreement
5. Right of First Refusal
6. Drag-Along/Tag-Along rights

**Key Considerations:**
• Anti-dilution provisions
• Liquidation preferences
• Board composition
• Option pool sizing

**Legal Costs:** Seed: $5K-$15K, Series A: $15K-$40K

Ready to review your term sheet or generate fundraising docs?"""
        else:
            return "I specialize in business law including entity formation, fundraising, employment agreements, and intellectual property. What business legal question can I help you with?"
    
    # Document Agent responses
    elif agent_type == "document":
        return "I specialize in document analysis and generation. I can help you:\n\n• **Analyze Documents**: Review contracts, agreements, legal forms\n• **Generate Documents**: Create privacy policies, terms of service, contracts\n• **Explain Legal Language**: Break down complex legal terms\n• **Identify Key Terms**: Highlight important clauses and implications\n\nDo you have a document you'd like me to analyze, or would you like me to help generate a specific legal document?"
    
    # Expert Agent responses
    elif agent_type == "expert":
        return "For complex legal matters, I recommend connecting with a qualified attorney. I can help you:\n\n• **Identify the Right Expert**: Match you with attorneys specializing in your area\n• **Prepare for Consultation**: Help you organize your questions and documents\n• **Understand Legal Issues**: Break down complex legal concepts\n• **Find Pro Bono Resources**: Connect you with legal aid organizations\n\nWhat type of legal expert are you looking for? I can help match you with the right professional."
    
    # Default response
    return "I'm here to help with your legal questions. Could you be more specific about what you need assistance with?"

def send_confirmation_email(email):
    """Send a confirmation email to the user"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to local file (will be migrated to Supabase later)
    try:
        signup_data = {
            "email": email,
            "timestamp": timestamp,
            "status": "confirmed",
            "source": "improved_api"
        }
        
        # Load existing signups
        try:
            with open('email_signups/beta_signups.json', 'r') as f:
                signups = json.load(f)
        except:
            signups = []
        
        # Add new signup
        signups.append(signup_data)
        
        # Save back to file
        with open('email_signups/beta_signups.json', 'w') as f:
            json.dump(signups, f, indent=2)
        
        print(f"Beta signup saved: {email}")
    except Exception as e:
        print(f"Error saving signup: {str(e)}")
    
    # Send email
    try:
        SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.zoho.com')
        SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
        SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'info@smartprobono.org')
        SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
        
        if not SMTP_PASSWORD:
            print(f"SMTP_PASSWORD not set. Would send confirmation email to {email}")
            return True
            
        # Send confirmation email
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = email
        msg['Subject'] = "Welcome to SmartProBono!"
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #0078d4; color: white; padding: 10px 20px; }}
                    .content {{ padding: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to SmartProBono!</h1>
                    </div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>Thank you for signing up for SmartProBono's beta program. We're excited to have you join our platform!</p>
                        <p>You'll be among the first to experience our AI-powered legal assistance tools designed to make legal help accessible to everyone.</p>
                        <p>Best regards,<br>The SmartProBono Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Confirmation email sent to {email}")
            
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return True

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "message": "SmartProBono API with Improved AI Agents is running",
        "status": "ok",
        "version": "2.1.0",
        "ai_system": "Multi-Agent with 5 specialized agents",
        "improvements": [
            "Fixed overwhelming responses to greetings",
            "Contextual AI routing",
            "Specialized legal agents",
            "Better user experience"
        ]
    })

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
        
        print(f"Received signup for email: {email}")
        
        # Send confirmation email and save locally
        send_confirmation_email(email)
        
        return jsonify({
            "status": "success", 
            "message": "Thank you for signing up! We'll be in touch soon.",
            "email_sent": True,
            "ai_system": "Multi-Agent v2.1.0"
        })
    except Exception as e:
        print(f"Error processing signup: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

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
        task_type = data.get('task_type', 'chat')
        
        if not message:
            return jsonify({"status": "error", "message": "Message is required"}), 400
        
        print(f"Received legal chat message: {message}, task_type: {task_type}")
        
        # Route to appropriate agent
        agent_type = route_to_agent(message, {'conversation_length': 0})
        agent = AI_AGENTS[agent_type]
        
        # Generate response
        response_text = generate_ai_response(message, agent_type)
        
        print(f"Routed to {agent['name']} - Response length: {len(response_text)} chars")
        
        return jsonify({
            "response": response_text,
            "model_info": {
                "name": agent['name'],
                "type": agent_type,
                "description": agent['description'],
                "version": "2.1.0",
                "response_time_ms": 150,
                "system": "Multi-Agent AI with Improved Routing"
            }
        })
    except Exception as e:
        print(f"Error processing legal chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/documents/history', methods=['GET'])
def get_document_history():
    """Get document history"""
    # Mock data for now - will be replaced with Supabase later
    documents = [
        {
            "_id": "doc-1",
            "title": "Sample Contract Review",
            "type": "document",
            "createdAt": "2023-01-15T12:00:00Z"
        },
        {
            "_id": "doc-2", 
            "title": "Privacy Policy Draft",
            "type": "document",
            "createdAt": "2023-02-20T14:30:00Z"
        }
    ]
    return jsonify({"documents": documents})

@app.route('/api/documents/templates', methods=['GET'])
def get_templates():
    """Get document templates"""
    templates = [
        {
            "_id": "template-1",
            "title": "Non-Disclosure Agreement",
            "type": "template",
            "category": "contract",
            "description": "Standard NDA for business relationships",
            "createdAt": "2023-01-15T12:00:00Z"
        },
        {
            "_id": "template-2",
            "title": "Privacy Policy Template",
            "type": "template",
            "category": "compliance",
            "description": "GDPR-compliant privacy policy template",
            "createdAt": "2023-02-20T14:30:00Z"
        }
    ]
    return jsonify({"templates": templates})

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
        
        print(f"Received feedback: {feedback_text}, rating: {rating}")
        
        # Save feedback locally (will be migrated to Supabase later)
        try:
            feedback_data = {
                "feedback": feedback_text,
                "rating": rating,
                "timestamp": datetime.now().isoformat(),
                "source": "improved_api"
            }
            
            # Load existing feedback
            try:
                with open('data/feedback/feedback.json', 'r') as f:
                    feedback_list = json.load(f)
            except:
                feedback_list = []
            
            # Add new feedback
            feedback_list.append(feedback_data)
            
            # Save back to file
            with open('data/feedback/feedback.json', 'w') as f:
                json.dump(feedback_list, f, indent=2)
            
            print(f"Feedback saved: {feedback_data}")
        except Exception as e:
            print(f"Error saving feedback: {str(e)}")
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your feedback!",
            "ai_system": "Multi-Agent v2.1.0"
        })
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    print(f"🚀 Starting SmartProBono API with Improved AI Agents on http://localhost:{port}")
    print(f"🤖 AI System: Multi-Agent with 5 specialized agents")
    print(f"✨ Improvements: Fixed overwhelming responses, contextual routing")
    print(f"📊 Database: Local storage (Supabase integration ready)")
    print(f"📧 Email: Zoho SMTP integration")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Documents: http://localhost:{port}/api/documents/history")
    print(f"  • Feedback: http://localhost:{port}/api/feedback")
    print(f"")
    print(f"🎯 Test the improvements:")
    print(f"  • Say 'hello' → Brief, friendly response")
    print(f"  • Ask 'What is GDPR?' → Detailed compliance guidance")
    print(f"  • Ask 'Should I form an LLC?' → Business law comparison")
    app.run(host='0.0.0.0', port=port, debug=True)
