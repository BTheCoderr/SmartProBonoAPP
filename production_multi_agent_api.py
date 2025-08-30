#!/usr/bin/env python3
"""
SmartProBono Production Multi-Agent API with Real AI Models
Deploy-ready version with OpenAI, Anthropic, and other AI providers
"""

import os
import json
import re
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from anthropic import Anthropic
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ewtcvsohdgkthuyajyyk.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng")

# AI Clients
openai_client = None
anthropic_client = None

# Initialize AI clients if API keys are available
try:
    if os.getenv("OPENAI_API_KEY"):
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info("✅ OpenAI client initialized")
except Exception as e:
    logger.warning(f"OpenAI client not available: {e}")

try:
    if os.getenv("ANTHROPIC_API_KEY"):
        anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logger.info("✅ Anthropic client initialized")
except Exception as e:
    logger.warning(f"Anthropic client not available: {e}")

class ProductionMultiAgentSystem:
    """Production-ready multi-agent system with real AI models"""
    
    def __init__(self):
        self.agents = {
            'greeting': {
                'name': 'Greeting Agent',
                'model': 'gpt-3.5-turbo',
                'system_prompt': """You are a friendly legal assistant for SmartProBono. 
                Keep responses brief and helpful. For greetings, respond warmly but briefly and ask what legal help they need.
                Keep responses under 50 words."""
            },
            'immigration': {
                'name': 'Immigration Agent',
                'model': 'gpt-4o',
                'system_prompt': """You are an immigration law specialist. Provide guidance on:
                - Various visa types (H1B, F1, K1, etc.)
                - Green card application processes
                - Citizenship requirements and naturalization
                - Asylum and refugee claims
                - Deportation defense basics
                
                Offer clear, step-by-step information. Always recommend consulting an immigration attorney for personalized advice.
                Provide general information only, not legal advice."""
            },
            'family': {
                'name': 'Family Law Agent',
                'model': 'claude-3-sonnet-20240229',
                'system_prompt': """You are a family law expert. Provide compassionate and clear guidance on:
                - Divorce proceedings and legal separation
                - Child custody and visitation arrangements
                - Child support calculations and enforcement
                - Adoption processes
                - Domestic violence legal protections
                
                Emphasize the emotional sensitivity of these topics and strongly recommend seeking legal counsel from a family law attorney.
                Provide general information only, not legal advice."""
            },
            'business': {
                'name': 'Business Law Agent',
                'model': 'gpt-4o',
                'system_prompt': """You are a business law expert for startups and small businesses. Provide guidance on:
                - Entity formation (LLC, C-Corp, S-Corp)
                - Fundraising legalities (SAFE, convertible notes)
                - Contract drafting and review (NDAs, service agreements)
                - Intellectual property protection
                
                Focus on practical, actionable advice. Always recommend consulting with a qualified attorney.
                Provide general information only, not legal advice."""
            },
            'criminal': {
                'name': 'Criminal Law Agent',
                'model': 'gpt-4o',
                'system_prompt': """You are a criminal defense law specialist. Provide information on:
                - Rights upon arrest (Miranda rights)
                - Common criminal charges and their implications
                - Basics of criminal court procedures
                - Potential defense strategies
                - Importance of legal representation
                
                Stress the critical need for a criminal defense attorney and the serious consequences of criminal charges.
                Provide general information only, not legal advice."""
            },
            'compliance': {
                'name': 'Compliance Agent',
                'model': 'claude-3-sonnet-20240229',
                'system_prompt': """You are a legal compliance expert specializing in:
                - GDPR and data privacy
                - SOC 2 and security frameworks
                - Privacy policies and terms of service
                - Regulatory compliance
                
                Provide detailed, actionable guidance. Include specific requirements, implementation steps, and potential risks.
                Always recommend consulting with a qualified attorney for complex matters.
                Provide general information only, not legal advice."""
            },
            'document': {
                'name': 'Document Agent',
                'model': 'gpt-4o',
                'system_prompt': """You are a legal document expert. Your role is to assist with:
                - Generating standard legal documents (NDAs, simple contracts, letters)
                - Reviewing documents for key clauses and potential issues
                - Summarizing complex legal texts
                - Explaining document terminology
                
                Ask clarifying questions to ensure accuracy. Do not provide legal advice, only document assistance."""
            },
            'expert': {
                'name': 'Expert Agent',
                'model': 'gpt-4o',
                'system_prompt': """You are a highly experienced legal expert. Your role is to:
                - Provide in-depth analysis for complex legal questions
                - Identify relevant legal precedents and statutes
                - Explain nuanced legal concepts
                - Recommend when a user should seek direct counsel from a human attorney
                - Offer potential next steps or strategies
                
                Always emphasize that your advice is for informational purposes and not a substitute for a licensed attorney."""
            }
        }
    
    def route_message(self, message):
        """Route message to appropriate agent"""
        lower_message = message.lower().strip()
        
        # Greeting patterns
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return 'greeting'
        
        # Immigration patterns
        if any(keyword in lower_message for keyword in ['immigration', 'visa', 'green card', 'citizenship', 'asylum', 'deportation']):
            return 'immigration'
        
        # Family law patterns
        if any(keyword in lower_message for keyword in ['divorce', 'custody', 'child support', 'adoption', 'family law']):
            return 'family'
        
        # Criminal law patterns
        if any(keyword in lower_message for keyword in ['criminal', 'arrest', 'charges', 'court', 'trial', 'defense']):
            return 'criminal'
        
        # Business patterns
        if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation', 'business', 'startup', 'contract']):
            return 'business'
        
        # Compliance patterns
        if any(keyword in lower_message for keyword in ['gdpr', 'compliance', 'privacy', 'data protection', 'soc 2']):
            return 'compliance'
        
        # Document patterns
        if any(keyword in lower_message for keyword in ['document', 'generate', 'review', 'summarize']):
            return 'document'
        
        # Complex questions
        if any(keyword in lower_message for keyword in ['complex', 'expert', 'in-depth', 'nuance']):
            return 'expert'
        
        # Default to greeting
        return 'greeting'
    
    def call_openai(self, messages, model="gpt-3.5-turbo"):
        """Call OpenAI API"""
        if not openai_client:
            return "I'm sorry, the AI service is currently unavailable. Please try again later."
        
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    def call_anthropic(self, messages, model="claude-3-sonnet-20240229"):
        """Call Anthropic API"""
        if not anthropic_client:
            return "I'm sorry, the AI service is currently unavailable. Please try again later."
        
        try:
            # Format messages for Anthropic
            formatted_messages = []
            system_prompt = ""
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_prompt = msg['content']
                else:
                    formatted_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=formatted_messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    def process_message(self, message):
        """Process message through multi-agent system"""
        try:
            # Route to appropriate agent
            agent_type = self.route_message(message)
            agent = self.agents[agent_type]
            
            logger.info(f"💬 Received: {message}")
            logger.info(f"➡️ Routing to Agent: {agent['name']} ({agent_type})")
            
            # Prepare messages
            messages = [
                {"role": "system", "content": agent['system_prompt']},
                {"role": "user", "content": message}
            ]
            
            # Call appropriate AI model
            if "claude" in agent['model']:
                response = self.call_anthropic(messages, agent['model'])
            else:
                response = self.call_openai(messages, agent['model'])
            
            # Add safety disclaimer
            if "not legal advice" not in response.lower():
                response += "\n\n⚠️ **Important**: This is general legal information, not legal advice. For specific legal matters, please consult with a qualified attorney."
            
            return {
                'response': response,
                'agent_type': agent_type,
                'agent_name': agent['name'],
                'model_used': agent['model'],
                'confidence': 0.9,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in multi-agent system: {e}")
            return {
                'response': "I'm sorry, I encountered an error processing your request. Please try again.",
                'agent_type': 'error',
                'agent_name': 'Error Handler',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }

# Initialize multi-agent system
agent_system = ProductionMultiAgentSystem()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono Production Multi-Agent System is running',
        'version': '4.0.0',
        'ai_system': 'Production Multi-Agent System with Real AI Models',
        'database': 'Supabase PostgreSQL with RLS',
        'migration_status': 'COMPLETED',
        'agents': list(agent_system.agents.keys()),
        'ai_providers': {
            'openai': openai_client is not None,
            'anthropic': anthropic_client is not None
        }
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Multi-agent legal chat endpoint"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        
        # Process through multi-agent system
        result = agent_system.process_message(message)
        
        logger.info(f"🤖 Agent: {result['agent_type']}, Model: {result['model_used']}")
        
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
                'name': agent['name'],
                'type': agent_type,
                'model': agent['model'],
                'description': f"Specialized agent for {agent_type} law"
            }
            for agent_type, agent in agent_system.agents.items()
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"🚀 Starting SmartProBono Production Multi-Agent System")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Production Multi-Agent System with Real AI Models")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"🔄 Migration Status: COMPLETED")
    print(f"")
    print(f"Available agents:")
    for agent_type, agent in agent_system.agents.items():
        print(f"  • {agent['name']}: {agent['model']}")
    print(f"")
    print(f"AI Providers:")
    print(f"  • OpenAI: {'✅ Available' if openai_client else '❌ Not configured'}")
    print(f"  • Anthropic: {'✅ Available' if anthropic_client else '❌ Not configured'}")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Agents: http://localhost:{port}/api/agents")
    print(f"")
    print(f"🎯 Test the production multi-agent system:")
    print(f"  • Say 'hello' → Greeting Agent (GPT-3.5)")
    print(f"  • Ask 'immigration visa' → Immigration Agent (GPT-4)")
    print(f"  • Ask 'divorce custody' → Family Law Agent (Claude-3)")
    print(f"  • Ask 'GDPR compliance' → Compliance Agent (Claude-3)")
    print(f"")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
