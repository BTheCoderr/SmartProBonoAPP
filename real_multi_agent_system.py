#!/usr/bin/env python3
"""
SmartProBono - REAL Multi-Layer AI Agent System
Using actual AI models for different legal specializations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

class RealAIAgent:
    """Real AI agent using actual AI models"""
    
    def __init__(self, name, model, system_prompt, api_key=None):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
    
    def generate_response(self, message, context=None):
        """Generate response using actual AI model"""
        try:
            if self.model.startswith('gpt'):
                return self._call_openai(message, context)
            elif self.model.startswith('claude'):
                return self._call_anthropic(message, context)
            elif self.model.startswith('gemini'):
                return self._call_google(message, context)
            else:
                return self._call_ollama(message, context)
        except Exception as e:
            logger.error(f"Error calling {self.model}: {e}")
            return f"I'm sorry, I'm having trouble connecting to my AI model right now. Please try again later."
    
    def _call_openai(self, message, context=None):
        """Call OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")
    
    def _call_anthropic(self, message, context=None):
        """Call Anthropic Claude API"""
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': self.model,
            'max_tokens': 1000,
            'system': self.system_prompt,
            'messages': [
                {'role': 'user', 'content': message}
            ]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['content'][0]['text']
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")
    
    def _call_google(self, message, context=None):
        """Call Google Gemini API"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            'contents': [
                {'parts': [{'text': f"{self.system_prompt}\n\nUser: {message}"}]}
            ],
            'generationConfig': {
                'maxOutputTokens': 1000,
                'temperature': 0.7
            }
        }
        
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"Google API error: {response.status_code}")
    
    def _call_ollama(self, message, context=None):
        """Call local Ollama API"""
        data = {
            'model': self.model,
            'prompt': f"{self.system_prompt}\n\nUser: {message}\nAssistant:",
            'stream': False
        }
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            raise Exception(f"Ollama API error: {response.status_code}")

class RealMultiLayerAgentSystem:
    """Real multi-layer AI agent system with actual AI models"""
    
    def __init__(self):
        self.agents = {
            'greeting': RealAIAgent(
                name="Greeting Agent",
                model="gpt-3.5-turbo",
                system_prompt="""You are a friendly legal assistant. Keep responses brief and helpful.

For greetings like "hello", "hi", "hey":
- Respond warmly but briefly
- Ask what legal help they need
- Don't overwhelm with information

For "what can you do?":
- List 3-4 main capabilities briefly
- Ask what specific help they need

Keep responses under 100 words unless specifically asked for details."""
            ),
            
            'immigration': RealAIAgent(
                name="Immigration Law Expert",
                model="gpt-4",
                system_prompt="""You are an expert immigration attorney with 15+ years of experience. You specialize in:

- Visa applications (work, family, student, tourist)
- Green card processes (family, employment, diversity lottery)
- Citizenship and naturalization
- Asylum and refugee cases
- Deportation defense
- Status changes and extensions

Provide detailed, accurate legal guidance. Always recommend consulting with a qualified immigration attorney for complex cases. Include specific steps, timelines, and requirements when possible."""
            ),
            
            'family': RealAIAgent(
                name="Family Law Expert",
                model="claude-3-sonnet",
                system_prompt="""You are an experienced family law attorney specializing in:

- Divorce and separation
- Child custody and visitation
- Child support calculations
- Spousal support (alimony)
- Property division
- Adoption procedures
- Domestic violence protection

Provide compassionate, practical legal guidance. Always prioritize the best interests of children. Include state-specific information when relevant. Recommend mediation when appropriate."""
            ),
            
            'criminal': RealAIAgent(
                name="Criminal Defense Expert",
                model="gpt-4",
                system_prompt="""You are a criminal defense attorney with extensive experience in:

- Criminal charges and procedures
- Arrest rights and Miranda warnings
- Bail and bond procedures
- Plea negotiations
- Trial preparation
- Sentencing and appeals
- Record expungement

Provide clear guidance on rights and procedures. Always emphasize the importance of legal representation. Include specific steps for emergency situations."""
            ),
            
            'business': RealAIAgent(
                name="Business Law Expert",
                model="gpt-4",
                system_prompt="""You are a business law attorney specializing in:

- Entity formation (LLC, Corporation, Partnership)
- Business contracts and agreements
- Employment law and HR policies
- Intellectual property protection
- Fundraising and securities law
- Compliance and regulatory matters
- Business disputes and litigation

Provide practical business legal guidance. Include cost estimates and timelines when possible. Always recommend proper legal documentation."""
            ),
            
            'compliance': RealAIAgent(
                name="Compliance Expert",
                model="claude-3-sonnet",
                system_prompt="""You are a compliance and regulatory expert specializing in:

- GDPR and data privacy compliance
- SOC 2 and security frameworks
- Industry-specific regulations
- Privacy policy development
- Risk assessments
- Audit preparation
- Regulatory compliance strategies

Provide detailed compliance guidance with specific requirements and implementation steps. Include risk assessments and cost considerations."""
            ),
            
            'document': RealAIAgent(
                name="Document Expert",
                model="gpt-4",
                system_prompt="""You are a legal document specialist with expertise in:

- Legal document drafting
- Contract analysis and review
- Document templates and forms
- Legal writing and formatting
- Document compliance
- Template customization
- Document automation

Provide detailed guidance on document creation and analysis. Include specific clauses and language recommendations. Always emphasize the importance of legal review."""
            ),
            
            'expert': RealAIAgent(
                name="Legal Expert",
                model="gpt-4",
                system_prompt="""You are a senior legal expert who handles complex legal matters requiring expert analysis. You specialize in:

- Complex legal research
- Multi-jurisdictional issues
- High-stakes legal matters
- Expert witness preparation
- Legal strategy development
- Risk assessment and mitigation
- Attorney referrals and case evaluation

Provide comprehensive legal analysis for complex matters. Always recommend consulting with specialized attorneys. Include detailed risk assessments and strategic recommendations."""
            )
        }
    
    def route_message(self, message, context=None):
        """Route message to appropriate AI agent"""
        lower_message = message.lower().strip()
        
        # Context-aware routing
        if context and context.get('conversation_history'):
            history = context['conversation_history']
            if any('immigration' in h.lower() for h in history[-3:]):
                return 'immigration'
            elif any('family' in h.lower() or 'divorce' in h.lower() for h in history[-3:]):
                return 'family'
            elif any('criminal' in h.lower() or 'arrest' in h.lower() for h in history[-3:]):
                return 'criminal'
        
        # Content-based routing
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return 'greeting'
        
        # Immigration patterns
        if any(keyword in lower_message for keyword in ['immigration', 'visa', 'green card', 'citizenship', 'asylum', 'deportation']):
            return 'immigration'
        
        # Family law patterns
        if any(keyword in lower_message for keyword in ['divorce', 'custody', 'child support', 'adoption', 'family law']):
            return 'family'
        
        # Criminal law patterns
        if any(keyword in lower_message for keyword in ['criminal', 'arrest', 'charges', 'court', 'trial', 'sentencing']):
            return 'criminal'
        
        # Compliance patterns
        if any(keyword in lower_message for keyword in ['gdpr', 'privacy', 'data protection', 'soc 2', 'compliance', 'regulatory']):
            return 'compliance'
        
        # Business patterns
        if any(keyword in lower_message for keyword in ['incorporat', 'llc', 'corporation', 'fundraising', 'business', 'startup']):
            return 'business'
        
        # Document patterns
        if any(keyword in lower_message for keyword in ['document', 'contract', 'agreement', 'generate', 'draft', 'template']):
            return 'document'
        
        # Expert patterns (complex questions)
        if len(message.split()) > 15 or any(keyword in lower_message for keyword in ['complex', 'detailed', 'analysis', 'research']):
            return 'expert'
        
        # Default to greeting for simple messages
        return 'greeting'
    
    def process_message(self, message, context=None):
        """Process message through the real multi-layer AI system"""
        try:
            # Route to appropriate agent
            agent_type = self.route_message(message, context)
            agent = self.agents[agent_type]
            
            # Get response from real AI model
            response = agent.generate_response(message, context)
            
            return {
                'response': response,
                'agent_type': agent_type,
                'agent_name': agent.name,
                'model_used': agent.model,
                'confidence': 0.9,  # High confidence for real AI
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in real multi-layer AI system: {e}")
            return {
                'response': "I'm sorry, I encountered an error processing your request. Please try again.",
                'agent_type': 'error',
                'agent_name': 'Error Handler',
                'model_used': 'none',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }

# Initialize the real multi-layer AI system
real_agent_system = RealMultiLayerAgentSystem()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono REAL Multi-Layer AI System is running',
        'version': '4.0.0',
        'ai_system': 'REAL Multi-Layer AI System with actual AI models',
        'models': {
            'greeting': 'gpt-3.5-turbo',
            'immigration': 'gpt-4',
            'family': 'claude-3-sonnet',
            'criminal': 'gpt-4',
            'business': 'gpt-4',
            'compliance': 'claude-3-sonnet',
            'document': 'gpt-4',
            'expert': 'gpt-4'
        }
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Real legal chat with actual AI models"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        context = data.get('context', {})
        
        logger.info(f"💬 Received: {message}")
        
        # Process through real multi-layer AI system
        result = real_agent_system.process_message(message, context)
        
        logger.info(f"🤖 Agent: {result['agent_type']}, Model: {result['model_used']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in legal chat: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'response': "I'm sorry, I encountered an error. Please try again.",
            'agent_type': 'error',
            'agent_name': 'Error Handler'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    print(f"🚀 Starting SmartProBono REAL Multi-Layer AI System")
    print(f"🤖 AI Models: GPT-4, Claude-3-Sonnet, GPT-3.5-Turbo")
    print(f"🎯 Specialized Agents: 8 real AI agents with different models")
    print(f"")
    print(f"Available AI Models:")
    for agent_type, agent in real_agent_system.agents.items():
        print(f"  • {agent.name}: {agent.model}")
    print(f"")
    print(f"🔑 Required API Keys:")
    print(f"  • OPENAI_API_KEY for GPT models")
    print(f"  • ANTHROPIC_API_KEY for Claude models")
    print(f"  • GOOGLE_API_KEY for Gemini models")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    
    app.run(host='0.0.0.0', port=port, debug=False)
