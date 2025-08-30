"""AI service for legal analysis and document processing"""
import logging
import random
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-based legal assistance and document analysis"""
    
    @staticmethod
    def generate_legal_response(message, task_type="chat", conversation_id=None, history=None, model="default", user_id=None):
        """
        Generate a response to a legal question using Ollama
        
        Args:
            message (str): The user message
            task_type (str): The type of task (chat, research, draft)
            conversation_id (str, optional): The conversation ID
            history (list, optional): Previous conversation history
            model (str, optional): The AI model to use
            user_id (str, optional): The user ID
            
        Returns:
            dict: The generated response
        """
        try:
            # Generate a response ID
            response_id = f"resp_{random.randint(1000, 9999)}_{int(datetime.now().timestamp())}"
            
            # Prepare the response container
            response = {
                "id": response_id,
                "created_at": datetime.now().isoformat(),
                "model": model,
                "task_type": task_type
            }
            
            # Map model names to Ollama models
            ollama_model_map = {
                "default": "llama3.2:3b",
                "chat": "llama3.2:3b", 
                "mistral": "mistral:7b",
                "llama": "llama3.2:3b",
                "qwen": "qwen2.5:0.5b",
                "gemma": "gemma2:2b",
                "phi": "phi3:mini"
            }
            
            ollama_model = ollama_model_map.get(model, "llama3.2:3b")
            
            # Use Ollama for AI responses
            ai_response = AIService._call_ollama(message, task_type, ollama_model, history)
            
            if ai_response:
                response["response"] = ai_response
                response["model_info"] = {
                    "name": f"Ollama-{model}",
                    "type": "local_llm",
                    "provider": "ollama"
                }
            else:
                # Fallback to simple responses if Ollama fails
                response["response"] = AIService._get_fallback_response(message, task_type)
                response["model_info"] = {
                    "name": "fallback",
                    "type": "static",
                    "provider": "fallback"
                }
            
            # Add conversation tracking if provided
            if conversation_id:
                response["conversation_id"] = conversation_id
                
            return response
            
        except Exception as e:
            logger.error(f"Error generating legal response: {str(e)}")
            return {
                "error": "An error occurred while generating a response",
                "created_at": datetime.now().isoformat()
            }
    
    @staticmethod
    def _call_ollama(message, task_type="chat", model="llama3.2:3b", history=None):
        """Call Ollama API to generate response"""
        try:
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
            
            # Call Ollama API
            ollama_url = "http://localhost:11434/api/generate"
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            response = requests.post(ollama_url, json=payload, timeout=30)
            
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
    
    @staticmethod
    def _get_fallback_response(message, task_type):
        """Fallback responses when Ollama is unavailable"""
        fallback_responses = {
            "chat": f"I understand you're asking about '{message}'. While I'd normally provide detailed guidance using our AI system, I'm currently experiencing technical difficulties. For immediate help, I recommend:\n\n1. Contacting your local legal aid organization\n2. Checking your state's legal resources website\n3. Consulting with a qualified attorney\n\nI apologize for the inconvenience and encourage you to try again in a few moments.",
            
            "research": f"For research on '{message}', I'd typically provide comprehensive legal analysis. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered research assistance.",
            
            "draft": f"I'd normally help draft documents related to '{message}', but our system is temporarily offline. For immediate document needs:\n\n1. Use standard legal templates from your state's court website\n2. Consult with a legal professional for complex documents\n3. Check legal aid organizations for free document assistance\n\nOur AI drafting service should be available again soon."
        }
        
        return fallback_responses.get(task_type, fallback_responses["chat"])

    @staticmethod
    def analyze_document(document, document_type="generic", questions=None):
        """
        Analyze a legal document
        
        Args:
            document: The document to analyze (file or text)
            document_type (str): The type of document
            questions (list, optional): Specific questions to answer about the document
            
        Returns:
            dict: The analysis results
        """
        try:
            # In a real app, this would use OCR/NLP to analyze the document
            # For demo purposes, we'll return mock analyses
            
            # Mock analyses based on document type
            analyses = {
                "eviction_notice": {
                    "document_type": "eviction_notice",
                    "confidence": 0.92,
                    "key_details": {
                        "landlord": "ABC Properties LLC",
                        "tenant": "Jane Doe",
                        "property_address": "123 Main St, Apt 4B",
                        "eviction_grounds": "Non-payment of rent",
                        "notice_period": "30 days",
                        "amount_due": "$1,200.00",
                        "notice_date": "2023-11-01"
                    },
                    "warnings": [
                        "This notice may not provide the legally required time period for your jurisdiction",
                        "The stated grounds for eviction may be contestable"
                    ],
                    "next_steps": [
                        "Verify the notice period complies with local law",
                        "Request an itemized statement of amounts due",
                        "Consider filing a response if you plan to contest"
                    ]
                },
                "lease_agreement": {
                    "document_type": "lease_agreement",
                    "confidence": 0.89,
                    "key_details": {
                        "landlord": "XYZ Real Estate",
                        "tenant": "John Smith",
                        "property_address": "456 Oak Ave",
                        "lease_term": "12 months",
                        "start_date": "2023-01-01",
                        "end_date": "2023-12-31",
                        "monthly_rent": "$1,500.00",
                        "security_deposit": "$1,500.00"
                    },
                    "concerning_clauses": [
                        {
                            "clause": "Tenant waives all rights to jury trial in any dispute",
                            "issue": "May be unenforceable in some jurisdictions",
                            "page": 4
                        },
                        {
                            "clause": "Landlord may enter without notice",
                            "issue": "Likely violates tenant right to privacy/notice requirements",
                            "page": 7
                        }
                    ],
                    "recommendations": [
                        "Negotiate removal of concerning clauses",
                        "Request clarification on maintenance responsibilities",
                        "Ensure security deposit terms comply with local laws"
                    ]
                },
                "generic": {
                    "document_type": "unknown_legal_document",
                    "confidence": 0.75,
                    "summary": "This appears to be a legal document related to property or contractual matters. It contains formal language typical of legal agreements.",
                    "parties_mentioned": ["Party A", "Party B"],
                    "key_dates": ["2023-10-15", "2024-10-15"],
                    "possible_document_types": ["contract", "agreement", "legal notice"],
                    "recommendations": [
                        "Have this document reviewed by an attorney",
                        "Request clarification on any terms you don't understand"
                    ]
                }
            }
            
            # Return the appropriate analysis or generic if type not found
            analysis = analyses.get(document_type, analyses["generic"])
            
            # If questions were provided, add answers
            if questions:
                mock_answers = [
                    "Based on this document, the deadline appears to be October 15, 2023.",
                    "Yes, this document does require notarization according to section 12.",
                    "The penalties for late payment are 5% of the outstanding amount per month.",
                    "You would need to provide 30 days written notice according to this agreement."
                ]
                
                analysis["answers"] = {}
                for i, question in enumerate(questions):
                    if i < len(mock_answers):
                        analysis["answers"][question] = mock_answers[i]
                    else:
                        analysis["answers"][question] = "The document doesn't clearly address this question."
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                "error": "An error occurred while analyzing the document",
                "created_at": datetime.now().isoformat()
            }

    @staticmethod
    def extract_text_from_document(document_path):
        """
        Extract text from a document
        
        Args:
            document_path (str): Path to the document
            
        Returns:
            str: The extracted text
        """
        try:
            # In a real app, this would use OCR to extract text
            # For demo purposes, we'll return mock text
            return """AGREEMENT BETWEEN PARTIES
            
THIS AGREEMENT made this 15th day of October, 2023
            
BETWEEN:
Party A
AND
Party B
            
WHEREAS the parties wish to enter into an agreement for the purpose of...
            
1. TERM
The term of this agreement shall be for a period of 12 months commencing on...
            
2. PAYMENT
The payment schedule shall be as follows...
            
[Document continues with standard legal text]
            """
        except Exception as e:
            logger.error(f"Error extracting text from document: {str(e)}")
            return None

    @staticmethod
    def analyze_eligibility(form_id, answers):
        """
        Analyze eligibility for a legal form or program
        
        Args:
            form_id (str): The form or program ID
            answers (dict): The user's answers to eligibility questions
            
        Returns:
            dict: Eligibility analysis
        """
        try:
            # In a real app, this would use rule-based or ML-based eligibility determination
            # For demo purposes, we'll return mock eligibility results
            
            # Random eligibility result for demonstration
            eligible = random.choice([True, False, "maybe"])
            
            if eligible is True:
                result = {
                    "eligible": True,
                    "confidence": random.uniform(0.8, 0.98),
                    "explanation": f"Based on your responses, you appear to be eligible for the {form_id} program/form.",
                    "next_steps": [
                        "Complete the full application form",
                        "Gather supporting documentation",
                        "Submit your application by the deadline"
                    ],
                    "required_documents": [
                        "Proof of identity",
                        "Proof of residence",
                        "Income verification"
                    ]
                }
            elif eligible is False:
                result = {
                    "eligible": False,
                    "confidence": random.uniform(0.75, 0.95),
                    "explanation": f"Based on your responses, you do not appear to be eligible for the {form_id} program/form.",
                    "disqualifying_factors": [
                        "Income exceeds program limits",
                        "Residency requirements not met"
                    ],
                    "alternatives": [
                        "You may qualify for the alternative program instead",
                        "Consider applying after your circumstances change"
                    ]
                }
            else:  # maybe
                result = {
                    "eligible": "maybe",
                    "confidence": random.uniform(0.6, 0.8),
                    "explanation": f"Your eligibility for the {form_id} program/form is unclear based on the information provided.",
                    "additional_information_needed": [
                        "Clarification on your employment status",
                        "More details about your household composition"
                    ],
                    "next_steps": [
                        "Consult with a legal aid representative",
                        "Provide additional documentation to determine eligibility"
                    ]
                }
                
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing eligibility: {str(e)}")
            return {
                "error": "An error occurred while analyzing eligibility",
                "created_at": datetime.now().isoformat()
            }

    @staticmethod
    def analyze_case(case_data):
        """
        Analyze a legal case for initial assessment
        
        Args:
            case_data (dict): The case data
            
        Returns:
            dict: Case analysis results
        """
        try:
            # In a real app, this would use legal knowledge and ML to analyze the case
            # For demo purposes, we'll return mock analysis
            
            issue_type = case_data.get('legal_issue_type', 'unknown')
            description = case_data.get('description', '')
            
            # Determine mock priority based on keywords
            priority = "medium"  # default
            urgent_keywords = ["eviction", "immediate", "emergency", "urgent", "safety", "violence", "danger"]
            for keyword in urgent_keywords:
                if keyword in description.lower():
                    priority = "high"
                    break
            
            # Generate mock analysis based on issue type
            analyses = {
                "housing": {
                    "issue_type": "housing",
                    "priority": priority,
                    "complexity": random.choice(["low", "medium", "high"]),
                    "estimated_time": random.choice(["1-2 weeks", "2-4 weeks", "1-2 months"]),
                    "recommended_resources": [
                        "Housing Rights Guide",
                        "Tenant Defense Toolkit",
                        "Eviction Prevention Resources"
                    ],
                    "suggested_attorney_expertise": "Landlord-Tenant Law"
                },
                "family": {
                    "issue_type": "family",
                    "priority": priority,
                    "complexity": random.choice(["medium", "high"]),
                    "estimated_time": random.choice(["2-4 weeks", "1-3 months", "3-6 months"]),
                    "recommended_resources": [
                        "Family Law Self-Help Guide",
                        "Child Custody Rights Information",
                        "Domestic Violence Resources"
                    ],
                    "suggested_attorney_expertise": "Family Law"
                },
                "immigration": {
                    "issue_type": "immigration",
                    "priority": priority,
                    "complexity": random.choice(["medium", "high", "very high"]),
                    "estimated_time": random.choice(["1-3 months", "3-6 months", "6-12 months"]),
                    "recommended_resources": [
                        "Immigration Rights Guide",
                        "USCIS Forms Database",
                        "Asylum Seeker Information"
                    ],
                    "suggested_attorney_expertise": "Immigration Law"
                },
                "criminal": {
                    "issue_type": "criminal",
                    "priority": priority,
                    "complexity": random.choice(["medium", "high"]),
                    "estimated_time": random.choice(["2-4 weeks", "1-3 months", "3-6 months"]),
                    "recommended_resources": [
                        "Criminal Record Expungement Guide",
                        "Know Your Rights During Arrest",
                        "Self-Representation in Court Information"
                    ],
                    "suggested_attorney_expertise": "Criminal Defense"
                }
            }
            
            # Return analysis for the issue type or generic if not found
            if issue_type in analyses:
                return analyses[issue_type]
            else:
                return {
                    "issue_type": issue_type,
                    "priority": priority,
                    "complexity": "unknown",
                    "next_steps": [
                        "Additional case assessment needed",
                        "Consultation with legal specialist recommended"
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error analyzing case: {str(e)}")
            return {
                "error": "An error occurred while analyzing the case",
                "priority": "medium"  # default priority as fallback
            }

# Create a singleton instance
ai_service = AIService()

# Convenience functions that delegate to the service instance
def generate_legal_response(message, task_type="chat", conversation_id=None, history=None, model="default", user_id=None):
    return AIService.generate_legal_response(message, task_type, conversation_id, history, model, user_id)

def analyze_document(document, document_type="generic", questions=None):
    return AIService.analyze_document(document, document_type, questions)

def extract_text_from_document(document_path):
    return AIService.extract_text_from_document(document_path)

def analyze_eligibility(form_id, answers):
    return AIService.analyze_eligibility(form_id, answers)

def analyze_case(case_data):
    return AIService.analyze_case(case_data)

def generate_case_summary(case_id):
    """Generate a summary for a case (placeholder function)"""
    return {
        "id": case_id,
        "summary": "This case involves a housing dispute between tenant and landlord.",
        "generated_at": datetime.now().isoformat()
    } 