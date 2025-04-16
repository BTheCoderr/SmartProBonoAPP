import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
AI_CONFIG = {
    'models': {
        'mistral': {
            'name': 'mistral',
            'specialization': ['chat', 'legal_qa', 'rights_explanation'],
            'huggingface_model': 'mistralai/Mistral-7B-Instruct-v0.3',
            'max_tokens': 1000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'includes_citations': False,
                'bullet_points': True,
                'conversational': True
            },
            'endpoint': 'http://localhost:11434',
            'specializations': ['chat', 'legal_qa']
        },
        'mixtral': {
            'name': 'mixtral',
            'specialization': ['complex_legal_analysis', 'multi_jurisdiction'],
            'huggingface_model': 'mistralai/Mixtral-8x7B-Instruct-v0.1',
            'max_tokens': 2000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'detailed_analysis': True,
                'multi_perspective': True
            },
            'specializations': ['complex analysis', 'multi-jurisdiction']
        },
        'llama': {
            'name': 'llama2',
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
            'endpoint': 'http://localhost:11434',
            'specializations': ['document drafting', 'contracts']
        },
        'llama3': {
            'name': 'llama3',
            'specialization': ['chat', 'multilingual', 'reasoning'],
            'huggingface_model': 'meta-llama/Llama-3-8b-chat',
            'max_tokens': 2000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'multilingual': True,
                'reasoning_focused': True
            },
            'endpoint': 'http://localhost:11434',
            'specializations': ['chat', 'multilingual']
        },
        'legal-bert': {
            'name': 'legal-bert',
            'specialization': ['legal_classification', 'precedent_analysis'],
            'huggingface_model': 'nlpaueb/legal-bert-base-uncased',
            'max_tokens': 512,
            'temperature': 0.2,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'legal_terminology': True,
                'classification_focused': True
            },
            'specializations': ['legal classification', 'precedent matching']
        },
        'legal-roberta': {
            'name': 'legal-roberta',
            'specialization': ['legal_document_analysis', 'contract_review'],
            'huggingface_model': 'lexlms/legal-roberta-large',
            'max_tokens': 512,
            'temperature': 0.3,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'contract_focus': True,
                'term_extraction': True
            },
            'specializations': ['document analysis', 'contract review']
        },
        'deepseek': {
            'name': 'deepseek',
            'specialization': ['legal_research', 'code_generation'],
            'huggingface_model': 'deepseek-ai/deepseek-coder-6.7b-instruct',
            'max_tokens': 2000,
            'temperature': 0.4,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'research_focused': True
            },
            'endpoint': 'http://localhost:11434',
            'specializations': ['legal research', 'code generation']
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
        'phi2': {
            'name': 'Phi-2',
            'specialization': ['quick_legal_qa', 'simple_rights'],
            'huggingface_model': 'microsoft/phi-2',
            'max_tokens': 1000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'simple_language': True,
                'concise': True
            },
            'specializations': ['quick answers', 'simple explanations']
        },
        'openhermes': {
            'name': 'openhermes',
            'specialization': ['chat', 'legal_qa', 'reasoning'],
            'huggingface_model': 'teknium/OpenHermes-2.5-Mistral-7B',
            'max_tokens': 2000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'reasoning_focused': True
            },
            'endpoint': 'http://localhost:11434',
            'specializations': ['chat', 'legal qa']
        },
        'lawgpt': {
            'name': 'lawgpt',
            'specialization': ['legal_analysis', 'case_law'],
            'huggingface_model': 'law-ai/law-gpt',
            'max_tokens': 2000,
            'temperature': 0.3,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'legal_focused': True,
                'case_law': True
            },
            'specializations': ['legal analysis', 'case law']
        },
        'openai': {
            'name': 'GPT-3.5-turbo',
            'model': 'gpt-3.5-turbo',
            'max_tokens': 2048,
            'temperature': 0.7,
            'specializations': ['general', 'legal qa', 'chat'],
            'api_key': os.getenv('OPENAI_API_KEY', '')
        },
        'legal-bertimbau': {
            'name': 'legal-bertimbau',
            'specialization': ['legal_analysis', 'portuguese_law'],
            'huggingface_model': 'rufimelo/Legal-BERTimbau-sts-large-ma-v3',
            'max_tokens': 512,
            'temperature': 0.2,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'legal_terminology': True,
                'multilingual': True
            },
            'specializations': ['legal analysis', 'portuguese law']
        },
        'legalbert-large': {
            'name': 'legalbert-large',
            'specialization': ['legal_classification', 'document_analysis'],
            'huggingface_model': 'pile-of-law/legalbert-large-1.7M-2',
            'max_tokens': 512,
            'temperature': 0.2,
            'response_format': {
                'structured': True,
                'includes_citations': True,
                'legal_terminology': True,
                'classification_focused': True
            },
            'specializations': ['legal classification', 'document analysis']
        },
        'phi-4': {
            'name': 'phi-4',
            'specialization': ['quick_qa', 'code_generation'],
            'huggingface_model': 'microsoft/phi-4',
            'max_tokens': 1000,
            'temperature': 0.7,
            'response_format': {
                'structured': True,
                'simple_language': True,
                'concise': True
            },
            'specializations': ['quick answers', 'code generation']
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
    'task_to_prompt': {
        # Default templates
        'chat': 'chat',
        'document_drafting': 'document_drafting',
        'contract_generation': 'contract_generation',
        'legal_research': 'legal_qa_with_citations',  # Use citation-focused prompt
        'rights_explanation': 'legal_qa_with_citations',  # Use citation-focused prompt
        'rights_research': 'legal_qa_with_citations',  # Use citation-focused prompt
        'statute_interpretation': 'statute_interpretation',
        'complex_analysis': 'complex_analysis',
        'procedure_guidance': 'legal_qa',
        'legal_qa': 'legal_qa',
        'default': 'chat'
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

DETAILED RESPONSE:""",

        'legal_qa_with_citations': """You are SmartProBono's Legal Research Assistant providing well-cited legal information.

RESPONSE GUIDELINES:
1. Structure your response clearly with headers and organized paragraphs
2. Include precise legal citations in your response using these formats:
   - Case law: Smith v. Jones, 123 U.S. 456 (1990)
   - Statutes: 42 U.S.C. § 1983
   - Regulations: 24 C.F.R. § 100.204
   - Constitution: U.S. Const. art. I, § 8
3. Mention relevant jurisdictions (Federal or specific states)
4. Use proper legal terminology
5. Provide a balanced view of the legal question
6. Conclude with practical implications

STRUCTURE YOUR ANSWER WITH:
- Introductory summary
- Applicable law with citations
- Analysis and explanation
- Jurisdiction-specific considerations
- Practical implications
- Conclusion

USER QUESTION: {prompt}

RESPONSE:"""
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