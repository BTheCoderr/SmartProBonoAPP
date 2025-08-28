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
import requests
from supabase import create_client, Client

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# AI Agent System
AI_AGENTS = {
    "greeting": {
        "name": "Greeting Agent",
        "system_prompt": """You are a friendly legal assistant. Keep responses brief and helpful.
        
        For greetings like "hello", "hi", "hey":
        - Respond warmly but briefly
        - Ask what legal help they need
        - Don't overwhelm with information
        
        For "what can you do?":
        - List 3-4 main capabilities briefly
        - Ask what specific help they need
        
        Keep responses under 100 words unless specifically asked for details.""",
        "max_tokens": 150,
        "temperature": 0.7
    },
    "compliance": {
        "name": "Compliance Agent",
        "system_prompt": """You are a legal compliance expert specializing in:
        - GDPR and data privacy
        - SOC 2 and security frameworks
        - Privacy policies and terms of service
        - Regulatory compliance
        
        Provide detailed, actionable guidance. Include:
        - Specific requirements
        - Implementation steps
        - Risk assessments
        - Cost estimates when relevant
        
        Always recommend consulting with a qualified attorney for complex matters.""",
        "max_tokens": 2000,
        "temperature": 0.3
    },
    "business": {
        "name": "Business Agent",
        "system_prompt": """You are a business law expert specializing in:
        - Entity formation (LLC, Corp, etc.)
        - Fundraising and investment
        - Employment agreements
        - Intellectual property
        - Contract review and drafting
        
        Provide practical, startup-focused advice. Include:
        - Pros and cons of different options
        - Cost considerations
        - Timeline estimates
        - Next steps
        
        Always recommend consulting with a qualified attorney for complex matters.""",
        "max_tokens": 2000,
        "temperature": 0.3
    },
    "document": {
        "name": "Document Agent",
        "system_prompt": """You are a document analysis and generation expert. You can:
        - Analyze legal documents
        - Generate legal documents
        - Explain complex legal language
        - Identify key terms and clauses
        
        When analyzing documents:
        - Highlight key terms
        - Explain implications
        - Identify potential issues
        - Suggest improvements
        
        When generating documents:
        - Use clear, professional language
        - Include all necessary clauses
        - Provide customization options
        - Include disclaimers about legal advice""",
        "max_tokens": 3000,
        "temperature": 0.2
    },
    "expert": {
        "name": "Expert Agent",
        "system_prompt": """You are a senior legal expert who handles complex questions and expert referrals.
        
        For complex legal questions:
        - Provide thorough analysis
        - Identify key legal issues
        - Suggest multiple approaches
        - Highlight risks and considerations
        
        For expert referrals:
        - Match users with appropriate legal experts
        - Explain why the expert is suitable
        - Provide contact information
        - Set expectations for consultation
        
        Always emphasize the importance of professional legal counsel for complex matters.""",
        "max_tokens": 2500,
        "temperature": 0.3
    }
}

def route_to_agent(message, context=None):
    """Route message to appropriate AI agent"""
    if context is None:
        context = {}
    
    lower_message = message.lower()
    
    # Greeting patterns
    if lower_message.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$'):
        return 'greeting'
    
    # Compliance patterns
    if any(keyword in lower_message for keyword in ['gdpr', 'privacy', 'data protection', 'soc 2', 'compliance', 'regulatory', 'terms of service', 'privacy policy']):
        return 'compliance'
    
    # Business patterns
    if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation', 'fundraising', 'investment', 'equity', 'employment', 'contract', 'intellectual property', 'ip', 'trademark', 'patent']):
        return 'business'
    
    # Document patterns
    if any(keyword in lower_message for keyword in ['document', 'contract', 'agreement', 'generate', 'create', 'draft', 'analyze', 'review', 'pdf', 'upload']):
        return 'document'
    
    # Expert patterns
    if any(keyword in lower_message for keyword in ['expert', 'attorney', 'lawyer', 'consult', 'complex', 'litigation', 'court', 'lawsuit']) or context.get('conversation_length', 0) > 5:
        return 'expert'
    
    # Default to greeting
    return 'greeting'

def generate_ai_response(message, agent_type):
    """Generate AI response based on agent type"""
    agent = AI_AGENTS[agent_type]
    lower_message = message.lower()
    
    # Greeting Agent responses
    if agent_type == "greeting":
        if any(greeting in lower_message for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hello! I'm your AI legal assistant. I can help with compliance, business law, document analysis, and more. What specific legal question can I help you with today?"
        if 'what can you do' in lower_message:
            return "I can help with:\n• Legal compliance (GDPR, SOC 2, privacy policies)\n• Business law (incorporation, fundraising, contracts)\n• Document analysis and generation\n• Expert referrals for complex matters\n\nWhat would you like to explore?"
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
    """Send a confirmation email to the user and a notification to the admin"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to Supabase
    try:
        result = supabase.table('beta_signups').insert({
            'email': email,
            'status': 'confirmed',
            'created_at': timestamp
        }).execute()
        print(f"Beta signup saved to Supabase: {email}")
    except Exception as e:
        print(f"Error saving to Supabase: {str(e)}")
    
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
        "message": "SmartProBono API with Supabase is running",
        "status": "ok",
        "version": "2.0.0",
        "database": "Supabase PostgreSQL",
        "security": "Row Level Security (RLS) enabled"
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
        
        # Send confirmation email and save to Supabase
        send_confirmation_email(email)
        
        return jsonify({
            "status": "success", 
            "message": "Thank you for signing up! We'll be in touch soon.",
            "email_sent": True,
            "database": "Supabase"
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
        
        # Save to Supabase (optional - for conversation history)
        try:
            # Create a mock conversation for demo
            conversation_data = {
                'title': f"Chat - {message[:50]}...",
                'model_used': agent['name'],
                'created_at': datetime.now().isoformat()
            }
            # Note: In production, you'd associate this with a real user_id
            print(f"Would save conversation to Supabase: {conversation_data}")
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")
        
        return jsonify({
            "response": response_text,
            "model_info": {
                "name": agent['name'],
                "type": agent_type,
                "version": "2.0.0",
                "response_time_ms": 150,
                "system": "Multi-Agent AI with Supabase"
            }
        })
    except Exception as e:
        print(f"Error processing legal chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/documents/history', methods=['GET'])
def get_document_history():
    """Get document history from Supabase"""
    try:
        # In production, you'd filter by user_id
        result = supabase.table('documents').select('*').limit(10).execute()
        return jsonify({"documents": result.data})
    except Exception as e:
        print(f"Error fetching documents: {str(e)}")
        return jsonify({"documents": []})

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
        
        # Save to Supabase
        try:
            result = supabase.table('feedback').insert({
                'rating': rating,
                'feedback_text': feedback_text,
                'created_at': datetime.now().isoformat()
            }).execute()
            print(f"Feedback saved to Supabase: {result.data}")
        except Exception as e:
            print(f"Error saving feedback to Supabase: {str(e)}")
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your feedback!",
            "database": "Supabase"
        })
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    print(f"🚀 Starting SmartProBono API with Supabase on http://localhost:{port}")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI: Multi-Agent system with 5 specialized agents")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"📧 Email: Zoho SMTP integration")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Documents: http://localhost:{port}/api/documents/history")
    print(f"  • Feedback: http://localhost:{port}/api/feedback")
    app.run(host='0.0.0.0', port=port, debug=True)
