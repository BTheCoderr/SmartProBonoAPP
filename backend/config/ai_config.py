import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
AI_CONFIG = {
    'models': {
        'mistral': {
            'name': 'Mistral-7B-Instruct',
            'specialization': ['chat', 'legal_qa', 'rights_explanation'],
            'huggingface_model': 'mistralai/Mistral-7B-Instruct-v0.1',
            'max_tokens': 1000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'includes_citations': False,
                'bullet_points': True,
                'conversational': True
            },
            'endpoint': 'http://localhost:11434/api/generate',
            'specializations': ['chat', 'legal_qa']
        },
        'llama': {
            'name': 'Llama-2-7b-chat',
            'specialization': ['document_drafting', 'contract_generation'],
            'huggingface_model': 'meta-llama/Llama-2-7b-chat-hf',
            'max_tokens': 2000,
            'temperature': 0.3,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'legal_formatting': True,
                'document_style': True
            },
            'endpoint': 'http://localhost:11434/api/generate',
            'specializations': ['document drafting', 'contracts']
        },
        'deepseek': {
            'name': 'DeepSeek-Coder',
            'specialization': ['legal_research', 'rights_research'],
            'huggingface_model': 'deepseek-ai/deepseek-coder-6.7b-instruct',
            'max_tokens': 2000,
            'temperature': 0.4,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'academic_style': True,
                'research_focused': True
            },
            'endpoint': 'http://localhost:11434/api/generate',
            'specializations': ['legal research', 'rights analysis']
        },
        'falcon': {
            'name': 'Falcon-7B-Instruct',
            'specialization': ['statute_interpretation', 'complex_analysis'],
            'huggingface_model': 'tiiuae/falcon-7b-instruct',
            'max_tokens': 2000,
            'temperature': 0.2,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'detailed_analysis': True,
                'legal_precision': True
            },
            'endpoint': 'http://localhost:11434/api/generate',
            'specializations': ['legal analysis', 'interpretation']
        },
        'openai': {
            'name': 'GPT-3.5-turbo',
            'model': 'gpt-3.5-turbo',
            'max_tokens': 2048,
            'temperature': 0.7,
            'specializations': ['general', 'legal qa', 'chat'],
            'api_key': os.getenv('OPENAI_API_KEY', '')
        }
    },
    'task_routing': {
        # Chat & Basic Q&A - TinyLlama
        'chat': 'mistral',
        'legal_qa': 'mistral',
        'rights_explanation': 'mistral',
        'procedure_guidance': 'mistral',
        
        # Document Generation - GPT2
        'document_drafting': 'llama',
        'contract_generation': 'llama',
        'agreement_review': 'llama',
        'legal_form_filling': 'llama',
        
        # Research & Analysis - BLOOM
        'legal_research': 'deepseek',
        'case_analysis': 'deepseek',
        'rights_research': 'deepseek',
        
        # Complex Interpretation - Falcon
        'statute_interpretation': 'falcon',
        'complex_analysis': 'falcon',
        'precedent_analysis': 'falcon',
        
        # Fallback for all other tasks
        'default': 'openai'
    },
    'api_keys': {
        'openai': os.getenv('OPENAI_API_KEY'),
        'huggingface': os.getenv('HUGGINGFACE_API_KEY')
    },
    'endpoints': {
        'huggingface': 'https://api-inference.huggingface.co/models',
        'ollama': os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434')
    }
}

# Performance Monitoring Configuration
MONITORING_CONFIG = {
    'enabled': True,
    'log_directory': 'logs/performance',
    'metrics': [
        'response_time',
        'token_count',
        'error_rate',
        'success_rate',
        'model_usage',
        'task_distribution',
        'token_efficiency',
        'response_quality',
        'fallback_rate',
        'api_latency',
        'prompt_effectiveness',
        'user_satisfaction'
    ],
    'quality_metrics': {
        'citation_accuracy': True,
        'legal_accuracy': True,
        'response_completeness': True,
        'formatting_accuracy': True
    }
}

# Model-specific prompts
PROMPT_TEMPLATES = {
    'mistral': {
        'chat': """You are SmartProBono's AI Legal Assistant. Your role is to provide clear, accessible legal guidance.

COMMUNICATION GUIDELINES:
1. Use simple, clear language
2. Break down complex legal terms
3. Provide step-by-step instructions
4. Include specific examples
5. Consider local jurisdiction differences

RESPONSE STRUCTURE:
1. Direct Answer: Begin with a clear, concise response
2. Step-by-Step Guide: Break down any processes
3. Important Details: Highlight key requirements, deadlines, or costs
4. Considerations: Note jurisdiction-specific information
5. Next Steps: Provide actionable guidance
6. Resources: Reference relevant forms or websites
7. Professional Help: Indicate when to consult an attorney

Remember: Always include a disclaimer that this is general guidance and not legal advice.

USER QUERY: {prompt}

RESPONSE:""",

        'legal_qa': """You are SmartProBono's Legal Research Assistant. Provide comprehensive answers to legal questions.

RESPONSE FRAMEWORK:
1. Summary: Brief overview of the legal topic
2. Key Points: Main legal principles and concepts
3. Practical Application: How this applies to common situations
4. Requirements: Any specific legal requirements or deadlines
5. Jurisdiction Notes: State or federal law differences
6. Common Issues: Potential challenges or pitfalls
7. Resources: Relevant legal resources or forms

USER QUESTION: {prompt}

DETAILED RESPONSE:"""
    },
    'llama': {
        'document_drafting': """[INST] <<SYS>>
You are the document generator in SmartProBono's contract creation tool.
Follow this document structure:

1. Document Header:
   • Title
   • Date
   • Parties involved
   • Document ID/Reference

2. Definitions:
   • Key terms
   • Important concepts
   • Specific terminology

3. Main Content:
   • Clear sections
   • Numbered paragraphs
   • Standard clauses
   • Custom provisions

4. Special Clauses:
   • Jurisdiction
   • Governing law
   • Dispute resolution
   • Termination terms

5. Signature Block:
   • Party details
   • Date fields
   • Witness sections
   • Notary requirements

Format using:
• Professional legal styling
• Clear paragraph spacing
• Proper numbering
• Section breaks
<</SYS>>
{prompt}
[/INST]""",

        'contract_generation': """[INST] <<SYS>>
You are creating contracts in SmartProBono's document builder.
Include these components:

1. Contract Basics:
   • Title and date
   • Party information
   • Recitals/background
   • Purpose statement

2. Essential Terms:
   • Scope of agreement
   • Payment terms
   • Timeline/deadlines
   • Deliverables

3. Legal Protections:
   • Warranties
   • Indemnification
   • Liability limits
   • Insurance requirements

4. Standard Clauses:
   • Confidentiality
   • Non-compete
   • Force majeure
   • Assignment rights

5. Closing Elements:
   • Notice requirements
   • Amendment process
   • Governing law
   • Signature blocks
<</SYS>>
{prompt}
[/INST]"""
    },
    'deepseek': {
        'legal_research': """System: You are the research assistant in SmartProBono's Rights Explorer.
Provide analysis in this format:

1. Executive Summary:
   • Key findings
   • Main conclusions
   • Critical points

2. Legal Framework:
   • Relevant laws
   • Key regulations
   • Important cases
   • Legal principles

3. Analysis:
   • Detailed examination
   • Multiple perspectives
   • Potential challenges
   • Risk assessment

4. Practical Implications:
   • Real-world impact
   • Common scenarios
   • Best practices
   • Risk mitigation

5. Recommendations:
   • Action items
   • Next steps
   • Professional guidance
   • Resource links

User: {prompt}""",

        'rights_research': """System: You are explaining rights in SmartProBono's Rights Information Center.
Structure your response as:

1. Rights Overview:
   • Basic rights
   • Key protections
   • Legal basis
   • Scope/limitations

2. Specific Rights:
   • Detailed breakdown
   • Conditions/requirements
   • Time limitations
   • Exceptions

3. Exercise of Rights:
   • Step-by-step process
   • Required documents
   • Important deadlines
   • Common obstacles

4. Violations & Remedies:
   • Warning signs
   • Documentation needed
   • Reporting process
   • Legal recourse

5. Support Resources:
   • Legal aid options
   • Advocacy groups
   • Government agencies
   • Additional help

User: {prompt}"""
    },
    'falcon': {
        'statute_interpretation': """System: You are the statute interpreter in SmartProBono's Legal Analysis tool.
Analyze using this framework:

1. Statute Overview:
   • Basic purpose
   • Key provisions
   • Scope/jurisdiction
   • Effective date

2. Key Terms:
   • Definitions
   • Important concepts
   • Legal terminology
   • Critical elements

3. Application:
   • Current interpretation
   • Court decisions
   • Common scenarios
   • Exceptions/limitations

4. Compliance:
   • Requirements
   • Obligations
   • Deadlines
   • Documentation

5. Practical Guidance:
   • Best practices
   • Risk factors
   • Common pitfalls
   • Professional help indicators

User: {prompt}""",

        'complex_analysis': """System: You are handling complex legal analysis in SmartProBono's Advanced Research tool.
Structure analysis as:

1. Issue Identification:
   • Core questions
   • Legal context
   • Key challenges
   • Scope of analysis

2. Legal Framework:
   • Applicable laws
   • Relevant cases
   • Regulations
   • Legal principles

3. Detailed Analysis:
   • Multiple perspectives
   • Competing interests
   • Risk assessment
   • Impact evaluation

4. Practical Implications:
   • Real-world effects
   • Business impact
   • Compliance needs
   • Risk management

5. Strategic Guidance:
   • Recommendations
   • Action items
   • Timeline/deadlines
   • Professional support

User: {prompt}"""
    }
} 