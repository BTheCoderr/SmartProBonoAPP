import openai
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from .ai_service_manager import ai_service_manager, AIProvider

load_dotenv()

# Configure OpenAI and Support Information
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@smartprobono.org')
SUPPORT_HOURS = '9:00 AM - 5:00 PM EST'
SUPPORT_RESPONSE_TIME = '24-48 hours'

if not openai.api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Legal domain categories for context
LEGAL_DOMAINS = {
    'tenant_rights': {
        'context': 'Housing law, tenant-landlord relationships, rental agreements, eviction processes',
        'key_terms': ['lease', 'eviction', 'security deposit', 'repairs', 'rent', 'landlord', 'tenant'],
        'task_type': 'faq'
    },
    'employment': {
        'context': 'Employment law, worker rights, workplace discrimination, compensation, benefits',
        'key_terms': ['workplace', 'salary', 'discrimination', 'benefits', 'termination', 'contract'],
        'task_type': 'legal_research'
    },
    'immigration': {
        'context': 'Immigration law, visa applications, citizenship, residency requirements',
        'key_terms': ['visa', 'citizenship', 'green card', 'immigration', 'passport', 'residency'],
        'task_type': 'case_analysis'
    },
    'contracts': {
        'context': 'Contract law, agreements, terms and conditions, breach of contract',
        'key_terms': ['agreement', 'contract', 'terms', 'breach', 'parties', 'signature'],
        'task_type': 'document_drafting'
    }
}

def get_support_info():
    """
    Get formatted support information
    """
    return f"""

Need additional help?
- Email: {SUPPORT_EMAIL}
- Support Hours: {SUPPORT_HOURS}
- Response Time: {SUPPORT_RESPONSE_TIME}"""

def detect_legal_domain(message):
    """
    Detect the legal domain of the user's query based on key terms.
    """
    message_lower = message.lower()
    domain_scores = {}

    for domain, info in LEGAL_DOMAINS.items():
        score = sum(1 for term in info['key_terms'] if term in message_lower)
        domain_scores[domain] = score

    # Get the domain with the highest score
    max_score_domain = max(domain_scores.items(), key=lambda x: x[1])
    return max_score_domain[0] if max_score_domain[1] > 0 else None

async def get_legal_response(message):
    """
    Get a legal response using the appropriate AI model based on the domain and task type.
    """
    # Detect the legal domain
    domain = detect_legal_domain(message)

    # Determine task type and best provider
    task_type = LEGAL_DOMAINS[domain]['task_type'] if domain else 'chat'
    provider = ai_service_manager.get_best_provider(task_type)

    # Build the system prompt based on the detected domain
    base_prompt = """You are an AI legal assistant providing general legal information and guidance. Your role is to:

1. Provide clear, accurate information about legal concepts, rights, and procedures
2. Use plain language to explain complex legal terms and concepts
3. Reference relevant legal frameworks when applicable
4. Always include appropriate disclaimers about the limitations of AI legal advice
5. Suggest when and how to seek professional legal counsel
6. Focus on educational and informational aspects rather than specific legal advice
7. Provide relevant resources and next steps when appropriate

Guidelines for responses:
- Start with a clear, direct answer to the question
- Break down complex concepts into simple explanations
- Use bullet points or numbered lists for steps or multiple points
- Include relevant examples when helpful
- End with next steps or resources
- Always maintain a professional yet approachable tone
- For complex queries, suggest contacting our support team"""

    # Add domain-specific context if detected
    if domain and domain in LEGAL_DOMAINS:
        domain_context = LEGAL_DOMAINS[domain]['context']
        base_prompt += f"\n\nYou are specifically responding to a question about {domain_context}. Focus on providing accurate information within this legal domain while maintaining general applicability."

    try:
        # Get response from appropriate AI provider
        ai_response = await ai_service_manager.get_response(
            prompt=f"{base_prompt}\n\nUser Question: {message}",
            provider=provider,
            task_type=task_type
        )

        # Add domain-specific disclaimer
        domain_disclaimer = ""
        if domain:
            domain_disclaimer = f"\n\nThis information relates to general {domain.replace('_', ' ')} matters. "

        general_disclaimer = "Please note: This information is for general guidance only and may not apply to your specific situation. For specific legal advice, please consult with a qualified legal professional."

        # Add support information for complex queries or if certain keywords are present
        complex_keywords = ['complex', 'complicated', 'difficult', 'unsure', 'help', 'support']
        if any(keyword in message.lower() for keyword in complex_keywords) or len(message.split()) > 20:
            support_info = get_support_info()
        else:
            support_info = ""

        if "consult" not in ai_response.lower() and "attorney" not in ai_response.lower():
            ai_response += domain_disclaimer + general_disclaimer

        # Add support information if applicable
        ai_response += support_info

        # Log the interaction for quality improvement
        log_interaction(message, ai_response, domain)

        return ai_response

    except Exception as e:
        # Fallback to OpenAI if other providers fail
        print(f"Error with {provider}: {str(e)}")
        return await ai_service_manager.get_response(
            prompt=f"{base_prompt}\n\nUser Question: {message}",
            provider=AIProvider.OPENAI,
            task_type='default'
        )

async def analyze_legal_document(document_text):
    """
    Analyze a legal document using Falcon (good for deep analysis) with OpenAI fallback.
    """
    system_prompt = """You are a legal document analyzer. Your task is to:
1. Break down complex legal language into clear, simple terms
2. Identify key provisions and obligations
3. Highlight important deadlines or dates
4. Flag any potentially concerning clauses
5. Explain the practical implications for all parties involved"""

    try:
        return await ai_service_manager.get_response(
            prompt=f"{system_prompt}\n\nDocument to analyze: {document_text}",
            provider=AIProvider.FALCON,
            task_type='legal_research'
        )
    except Exception as e:
        print(f"Error with Falcon: {str(e)}")
        return await ai_service_manager.get_response(
            prompt=f"{system_prompt}\n\nDocument to analyze: {document_text}",
            provider=AIProvider.OPENAI,
            task_type='default'
        )

async def get_legal_suggestions(context):
    """
    Get context-aware legal suggestions using Mistral (good for FAQs and suggestions) with OpenAI fallback.
    """
    system_prompt = """You are a legal assistant providing actionable next steps and suggestions. Focus on:
1. Practical, step-by-step guidance
2. Required documentation or forms
3. Relevant deadlines or timelines
4. Potential challenges or considerations
5. Resources for additional help"""

    try:
        return await ai_service_manager.get_response(
            prompt=f"{system_prompt}\n\nContext: {context}",
            provider=AIProvider.MISTRAL,
            task_type='faq'
        )
    except Exception as e:
        print(f"Error with Mistral: {str(e)}")
        return await ai_service_manager.get_response(
            prompt=f"{system_prompt}\n\nContext: {context}",
            provider=AIProvider.OPENAI,
            task_type='default'
        )

def log_interaction(user_message, ai_response, domain):
    """
    Log interactions for quality improvement and analysis.
    """
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'user_message': user_message,
            'ai_response': ai_response
        }

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Write to log file
        log_file = f"logs/interactions_{datetime.now().strftime('%Y%m%d')}.json"

        existing_logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                existing_logs = json.load(f)

        existing_logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

    except Exception as e:
        print(f"Error logging interaction: {str(e)}")
        # Don't raise the exception as logging failure shouldn't affect the main functionality 