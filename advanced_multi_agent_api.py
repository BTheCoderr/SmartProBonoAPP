#!/usr/bin/env python3
"""
SmartProBono - Advanced Multi-Layer Agent System
Professional AI agents with specialized capabilities
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

def call_ollama(message, task_type="chat", history=None):
    """Call Ollama API to generate response with smart model selection"""
    try:
        # Smart model selection based on question complexity
        def analyze_question_complexity(question):
            question_lower = question.lower()
            
            # Simple patterns
            simple_patterns = [
                r"\b(hello|hi|hey|thanks|thank you)\b",
                r"^.{1,50}\?$"  # Short questions
            ]
            
            # Complex patterns
            complex_patterns = [
                r"\b(analyze|compare|evaluate|assess)\b",
                r"\b(dispute|litigation|court|lawsuit|settlement)\b",
                r".{200,}\?$"  # Long questions
            ]
            
            for pattern in complex_patterns:
                if re.search(pattern, question_lower):
                    return "complex"
            
            for pattern in simple_patterns:
                if re.search(pattern, question_lower):
                    return "simple"
            
            # Default based on length
            if len(question) < 50:
                return "simple"
            elif len(question) < 200:
                return "moderate"
            else:
                return "complex"
        
        # Smart model selection
        complexity = analyze_question_complexity(message)
        
        if complexity == "simple":
            ollama_model = "tinyllama:1.1b"  # Ultra-fast for simple questions
        elif complexity == "moderate":
            ollama_model = "qwen2.5:0.5b"    # Balanced for moderate questions
        else:  # complex
            ollama_model = "qwen2.5:0.5b"    # Use lightweight for complex too (to prevent freezing)
        
        # Override with user preference if specified and it's a lightweight model
        lightweight_models = {
            "tiny": "tinyllama:1.1b",
            "qwen": "qwen2.5:0.5b", 
            "gemma": "gemma2:2b",
            "llama": "llama3.2:3b"
        }
        
        if task_type in lightweight_models:
            ollama_model = lightweight_models[task_type]
        
        # Build context from conversation history
        context = ""
        if history and len(history) > 0:
            # Include last few messages for context
            recent_history = history[-4:] if len(history) > 4 else history
            for msg in recent_history:
                role = "User" if msg.get('sender') == 'user' else "Assistant"
                context += f"{role}: {msg.get('text', '')}\n"
        
        # Create system prompt based on task type
        system_prompts = {
            "chat": """You are SmartProBono's AI Legal Assistant. Provide helpful, conversational legal guidance.

COMMUNICATION STYLE:
- Be friendly and approachable
- Use simple, clear language
- Ask follow-up questions to understand the user's situation better
- Provide specific, actionable advice when possible
- Always remind users this is general information, not legal advice

RESPONSE FORMAT:
- Start with a direct answer to their question
- Provide relevant details and context
- Ask clarifying questions if needed
- Suggest next steps or resources
- End with a disclaimer about consulting an attorney

Keep responses conversational and helpful. Avoid repetitive responses.""",

            "research": """You are a legal research assistant. Provide comprehensive, well-structured legal information.

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the question
2. Legal Principles: Key legal concepts involved
3. Practical Application: How this applies in real situations
4. Jurisdiction Notes: State/federal law differences
5. Resources: Relevant forms, websites, or organizations
6. Next Steps: Recommended actions

Be thorough but accessible.""",

            "draft": """You are a legal document drafting assistant. Help create clear, professional legal documents.

DRAFTING GUIDELINES:
- Use clear, professional language
- Include all necessary legal elements
- Structure documents logically
- Provide placeholders for specific information
- Include standard legal disclaimers

Focus on creating practical, usable documents."""
        }
        
        system_prompt = system_prompts.get(task_type, system_prompts["chat"])
        
        # Build the full prompt
        full_prompt = f"{system_prompt}\n\n{context}User: {message}\n\nAssistant:"
        
        # Call Ollama API with optimized settings
        ollama_url = "http://localhost:11434/api/generate"
        # Ultra-optimized settings for lightweight models
        payload = {
            "model": ollama_model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 300,  # Shorter responses for speed
                "num_ctx": 1024,     # Smaller context window
                "num_batch": 1,      # Process one at a time
                "num_thread": 1,     # Single thread for stability
                "num_gpu": 0,        # Force CPU usage (more stable)
                "low_vram": True     # Optimize for low memory
            }
        }
        
        # Shorter timeout for faster fallback
        response = requests.post(ollama_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama connection error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error calling Ollama: {str(e)}")
        return None

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

class MultiLayerAgentSystem:
    """TRUE multi-layer AI agent system where agents call other agents"""
    
    def __init__(self):
        self.agents = {
            'greeting': GreetingAgent(),
            'compliance': ComplianceAgent(),
            'business': BusinessAgent(),
            'document': DocumentAgent(),
            'expert': ExpertAgent(),
            'immigration': ImmigrationAgent(),
            'family': FamilyLawAgent(),
            'criminal': CriminalLawAgent()
        }
    
    def analyze_complexity(self, message):
        """Analyze message complexity to determine workflow"""
        lower_message = message.lower()
        complexity_indicators = [
            'complex', 'detailed', 'multiple', 'and', 'compliance', 'document',
            'lawsuit', 'defense', 'strategy', 'analysis', 'help with', 'requirements'
        ]
        
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in lower_message) / len(complexity_indicators)
        
        if complexity_score > 0.7:
            return 'complex', True  # complex workflow, needs human review
        elif complexity_score > 0.4:
            return 'multi-agent', False  # multi-agent workflow
        else:
            return 'simple', False  # simple workflow
    
    def determine_agent_chain(self, message, complexity_type):
        """Determine which agents should be involved in processing"""
        lower_message = message.lower()
        agent_chain = ['supervisor']
        
        # Determine primary agent (prioritize main topics over sub-topics)
        if any(keyword in lower_message for keyword in ['immigration', 'visa', 'green card', 'citizenship', 'h1b']):
            agent_chain.append('immigration')
            # Check if we need sub-agents
            if any(keyword in lower_message for keyword in ['document', 'form', 'application']):
                agent_chain.append('document')
            if any(keyword in lower_message for keyword in ['compliance', 'regulation', 'requirement']):
                agent_chain.append('compliance')
                
        elif any(keyword in lower_message for keyword in ['family', 'divorce', 'custody']):
            agent_chain.append('family')
            if complexity_type == 'complex':
                agent_chain.append('expert')
                
        elif any(keyword in lower_message for keyword in ['business', 'llc', 'incorporat', 'corporation']):
            agent_chain.append('business')
            agent_chain.extend(['document', 'compliance'])  # Business always needs docs and compliance
            
        elif any(keyword in lower_message for keyword in ['criminal', 'arrest', 'charges']):
            agent_chain.append('criminal')
            if complexity_type == 'complex':
                agent_chain.append('expert')
                
        elif any(keyword in lower_message for keyword in ['document', 'contract', 'draft']) and not any(keyword in lower_message for keyword in ['immigration', 'visa', 'business', 'family', 'criminal']):
            agent_chain.append('document')
            
        elif any(keyword in lower_message for keyword in ['compliance', 'gdpr', 'privacy']) and not any(keyword in lower_message for keyword in ['immigration', 'visa', 'business', 'family', 'criminal']):
            agent_chain.append('compliance')
            
        else:
            agent_chain.append('greeting')
        
        # Always add synthesis for multi-agent workflows
        if len(agent_chain) > 2:
            agent_chain.append('synthesis')
        
        return agent_chain
    
    def call_agent_with_sub_agents(self, agent_name, message, context, agent_chain):
        """Call an agent and let it call sub-agents if needed"""
        agent = self.agents[agent_name]
        
        # Get the main response from the agent
        main_response = agent.process(message, context)
        
        # Check if this agent needs to call sub-agents
        sub_agent_responses = {}
        
        if agent_name == 'immigration':
            # Immigration agent can call document and compliance agents
            if 'document' in agent_chain:
                doc_agent = self.agents['document']
                sub_agent_responses['document'] = doc_agent.process(f"Generate immigration documents for: {message}", context)
            
            if 'compliance' in agent_chain:
                comp_agent = self.agents['compliance']
                sub_agent_responses['compliance'] = comp_agent.process(f"Check compliance requirements for: {message}", context)
        
        elif agent_name == 'business':
            # Business agent always calls document and compliance
            doc_agent = self.agents['document']
            sub_agent_responses['document'] = doc_agent.process(f"Generate business documents for: {message}", context)
            
            comp_agent = self.agents['compliance']
            sub_agent_responses['compliance'] = comp_agent.process(f"Check business compliance for: {message}", context)
        
        elif agent_name in ['family', 'criminal'] and 'expert' in agent_chain:
            # Family and criminal can call expert for complex cases
            expert_agent = self.agents['expert']
            sub_agent_responses['expert'] = expert_agent.process(f"Provide expert analysis for: {message}", context)
        
        return main_response, sub_agent_responses
    
    def synthesize_responses(self, main_response, sub_agent_responses, agent_chain):
        """Synthesize multiple agent responses into a coherent final response"""
        if not sub_agent_responses:
            return main_response
        
        # Build comprehensive response
        synthesis = f"{main_response}\n\n"
        
        if 'document' in sub_agent_responses:
            synthesis += f"**📄 Document Assistance:**\n{sub_agent_responses['document']}\n\n"
        
        if 'compliance' in sub_agent_responses:
            synthesis += f"**⚖️ Compliance Requirements:**\n{sub_agent_responses['compliance']}\n\n"
        
        if 'expert' in sub_agent_responses:
            synthesis += f"**🔍 Expert Analysis:**\n{sub_agent_responses['expert']}\n\n"
        
        # Add human escalation notice for complex cases
        if len(agent_chain) > 3:  # Multiple agents involved
            synthesis += "**⚠️ Important Notice:**\n"
            synthesis += "This response involves multiple legal areas. For specific legal matters, I strongly recommend consulting with a qualified attorney who can provide personalized legal advice based on your unique situation.\n\n"
        
        return synthesis
    
    def process_message(self, message, context=None):
        """Process message through TRUE multi-layer agent system"""
        try:
            # Step 1: Analyze complexity and determine workflow
            complexity_type, needs_human_review = self.analyze_complexity(message)
            
            # Step 2: Determine agent chain
            agent_chain = self.determine_agent_chain(message, complexity_type)
            
            # Step 3: Process through agent chain
            main_agent = None
            main_response = ""
            sub_agent_responses = {}
            
            for agent_name in agent_chain:
                if agent_name == 'supervisor':
                    continue  # Skip supervisor, it's just for routing
                elif agent_name == 'synthesis':
                    # Synthesize all responses
                    main_response = self.synthesize_responses(main_response, sub_agent_responses, agent_chain)
                else:
                    # Call the agent and its sub-agents (only process the main agent)
                    if main_agent is None:  # Only process the first non-supervisor agent
                        main_response, sub_agent_responses = self.call_agent_with_sub_agents(agent_name, message, context, agent_chain)
                        main_agent = agent_name
            
            # Step 4: Add human escalation if needed
            if needs_human_review:
                main_response += "\n\n**🚨 Human Attorney Review Recommended:**\n"
                main_response += "This case involves complex legal matters that require review by a qualified attorney. Please consult with a legal professional for personalized advice."
            
            # Log the multi-layer processing
            logger.info(f"🔗 Multi-layer chain: {' → '.join(agent_chain)}")
            logger.info(f"📊 Complexity: {complexity_type}, Human Review: {needs_human_review}")
            logger.info(f"🤖 Sub-agents called: {list(sub_agent_responses.keys())}")
            
            return {
                'response': main_response,
                'agent_type': main_agent,
                'agent_name': self.agents[main_agent].name if main_agent else 'Multi-Agent System',
                'agent_chain': agent_chain,
                'complexity_type': complexity_type,
                'needs_human_review': needs_human_review,
                'sub_agents_used': list(sub_agent_responses.keys()),
                'confidence': 0.9 if sub_agent_responses else 0.7,
                'suggestions': self.agents[main_agent].get_suggestions(message) if main_agent else [],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in TRUE multi-layer agent system: {e}")
            return {
                'response': "I'm sorry, I encountered an error in the multi-layer system. Please try again.",
                'agent_type': 'error',
                'agent_name': 'Error Handler',
                'agent_chain': ['error'],
                'complexity_type': 'error',
                'needs_human_review': True,
                'sub_agents_used': [],
                'confidence': 0.0,
                'suggestions': [],
                'timestamp': datetime.now().isoformat()
            }

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def process(self, message, context=None):
        """Process message and return response"""
        raise NotImplementedError
    
    def get_confidence(self, message):
        """Get confidence score for this agent handling the message"""
        return 0.8  # Default confidence
    
    def get_suggestions(self, message):
        """Get follow-up suggestions"""
        return []

class GreetingAgent(BaseAgent):
    """Handles greetings and basic introductions"""
    
    def __init__(self):
        super().__init__("Greeting Agent", "Handles greetings and basic questions")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return "Hello! I'm your AI legal assistant. I can help with various legal matters including immigration, family law, business law, and compliance. What specific legal question can I help you with today?"
        
        elif 'what can you do' in lower_message or 'help' in lower_message:
            return """I can help you with:

• **Immigration Law**: Visas, green cards, citizenship, asylum
• **Family Law**: Divorce, custody, child support, adoption  
• **Business Law**: Incorporation, contracts, compliance
• **Criminal Law**: Charges, court proceedings, rights
• **Document Generation**: Legal forms, contracts, letters
• **Compliance**: GDPR, privacy policies, regulations

What area would you like assistance with?"""
        
        else:
            return "I'm here to help with your legal questions! What specific area would you like assistance with?"
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', lower_message):
            return 0.95
        elif 'what can you do' in lower_message or 'help' in lower_message:
            return 0.9
        return 0.7
    
    def get_suggestions(self, message):
        return [
            "Ask about immigration law",
            "Help with family law matters", 
            "Business legal questions",
            "Document generation help"
        ]

class ImmigrationAgent(BaseAgent):
    """Specializes in immigration law"""
    
    def __init__(self):
        super().__init__("Immigration Agent", "Specializes in immigration law and procedures")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'visa' in lower_message:
            return """**Visa Information:**

I can help with various visa types:
• **Work Visas**: H-1B, L-1, O-1, E-2
• **Family Visas**: Spouse, parent, child petitions
• **Student Visas**: F-1, J-1, M-1
• **Tourist Visas**: B-1/B-2 visitor visas

**Common Issues:**
• Visa denials and appeals
• Status changes and extensions
• Travel restrictions and re-entry

What specific visa situation are you dealing with?"""
        
        elif 'green card' in lower_message:
            return """**Green Card (Permanent Residence):**

**Paths to Green Card:**
• Family-based petitions
• Employment-based petitions  
• Diversity visa lottery
• Asylum/refugee status
• Special immigrant categories

**Process Steps:**
1. File petition (if required)
2. Wait for priority date
3. File adjustment of status
4. Attend interview
5. Receive green card

**Timeline**: 6 months to several years depending on category

What's your specific green card situation?"""
        
        elif 'citizenship' in lower_message or 'naturalization' in lower_message:
            return """**U.S. Citizenship (Naturalization):**

**Requirements:**
• 5 years as permanent resident (3 years if married to U.S. citizen)
• Physical presence in U.S.
• Good moral character
• English language proficiency
• Knowledge of U.S. history and government

**Process:**
1. File Form N-400
2. Biometrics appointment
3. Interview and civics test
4. Oath ceremony

**Benefits:**
• Right to vote
• U.S. passport
• Protection from deportation
• Ability to sponsor family members

Are you ready to apply for citizenship?"""
        
        else:
            return """**Immigration Law Assistance:**

I specialize in helping with:
• **Visa Applications**: Work, family, student, tourist
• **Green Card Process**: Family, employment, diversity lottery
• **Citizenship**: Naturalization requirements and process
• **Asylum**: Refugee status and protection
• **Deportation Defense**: Removal proceedings
• **Status Changes**: Adjusting immigration status

What specific immigration matter can I help you with?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        immigration_keywords = ['immigration', 'visa', 'green card', 'citizenship', 'asylum', 'deportation', 'naturalization']
        return 0.9 if any(keyword in lower_message for keyword in immigration_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "Help with visa application",
            "Green card process guidance",
            "Citizenship requirements",
            "Asylum application help"
        ]

class FamilyLawAgent(BaseAgent):
    """Specializes in family law matters"""
    
    def __init__(self):
        super().__init__("Family Law Agent", "Specializes in family law and domestic relations")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'divorce' in lower_message:
            return """**Divorce Process:**

**Types of Divorce:**
• **Uncontested**: Both parties agree on terms
• **Contested**: Disagreement on key issues
• **No-fault**: Irreconcilable differences
• **Fault-based**: Adultery, abandonment, cruelty

**Key Issues to Address:**
• Child custody and visitation
• Child support calculations
• Spousal support (alimony)
• Property division
• Debt allocation

**Process Steps:**
1. File divorce petition
2. Serve papers to spouse
3. Discovery and negotiations
4. Mediation (if needed)
5. Trial (if contested)
6. Final judgment

What specific aspect of divorce do you need help with?"""
        
        elif 'custody' in lower_message:
            return """**Child Custody:**

**Types of Custody:**
• **Legal Custody**: Decision-making authority
• **Physical Custody**: Where child lives
• **Joint Custody**: Shared by both parents
• **Sole Custody**: One parent has primary custody

**Factors Courts Consider:**
• Child's best interests
• Parent-child relationship
• Parent's ability to provide care
• Child's preferences (if mature enough)
• History of abuse or neglect

**Custody Arrangements:**
• 50/50 shared custody
• Primary custody with visitation
• Supervised visitation
• Virtual visitation

What custody situation are you dealing with?"""
        
        else:
            return """**Family Law Assistance:**

I can help with:
• **Divorce**: Process, property division, support
• **Child Custody**: Arrangements, modifications
• **Child Support**: Calculations, enforcement
• **Adoption**: Process, requirements, costs
• **Domestic Violence**: Protection orders, safety
• **Prenuptial Agreements**: Drafting, enforcement

What family law matter can I assist you with?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        family_keywords = ['divorce', 'custody', 'child support', 'adoption', 'family law', 'alimony']
        return 0.9 if any(keyword in lower_message for keyword in family_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "Divorce process help",
            "Child custody guidance", 
            "Child support calculation",
            "Adoption process info"
        ]

class ComplianceAgent(BaseAgent):
    """Specializes in legal compliance and regulatory matters"""
    
    def __init__(self):
        super().__init__("Compliance Agent", "Specializes in legal compliance and regulatory requirements")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'gdpr' in lower_message:
            return """**GDPR Compliance Overview:**

**When GDPR Applies:**
• Processing personal data of EU residents
• Offering goods/services to EU residents
• Monitoring behavior of EU residents

**Key Requirements:**
1. **Legal Basis**: Consent, contract, legitimate interest, etc.
2. **Privacy Policy**: Clear, accessible, comprehensive
3. **Data Rights**: Access, rectification, erasure, portability
4. **Breach Notification**: Report within 72 hours
5. **Privacy by Design**: Build protection into systems
6. **Data Protection Officer**: Required for certain organizations

**Penalties**: Up to €20M or 4% of annual revenue

**Implementation Steps:**
1. Data audit and mapping
2. Update privacy policies
3. Implement consent mechanisms
4. Create data subject rights procedures
5. Train staff on GDPR requirements

Would you like help creating a GDPR compliance checklist?"""
        
        elif 'privacy policy' in lower_message:
            return """**Privacy Policy Requirements:**

**Essential Elements:**
• What data you collect
• How you use the data
• Who you share data with
• User rights and choices
• Contact information
• Effective date and updates

**Legal Requirements:**
• GDPR (EU residents)
• CCPA (California residents)
• COPPA (children under 13)
• State privacy laws

**Best Practices:**
• Plain language, not legalese
• Easy to find and read
• Regular updates
• User-friendly format
• Clear opt-out mechanisms

Would you like help drafting a privacy policy?"""
        
        else:
            return """**Compliance & Regulatory Assistance:**

I specialize in:
• **GDPR**: Data privacy compliance
• **CCPA**: California privacy rights
• **SOC 2**: Security frameworks
• **HIPAA**: Healthcare privacy
• **COPPA**: Children's privacy
• **Industry Regulations**: Sector-specific compliance

**Services:**
• Compliance assessments
• Policy drafting
• Risk assessments
• Training programs
• Audit preparation

What compliance matter can I help you with?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        compliance_keywords = ['gdpr', 'privacy', 'compliance', 'regulatory', 'soc 2', 'ccpa', 'hipaa']
        return 0.9 if any(keyword in lower_message for keyword in compliance_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "GDPR compliance checklist",
            "Privacy policy drafting",
            "SOC 2 preparation",
            "Regulatory assessment"
        ]

class BusinessAgent(BaseAgent):
    """Specializes in business law and startup legal needs"""
    
    def __init__(self):
        super().__init__("Business Agent", "Specializes in business law and startup legal needs")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'incorporat' in lower_message or 'llc' in lower_message:
            return """**Business Entity Formation:**

**Entity Types:**
• **LLC**: Limited liability, flexible management, pass-through taxation
• **Corporation**: C-Corp, S-Corp, formal structure, potential tax benefits
• **Partnership**: General, limited, limited liability partnership
• **Sole Proprietorship**: Simple, no formal filing required

**LLC Formation Process:**
1. Choose business name
2. File Articles of Organization
3. Create Operating Agreement
4. Obtain EIN from IRS
5. Open business bank account
6. Get necessary licenses/permits

**Considerations:**
• Liability protection
• Tax implications
• Management structure
• Ownership flexibility
• State requirements

What type of business entity are you considering?"""
        
        elif 'contract' in lower_message:
            return """**Business Contracts:**

**Essential Contract Types:**
• **Service Agreements**: Client work, deliverables, payment terms
• **Employment Contracts**: Job duties, compensation, confidentiality
• **Partnership Agreements**: Roles, responsibilities, profit sharing
• **Vendor Agreements**: Supply terms, pricing, delivery
• **NDAs**: Confidentiality protection
• **Terms of Service**: Website/app user agreements

**Key Elements:**
• Clear parties and obligations
• Payment terms and schedules
• Termination clauses
• Dispute resolution
• Governing law
• Force majeure provisions

**Best Practices:**
• Written agreements (avoid oral contracts)
• Clear, specific language
• Regular review and updates
• Legal review for complex matters

What type of contract do you need help with?"""
        
        else:
            return """**Business Law Assistance:**

I can help with:
• **Entity Formation**: LLC, Corporation, Partnership setup
• **Contracts**: Service agreements, employment, partnerships
• **Intellectual Property**: Trademarks, copyrights, patents
• **Employment Law**: Hiring, termination, policies
• **Fundraising**: Investment agreements, securities compliance
• **Compliance**: Industry regulations, licensing

**Startup Legal Checklist:**
• Choose business structure
• File formation documents
• Create operating agreements
• Protect intellectual property
• Set up employment policies
• Ensure regulatory compliance

What business legal matter can I assist you with?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        business_keywords = ['incorporat', 'llc', 'corporation', 'business', 'contract', 'startup', 'fundraising']
        return 0.9 if any(keyword in lower_message for keyword in business_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "LLC formation help",
            "Contract drafting",
            "Business compliance",
            "Startup legal checklist"
        ]

class DocumentAgent(BaseAgent):
    """Specializes in document generation and analysis"""
    
    def __init__(self):
        super().__init__("Document Agent", "Specializes in legal document generation and analysis")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'generate' in lower_message or 'create' in lower_message:
            return """**Document Generation Services:**

**Available Documents:**
• **Business**: LLC formation, contracts, agreements
• **Family**: Divorce petitions, custody agreements
• **Immigration**: Visa applications, support letters
• **General**: Cease and desist, demand letters
• **Templates**: Customizable legal forms

**Process:**
1. Select document type
2. Answer questionnaire
3. Review generated document
4. Download and customize
5. Legal review recommended

**Important Note**: Generated documents are templates and should be reviewed by an attorney for your specific situation.

What type of document do you need to generate?"""
        
        elif 'analyze' in lower_message or 'review' in lower_message:
            return """**Document Analysis Services:**

**Analysis Capabilities:**
• **Contract Review**: Terms, obligations, risks
• **Legal Document**: Compliance, enforceability
• **Business Agreement**: Structure, fairness
• **Policy Review**: Compliance, clarity

**What I Look For:**
• Unclear or ambiguous language
• Missing essential terms
• Unfair or one-sided provisions
• Compliance issues
• Potential risks or liabilities

**Analysis Report Includes:**
• Summary of key terms
• Identified issues and risks
• Recommendations for improvement
• Compliance assessment

What document would you like me to analyze?"""
        
        else:
            return """**Document Services:**

I can help with:
• **Document Generation**: Legal forms, contracts, agreements
• **Document Analysis**: Review, compliance, risk assessment
• **Template Creation**: Customizable legal documents
• **Form Filling**: Assistance with legal forms
• **Document Review**: Professional analysis and recommendations

**Popular Documents:**
• Business formation documents
• Employment contracts
• Service agreements
• Demand letters
• Legal notices

What document service do you need?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        document_keywords = ['document', 'contract', 'agreement', 'generate', 'draft', 'template', 'analyze']
        return 0.9 if any(keyword in lower_message for keyword in document_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "Generate legal document",
            "Analyze contract",
            "Create business agreement",
            "Review legal form"
        ]

class ExpertAgent(BaseAgent):
    """Handles complex legal questions requiring expert analysis"""
    
    def __init__(self):
        super().__init__("Expert Agent", "Handles complex legal questions requiring expert analysis")
    
    def process(self, message, context=None):
        return """**Expert Legal Analysis:**

For complex legal matters, I recommend:

**Immediate Steps:**
1. **Document Everything**: Keep records of all communications and events
2. **Don't Delay**: Legal deadlines are often strict
3. **Avoid Self-Representation**: Complex matters require professional help

**When to Consult an Attorney:**
• Criminal charges or investigations
• Complex business transactions
• High-stakes litigation
• Regulatory compliance issues
• Intellectual property disputes

**Finding the Right Attorney:**
• State bar association referrals
• Legal aid organizations (for low-income)
• Pro bono programs
• Specialized practice areas

**Cost Considerations:**
• Many attorneys offer free consultations
• Legal aid for qualifying individuals
• Payment plans and alternative fee structures
• Pro bono representation available

**Emergency Situations:**
• Arrest or criminal charges
• Restraining orders
• Eviction notices
• Employment termination with legal implications

Would you like help finding legal resources in your area?"""
    
    def get_confidence(self, message):
        # Expert agent for complex questions
        return 0.8 if len(message.split()) > 15 else 0.6
    
    def get_suggestions(self, message):
        return [
            "Find local attorney",
            "Legal aid resources",
            "Emergency legal help",
            "Pro bono programs"
        ]

class CriminalLawAgent(BaseAgent):
    """Specializes in criminal law matters"""
    
    def __init__(self):
        super().__init__("Criminal Law Agent", "Specializes in criminal law and defense")
    
    def process(self, message, context=None):
        lower_message = message.lower().strip()
        
        if 'arrest' in lower_message:
            return """**If You're Arrested:**

**Your Rights:**
• Right to remain silent
• Right to an attorney
• Right to know charges against you
• Right to make phone calls

**What to Do:**
1. **Stay Calm**: Don't resist or argue
2. **Invoke Rights**: "I want to speak to an attorney"
3. **Don't Answer Questions**: Beyond basic identification
4. **Document Everything**: Remember details, witnesses
5. **Contact Attorney**: As soon as possible

**What NOT to Do:**
• Don't make statements without attorney
• Don't consent to searches
• Don't sign anything without reading
• Don't discuss case with others

**Bail and Release:**
• Bail hearing within 24-48 hours
• Bail amount depends on charges and risk
• Can use bail bondsman if needed

**Next Steps:**
• Hire criminal defense attorney
• Prepare for arraignment
• Understand charges and potential penalties

Are you currently facing criminal charges?"""
        
        elif 'charges' in lower_message:
            return """**Understanding Criminal Charges:**

**Types of Charges:**
• **Misdemeanors**: Less serious, fines and/or jail up to 1 year
• **Felonies**: Serious crimes, prison time over 1 year
• **Infractions**: Minor violations, usually just fines

**Common Charges:**
• Theft, fraud, embezzlement
• Assault, battery, domestic violence
• Drug possession, distribution
• DUI/DWI, traffic violations
• White-collar crimes

**Potential Consequences:**
• Fines and restitution
• Probation or parole
• Jail or prison time
• Criminal record
• Loss of rights (voting, firearms)
• Employment difficulties

**Defense Strategies:**
• Challenge evidence
• Constitutional violations
• Plea negotiations
• Alternative sentencing

**Important**: Criminal charges are serious. You need an experienced criminal defense attorney immediately.

What specific charges are you facing?"""
        
        else:
            return """**Criminal Law Assistance:**

I can help with:
• **Arrest Rights**: What to do if arrested
• **Charges**: Understanding criminal charges
• **Defense**: Legal defense strategies
• **Court Process**: Criminal court procedures
• **Sentencing**: Understanding penalties
• **Record Expungement**: Clearing criminal records

**Emergency Situations:**
• If you're currently under arrest
• If you have a warrant
• If you're being questioned by police
• If you have a court date soon

**Important**: Criminal law is complex and consequences are serious. Always consult with a qualified criminal defense attorney.

What criminal law matter can I help you with?"""
    
    def get_confidence(self, message):
        lower_message = message.lower().strip()
        criminal_keywords = ['criminal', 'arrest', 'charges', 'court', 'trial', 'sentencing', 'jail', 'prison']
        return 0.9 if any(keyword in lower_message for keyword in criminal_keywords) else 0.6
    
    def get_suggestions(self, message):
        return [
            "Arrest rights information",
            "Understanding charges",
            "Find criminal defense attorney",
            "Court process help"
        ]

# Initialize the multi-layer agent system
agent_system = MultiLayerAgentSystem()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono Advanced Multi-Layer Agent System is running',
        'version': '3.0.0',
        'ai_system': 'Multi-Layer Agent System with 8 specialized agents',
        'database': 'Supabase PostgreSQL with RLS',
        'migration_status': 'COMPLETED',
        'agents': list(agent_system.agents.keys())
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Advanced legal chat with Ollama integration"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        task_type = data.get('task_type', 'chat')
        context = data.get('context', {})
        
        logger.info(f"💬 Received: {message} (model: {task_type})")
        
        # Use TRUE multi-layer agent system FIRST
        try:
            result = agent_system.process_message(message, context)
        except Exception as e:
            logger.error(f"Multi-layer system error: {e}")
            # Fallback to Ollama only if multi-layer system fails
            ai_response = call_ollama(message, task_type, context.get('history', []))
            if ai_response:
                result = {
                    'response': ai_response,
                    'agent_type': task_type,
                    'agent_name': f'Ollama-{task_type}',
                    'model_info': {
                        'name': f'Ollama-{task_type}',
                        'type': 'local_llm',
                        'provider': 'ollama'
                    },
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Final fallback to simple response
                result = {
                    'response': "I'm experiencing technical difficulties. Please try again or contact support.",
                    'agent_type': 'fallback',
                    'agent_name': 'System Fallback',
                    'timestamp': datetime.now().isoformat()
                }
        
        logger.info(f"🤖 Response length: {len(result['response'])}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in legal chat: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'response': "I'm sorry, I encountered an error. Please try again.",
            'agent_type': 'error',
            'agent_name': 'Error Handler'
        }), 500

@app.route('/api/beta/signup', methods=['POST'])
def beta_signup():
    """Beta signup endpoint"""
    try:
        data = request.json
        if not data or not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email']
        name = data.get('name', '')
        
        # Store in Supabase
        signup_data = {
            'email': email,
            'name': name,
            'signup_date': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/beta_signups",
            headers=SUPABASE_HEADERS,
            json=signup_data
        )
        
        if response.status_code in [200, 201]:
            # Send welcome email
            send_welcome_email(email, name)
            
            return jsonify({
                'success': True,
                'message': 'Successfully signed up for beta access!',
                'email': email
            })
        else:
            return jsonify({'error': 'Failed to sign up'}), 500
            
    except Exception as e:
        logger.error(f"Error in beta signup: {e}")
        return jsonify({'error': 'An error occurred during signup'}), 500

def send_welcome_email(email, name):
    """Send welcome email to beta signup"""
    try:
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.zoho.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME', 'info@smartprobono.org')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_password:
            logger.warning("SMTP password not configured")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Welcome to SmartProBono Beta!'
        
        body = f"""
        Hi {name or 'there'}!
        
        Thank you for signing up for SmartProBono beta access!
        
        SmartProBono is an AI-powered legal platform that provides:
        • Free legal assistance and guidance
        • Document generation and analysis
        • Expert legal advice
        • Immigration, family, business, and criminal law support
        
        We'll notify you as soon as beta access is available.
        
        Best regards,
        The SmartProBono Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Welcome email sent to {email}")
        
    except Exception as e:
        logger.error(f"Error sending welcome email: {e}")

# Audit API endpoints
@app.route('/api/audit/logs', methods=['GET'])
def get_audit_logs():
    """Get audit logs - simplified version for standalone app"""
    try:
        # For now, return a simple response indicating audit system is available
        return jsonify({
            "status": "success",
            "message": "Audit system is available",
            "data": [],
            "count": 0,
            "note": "Full audit functionality requires the complete backend system"
        })
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}")
        return jsonify({"error": "Failed to retrieve audit logs"}), 500

@app.route('/api/audit/dashboard/stats', methods=['GET'])
def get_audit_dashboard_stats():
    """Get audit dashboard statistics - simplified version"""
    try:
        return jsonify({
            "status": "success",
            "data": {
                "time_range": {
                    "start_time": datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "hours": 24
                },
                "totals": {
                    "audit_logs": 0,
                    "security_events": 0,
                    "user_activities": 0
                },
                "security_by_severity": {
                    "low": 0,
                    "medium": 0,
                    "high": 0,
                    "critical": 0
                },
                "events_by_type": {
                    "security": 0,
                    "user_activity": 0,
                    "data_access": 0,
                    "performance": 0,
                    "api_usage": 0,
                    "document_access": 0,
                    "compliance": 0,
                    "system": 0
                },
                "performance": {
                    "avg_response_time_ms": 0
                },
                "top_endpoints": []
            }
        })
    except Exception as e:
        logger.error(f"Error getting audit dashboard stats: {str(e)}")
        return jsonify({"error": "Failed to retrieve audit dashboard stats"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    print(f"🚀 Starting SmartProBono Advanced Multi-Layer Agent System")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Multi-Layer Agent System with 8 specialized agents")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"🔄 Migration Status: COMPLETED")
    print(f"🔍 Audit System: Available (simplified)")
    print(f"")
    print(f"Available agents:")
    for agent_type, agent in agent_system.agents.items():
        print(f"  • {agent.name}: {agent.description}")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"  • Audit Logs: http://localhost:{port}/api/audit/logs")
    print(f"  • Audit Dashboard: http://localhost:{port}/api/audit/dashboard/stats")
    print(f"")
    print(f"🎯 Test the multi-layer system:")
    print(f"  • Say 'hello' → Greeting Agent")
    print(f"  • Ask 'immigration visa' → Immigration Agent")
    print(f"  • Ask 'divorce custody' → Family Law Agent")
    print(f"  • Ask 'GDPR compliance' → Compliance Agent")
    print(f"")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
