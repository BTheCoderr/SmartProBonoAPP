"""AI service for legal analysis and document processing"""
import logging
import random
import re
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
    def analyze_document(document_path, document_type="generic", questions=None):
        """
        Analyze a legal document using real text extraction
        
        Args:
            document_path (str): Path to the document file
            document_type (str): The type of document
            questions (list, optional): Specific questions to answer about the document
            
        Returns:
            dict: The analysis results
        """
        try:
            # Extract text from the document
            extracted_text = AIService.extract_text_from_document(document_path)
            
            if not extracted_text:
                return {
                    "error": "Could not extract text from document",
                    "document_type": document_type,
                    "confidence": 0.0
                }
            
            # Analyze the extracted text
            analysis = AIService._analyze_extracted_text(extracted_text, document_type)
            
            # Add extracted text to the analysis
            analysis["extracted_text"] = extracted_text
            analysis["text_length"] = len(extracted_text)
            analysis["word_count"] = len(extracted_text.split())
            
            # If questions were provided, add answers based on extracted text
            if questions:
                analysis["answers"] = {}
                for question in questions:
                    analysis["answers"][question] = AIService._answer_question_from_text(extracted_text, question)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                "error": "An error occurred while analyzing the document",
                "created_at": datetime.now().isoformat()
            }
    
    @staticmethod
    def _analyze_extracted_text(text, document_type="generic"):
        """
        Analyze extracted text to identify legal document characteristics
        
        Args:
            text (str): The extracted text from the document
            document_type (str): The type of document
            
        Returns:
            dict: Analysis results
        """
        import re
        from datetime import datetime
        
        # Convert to lowercase for analysis
        text_lower = text.lower()
        
        # Basic document analysis
        analysis = {
            "document_type": document_type,
            "confidence": 0.85,
            "analysis_date": datetime.now().isoformat(),
            "parties": [],
            "key_dates": [],
            "monetary_amounts": [],
            "legal_terms": [],
            "potential_issues": [],
            "recommendations": []
        }
        
        # Extract parties (look for common patterns)
        party_patterns = [
            r'(?:between|party|plaintiff|defendant|tenant|landlord|buyer|seller)\s*:?\s*([A-Z][a-zA-Z\s&,\.]+)',
            r'([A-Z][a-zA-Z\s&,\.]+)\s*(?:vs?\.?|v\.?)\s*([A-Z][a-zA-Z\s&,\.]+)',
            r'(?:plaintiff|defendant|tenant|landlord|buyer|seller)\s*:?\s*([A-Z][a-zA-Z\s&,\.]+)'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    analysis["parties"].extend([m.strip() for m in match if m.strip()])
                else:
                    if match.strip() and len(match.strip()) > 2:
                        analysis["parties"].append(match.strip())
        
        # Remove duplicates and clean up
        analysis["parties"] = list(set([p for p in analysis["parties"] if len(p) > 2 and not p.lower() in ['party', 'plaintiff', 'defendant']]))
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            analysis["key_dates"].extend(matches)
        
        # Extract monetary amounts
        money_patterns = [
            r'\$[\d,]+\.?\d*',
            r'\b\d+\.\d{2}\s*(?:dollars?|USD)\b',
            r'\b(?:amount|total|sum|payment|rent|deposit|fee|cost|price)\s*:?\s*\$?[\d,]+\.?\d*\b'
        ]
        
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            analysis["monetary_amounts"].extend(matches)
        
        # Identify legal terms and concepts
        legal_terms = [
            'agreement', 'contract', 'lease', 'notice', 'complaint', 'petition',
            'warrant', 'injunction', 'damages', 'liability', 'indemnification',
            'breach', 'termination', 'renewal', 'assignment', 'subletting',
            'security deposit', 'rent', 'utilities', 'maintenance', 'repair',
            'eviction', 'possession', 'quiet enjoyment', 'habitability'
        ]
        
        for term in legal_terms:
            if term in text_lower:
                analysis["legal_terms"].append(term)
        
        # Analyze document type based on content
        if 'eviction' in text_lower or 'notice to quit' in text_lower:
            analysis["document_type"] = "eviction_notice"
            analysis["confidence"] = 0.9
        elif 'lease' in text_lower or 'rental agreement' in text_lower:
            analysis["document_type"] = "lease_agreement"
            analysis["confidence"] = 0.9
        elif 'complaint' in text_lower or 'plaintiff' in text_lower:
            analysis["document_type"] = "legal_complaint"
            analysis["confidence"] = 0.9
        elif 'contract' in text_lower or 'agreement' in text_lower:
            analysis["document_type"] = "contract"
            analysis["confidence"] = 0.8
        
        # Generate potential issues and recommendations
        analysis["potential_issues"] = AIService._identify_potential_issues(text, analysis["document_type"])
        analysis["recommendations"] = AIService._generate_recommendations(text, analysis["document_type"])
        
        return analysis
    
    @staticmethod
    def _identify_potential_issues(text, doc_type):
        """Identify potential legal issues in the document"""
        issues = []
        text_lower = text.lower()
        
        # Check for concerning clauses
        concerning_patterns = [
            (r'waive.*right.*jury.*trial', 'Waiver of jury trial rights may be unenforceable'),
            (r'enter.*without.*notice', 'Entry without notice may violate privacy rights'),
            (r'automatic.*renewal', 'Automatic renewal clauses can be problematic'),
            (r'penalty.*late.*payment', 'Late payment penalties should be reasonable'),
            (r'one.sided.*indemnification', 'One-sided indemnification may be unenforceable')
        ]
        
        for pattern, issue in concerning_patterns:
            if re.search(pattern, text_lower):
                issues.append(issue)
        
        return issues
    
    @staticmethod
    def _generate_recommendations(text, doc_type):
        """Generate recommendations based on document analysis"""
        recommendations = []
        
        if doc_type == "eviction_notice":
            recommendations.extend([
                "Verify the notice period complies with local law",
                "Check if the grounds for eviction are valid",
                "Consider consulting with a tenant rights organization"
            ])
        elif doc_type == "lease_agreement":
            recommendations.extend([
                "Review all terms carefully before signing",
                "Ensure security deposit terms comply with local laws",
                "Consider having the document reviewed by an attorney"
            ])
        else:
            recommendations.extend([
                "Have this document reviewed by an attorney",
                "Request clarification on any terms you don't understand",
                "Ensure all parties understand their obligations"
            ])
        
        return recommendations
    
    @staticmethod
    def _answer_question_from_text(text, question):
        """Answer a specific question based on the extracted text"""
        # Simple keyword-based answering
        text_lower = text.lower()
        question_lower = question.lower()
        
        if 'deadline' in question_lower or 'due date' in question_lower:
            # Look for dates in the text
            import re
            dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
            if dates:
                return f"Based on the document, relevant dates found: {', '.join(dates[:3])}"
        
        if 'notarization' in question_lower or 'notary' in question_lower:
            if 'notar' in text_lower:
                return "Yes, this document appears to require notarization."
            else:
                return "The document doesn't clearly mention notarization requirements."
        
        if 'penalty' in question_lower or 'late payment' in question_lower:
            if 'penalty' in text_lower or 'late' in text_lower:
                return "The document contains penalty provisions. Please review the specific terms."
            else:
                return "No specific penalty terms were found in the document."
        
        return "The document doesn't clearly address this question. Please review the full text for relevant information."

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
            import os
            from PyPDF2 import PdfReader
            
            # Check if file exists
            if not os.path.exists(document_path):
                logger.error(f"Document file not found: {document_path}")
                return None
            
            # Get file extension
            file_ext = os.path.splitext(document_path)[1].lower()
            
            if file_ext == '.pdf':
                # Extract text from PDF using PyPDF2
                reader = PdfReader(document_path)
                text = ""
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                        continue
                
                if text.strip():
                    logger.info(f"Successfully extracted {len(text)} characters from PDF")
                    return text.strip()
                else:
                    logger.warning("No text could be extracted from PDF")
                    return None
                    
            else:
                # For other file types, return a placeholder
                logger.warning(f"File type {file_ext} not supported for text extraction")
                return f"Text extraction not supported for {file_ext} files"
                
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