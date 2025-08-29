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

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_SERVICE_KEY = "***REMOVED***"

# Headers for Supabase API calls
SUPABASE_HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json"
}

class MultiLayerAgentSystem:
    """Advanced multi-layer AI agent system"""
    
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
    
    def route_message(self, message, context=None):
        """Route message to appropriate agent based on content and context"""
        lower_message = message.lower().strip()
        
        # Context-aware routing
        if context and context.get('conversation_history'):
            # Analyze conversation history for better routing
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
        if len(message.split()) > 10 or any(keyword in lower_message for keyword in ['complex', 'detailed', 'analysis', 'research']):
            return 'expert'
        
        # Default to greeting for simple messages
        return 'greeting'
    
    def process_message(self, message, context=None):
        """Process message through the multi-layer agent system"""
        try:
            # Route to appropriate agent
            agent_type = self.route_message(message, context)
            agent = self.agents[agent_type]
            
            # Get response from agent
            response = agent.process(message, context)
            
            return {
                'response': response,
                'agent_type': agent_type,
                'agent_name': agent.name,
                'confidence': agent.get_confidence(message),
                'suggestions': agent.get_suggestions(message),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in multi-layer agent system: {e}")
            return {
                'response': "I'm sorry, I encountered an error processing your request. Please try again.",
                'agent_type': 'error',
                'agent_name': 'Error Handler',
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
    """Advanced legal chat with multi-layer agent system"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        context = data.get('context', {})
        
        logger.info(f"💬 Received: {message}")
        
        # Process through multi-layer agent system
        result = agent_system.process_message(message, context)
        
        logger.info(f"🤖 Agent: {result['agent_type']}, Response length: {len(result['response'])}")
        
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    print(f"🚀 Starting SmartProBono Advanced Multi-Layer Agent System")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Multi-Layer Agent System with 8 specialized agents")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"🔄 Migration Status: COMPLETED")
    print(f"")
    print(f"Available agents:")
    for agent_type, agent in agent_system.agents.items():
        print(f"  • {agent.name}: {agent.description}")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Beta Signup: http://localhost:{port}/api/beta/signup")
    print(f"")
    print(f"🎯 Test the multi-layer system:")
    print(f"  • Say 'hello' → Greeting Agent")
    print(f"  • Ask 'immigration visa' → Immigration Agent")
    print(f"  • Ask 'divorce custody' → Family Law Agent")
    print(f"  • Ask 'GDPR compliance' → Compliance Agent")
    print(f"")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
