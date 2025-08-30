#!/usr/bin/env python3
"""
SmartProBono Multi-Agent Integration
Integrates with existing backend and adds multi-agent capabilities
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng"

class MultiAgentSystem:
    """Multi-agent system for legal assistance"""
    
    def __init__(self):
        self.agents = {
            'intake': self.intake_agent,
            'research': self.research_agent,
            'drafting': self.drafting_agent,
            'safety': self.safety_agent
        }
    
    def route_message(self, message):
        """Route message to appropriate agent"""
        lower_message = message.lower().strip()
        
        # Greeting patterns
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return 'intake'
        
        # Immigration patterns
        if any(keyword in lower_message for keyword in ['immigration', 'visa', 'green card', 'citizenship', 'asylum']):
            return 'research'
        
        # Family law patterns
        if any(keyword in lower_message for keyword in ['divorce', 'custody', 'child support', 'adoption', 'family law']):
            return 'research'
        
        # Criminal law patterns
        if any(keyword in lower_message for keyword in ['criminal', 'arrest', 'charges', 'court', 'trial']):
            return 'research'
        
        # Business patterns
        if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation', 'business', 'startup']):
            return 'research'
        
        # Document patterns
        if any(keyword in lower_message for keyword in ['document', 'contract', 'agreement', 'generate']):
            return 'drafting'
        
        # Default to intake
        return 'intake'
    
    def intake_agent(self, message):
        """Intake agent: normalize questions and extract jurisdiction"""
        lower_message = message.lower().strip()
        
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return {
                'response': "Hello! I'm your AI legal assistant. I can help with various legal matters including immigration, family law, business law, and compliance. What specific legal question can I help you with today?",
                'agent': 'intake',
                'jurisdiction': None,
                'confidence': 0.9
            }
        
        # Extract jurisdiction
        jurisdiction_patterns = [
            r'\b(MA|Massachusetts|RI|Rhode Island|CT|Connecticut|NY|New York|CA|California|TX|Texas|FL|Florida)\b',
            r'\b(federal|state|local)\b'
        ]
        
        jurisdiction = None
        for pattern in jurisdiction_patterns:
            match = re.search(pattern, message, flags=re.I)
            if match:
                jurisdiction = match.group(0)
                break
        
        return {
            'response': f"I understand you're asking about: {message}. I'll route this to our research agent for detailed assistance.",
            'agent': 'intake',
            'jurisdiction': jurisdiction,
            'confidence': 0.8
        }
    
    def research_agent(self, message):
        """Research agent: provide detailed legal information"""
        lower_message = message.lower().strip()
        
        if 'immigration' in lower_message or 'visa' in lower_message:
            return {
                'response': """**Immigration Law Assistance:**

I can help with various immigration matters:

• **Visa Applications**: Work, family, student, tourist visas
• **Green Card Process**: Family, employment, diversity lottery
• **Citizenship**: Naturalization requirements and process
• **Asylum**: Refugee status and protection
• **Deportation Defense**: Removal proceedings

**Important**: Immigration law is complex and constantly changing. For specific cases, I recommend consulting with a qualified immigration attorney.

What specific immigration matter can I help you with?""",
                'agent': 'research',
                'jurisdiction': 'federal',
                'confidence': 0.9
            }
        
        elif 'family' in lower_message or 'divorce' in lower_message:
            return {
                'response': """**Family Law Assistance:**

I can help with family law matters:

• **Divorce**: Process, property division, support
• **Child Custody**: Arrangements, modifications
• **Child Support**: Calculations, enforcement
• **Adoption**: Process, requirements, costs
• **Domestic Violence**: Protection orders, safety

**Important**: Family law varies by state. For specific cases, I recommend consulting with a qualified family law attorney.

What specific family law matter can I assist you with?""",
                'agent': 'research',
                'jurisdiction': 'state',
                'confidence': 0.9
            }
        
        elif 'criminal' in lower_message or 'arrest' in lower_message:
            return {
                'response': """**Criminal Law Information:**

I can provide information about:

• **Your Rights**: What to do if arrested
• **Criminal Charges**: Understanding charges and procedures
• **Court Process**: Criminal court procedures
• **Defense Strategies**: Legal defense options
• **Record Expungement**: Clearing criminal records

**Important**: If you're facing criminal charges, you should immediately consult with a criminal defense attorney. This is general information only.

What specific criminal law matter can I help you with?""",
                'agent': 'research',
                'jurisdiction': 'state',
                'confidence': 0.9
            }
        
        else:
            return {
                'response': f"I understand you're asking about: {message}. This appears to be a legal question that requires research. Let me provide some general guidance and recommend consulting with an attorney for specific advice.",
                'agent': 'research',
                'jurisdiction': 'general',
                'confidence': 0.7
            }
    
    def drafting_agent(self, message):
        """Drafting agent: generate legal documents and responses"""
        return {
            'response': f"""**Document Generation Assistance:**

I can help with:

• **Legal Document Templates**: Contracts, agreements, letters
• **Document Analysis**: Review and analysis of legal documents
• **Form Completion**: Assistance with legal forms
• **Document Customization**: Tailoring documents to your needs

**Important**: Generated documents are templates and should be reviewed by an attorney for your specific situation.

What type of document do you need help with?""",
            'agent': 'drafting',
            'jurisdiction': 'general',
            'confidence': 0.8
        }
    
    def safety_agent(self, response_data):
        """Safety agent: check for unauthorized legal advice"""
        response = response_data.get('response', '')
        lower_response = response.lower()
        
        # Check for advice-giving language
        advice_patterns = [
            r'\b(i advise|i recommend|you should|you must|you need to)\b',
            r'\b(file .* by|plead .*|sign .*|submit form)\b',
            r'\b(this constitutes legal advice|this is legal advice)\b'
        ]
        
        needs_escalation = False
        for pattern in advice_patterns:
            if re.search(pattern, lower_response):
                needs_escalation = True
                break
        
        # Add disclaimer if needed
        if needs_escalation or 'attorney' not in lower_response:
            response += "\n\n⚠️ **Important**: This is general legal information, not legal advice. For specific legal matters, please consult with a qualified attorney."
        
        response_data['response'] = response
        response_data['escalate'] = needs_escalation
        response_data['safety_checked'] = True
        
        return response_data
    
    def process_message(self, message):
        """Process message through multi-agent system"""
        try:
            # Route to appropriate agent
            agent_type = self.route_message(message)
            agent_func = self.agents[agent_type]
            
            # Get initial response
            response_data = agent_func(message)
            
            # Safety check
            response_data = self.safety_agent(response_data)
            
            # Add metadata
            response_data.update({
                'timestamp': datetime.now().isoformat(),
                'processing_time': 0.1,  # Simulated
                'system': 'multi-agent'
            })
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error in multi-agent system: {e}")
            return {
                'response': "I'm sorry, I encountered an error processing your request. Please try again.",
                'agent': 'error',
                'confidence': 0.0,
                'escalate': True,
                'error': str(e)
            }

# Initialize multi-agent system
agent_system = MultiAgentSystem()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono Multi-Agent System is running',
        'version': '1.0.0',
        'system': 'Multi-Agent Legal AI',
        'agents': list(agent_system.agents.keys())
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Multi-agent legal chat endpoint"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        logger.info(f"💬 Received: {message}")
        
        # Process through multi-agent system
        result = agent_system.process_message(message)
        
        logger.info(f"🤖 Agent: {result['agent']}, Confidence: {result['confidence']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in legal chat: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'response': "I'm sorry, I encountered an error. Please try again."
        }), 500

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get information about available agents"""
    return jsonify({
        'agents': [
            {
                'name': 'Intake Agent',
                'description': 'Normalizes user questions and extracts jurisdiction',
                'type': 'intake'
            },
            {
                'name': 'Research Agent', 
                'description': 'Provides detailed legal information and guidance',
                'type': 'research'
            },
            {
                'name': 'Drafting Agent',
                'description': 'Generates legal documents and templates',
                'type': 'drafting'
            },
            {
                'name': 'Safety Agent',
                'description': 'Ensures compliance and prevents unauthorized legal advice',
                'type': 'safety'
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    print(f"🚀 Starting SmartProBono Multi-Agent System")
    print(f"🤖 Agents: {list(agent_system.agents.keys())}")
    print(f"🔗 Supabase: {SUPABASE_URL}")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Agents: http://localhost:{port}/api/agents")
    print(f"")
    print(f"🎯 Test the multi-agent system:")
    print(f"  • Say 'hello' → Intake Agent")
    print(f"  • Ask 'immigration visa' → Research Agent")
    print(f"  • Ask 'divorce custody' → Research Agent")
    print(f"  • Ask 'generate contract' → Drafting Agent")
    
    app.run(host='0.0.0.0', port=port, debug=False)
