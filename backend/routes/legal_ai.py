from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import json
import sys
import os
from datetime import datetime
import logging
from backend.services.auth_service import require_auth, get_current_user
from backend.services.ai_service import generate_legal_response, analyze_document

# Add the legal_ai_backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'legal_ai_backend'))

try:
    from langgraph.main_graph import run_pipeline
    LEGAL_AI_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Legal AI backend not available: {e}")
    LEGAL_AI_AVAILABLE = False

bp = Blueprint('legal_ai', __name__)
logger = logging.getLogger(__name__)

@bp.route('/chat', methods=['POST'])
def chat():
    """Endpoint for legal AI chat"""
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Missing message")
            
        message = data['message']
        task_type = data.get('task_type', 'chat')  # Default to chat if no task type is specified
        conversation_id = data.get('conversation_id')
        history = data.get('history', [])
        model = data.get('model', 'default')
        
        logger.info(f"Received legal chat message: {message}, task_type: {task_type}")
        
        # Optional user context
        user_id = None
        try:
            user = get_current_user()
            if user:
                user_id = user.get('id')
        except:
            # User not authenticated - still allow chat as guest
            pass
        
        # Generate response using the appropriate model
        response = generate_legal_response(
            message=message,
            task_type=task_type,
            conversation_id=conversation_id,
            history=history,
            model=model,
            user_id=user_id
        )
        
        return jsonify(response)
    except BadRequest as e:
        logger.error(f"Bad request in legal chat: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in legal chat: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@bp.route('/analyze-document', methods=['POST'])
def analyze_document_route():
    """Endpoint for analyzing legal documents"""
    try:
        if 'file' not in request.files:
            raise BadRequest("No file part")
            
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No selected file")
            
        # Get document type from request
        document_type = request.form.get('document_type', 'generic')
        
        # Get questions to answer about the document (if any)
        questions = request.form.get('questions', '')
        if questions:
            try:
                questions = json.loads(questions)
            except:
                questions = []
        
        # Analyze the document
        analysis = analyze_document(file, document_type, questions)
        
        return jsonify(analysis)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        return jsonify({"error": "An error occurred while analyzing the document"}), 500

@bp.route('/conversations', methods=['GET'])
@require_auth
def get_conversations():
    """Get user's chat conversations"""
    try:
        user = get_current_user()
        
        # In a real app, this would fetch from a database
        # Mocked response for demonstration
        conversations = [
            {
                "id": "conv_001",
                "title": "Tenant Rights Question",
                "last_message": "What are my rights as a tenant?",
                "last_updated": "2023-11-10T14:30:00Z",
                "model": "default"
            },
            {
                "id": "conv_002",
                "title": "Small Claims Court Process",
                "last_message": "How do I file a small claims case?",
                "last_updated": "2023-11-09T10:15:00Z",
                "model": "default"
            }
        ]
        
        return jsonify({"conversations": conversations})
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/conversation/<conversation_id>', methods=['GET'])
@require_auth
def get_conversation(conversation_id):
    """Get a specific conversation history"""
    try:
        user = get_current_user()
        
        # In a real app, this would fetch from a database and validate the user has access
        # Mocked response for demonstration
        messages = [
            {
                "id": "msg_001",
                "conversation_id": conversation_id,
                "role": "user",
                "content": "What are my rights as a tenant if my landlord hasn't fixed a leaking pipe?",
                "timestamp": "2023-11-10T14:30:00Z"
            },
            {
                "id": "msg_002",
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": "As a tenant, you generally have the right to habitable living conditions. If your landlord hasn't fixed a leaking pipe, you may have several options depending on your jurisdiction:\n\n1. Send a written notice to your landlord requesting repairs\n2. In some states, you may be able to withhold rent or \"repair and deduct\"\n3. Contact local housing authorities\n4. Consider legal action if the issue persists\n\nWould you like more specific information about tenant rights in your state?",
                "timestamp": "2023-11-10T14:30:30Z"
            }
        ]
        
        return jsonify({
            "conversation_id": conversation_id,
            "messages": messages
        })
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/models', methods=['GET'])
def get_available_models():
    """Get available AI models for legal assistance"""
    try:
        models = [
            {
                "id": "default",
                "name": "Legal Assistant",
                "description": "General-purpose legal assistant for most questions",
                "capabilities": ["question-answering", "document-explanation"]
            },
            {
                "id": "mistral",
                "name": "Mistral Legal Expert",
                "description": "Specialized legal reasoning model for complex scenarios",
                "capabilities": ["complex-reasoning", "case-analysis"]
            },
            {
                "id": "llama",
                "name": "Llama Document Drafter",
                "description": "Specialized for drafting legal documents and letters",
                "capabilities": ["document-drafting", "template-completion"]
            },
            {
                "id": "deepseek",
                "name": "DeepSeek Research",
                "description": "Research-focused model for legal precedent and case law",
                "capabilities": ["legal-research", "precedent-finding"]
            },
            {
                "id": "falcon",
                "name": "Falcon MultiLingual",
                "description": "Supports multiple languages for global legal questions",
                "capabilities": ["multilingual", "international-law"]
            }
        ]
        
        return jsonify({"models": models})
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/legal-analysis', methods=['POST'])
def legal_analysis():
    """Endpoint for comprehensive legal analysis using LangGraph pipeline"""
    try:
        data = request.json
        if not data or not data.get('query'):
            raise BadRequest("Missing query")
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'ri')  # Default to Rhode Island
        
        logger.info(f"Received legal analysis request: {query[:100]}... in {jurisdiction}")
        
        # Check if legal AI backend is available
        if not LEGAL_AI_AVAILABLE:
            logger.warning("Legal AI backend not available, falling back to basic AI service")
            # Fallback to existing AI service
            response = generate_legal_response(
                message=query,
                task_type="research",
                model="default"
            )
            return jsonify({
                "success": True,
                "analysis": {
                    "case_summary": response.get("response", "Analysis not available"),
                    "key_facts": [],
                    "legal_rules": [],
                    "court_decision": "Analysis not available",
                    "relevance": "Please consult with a qualified attorney",
                    "practical_advice": ["This is general information, not legal advice"],
                    "similar_cases": []
                },
                "disclaimers": [
                    "⚠️ **NOT LEGAL ADVICE**: This analysis is for informational purposes only.",
                    "⚖️ **CONSULT AN ATTORNEY**: Always consult with a qualified, licensed attorney."
                ],
                "warnings": ["Please consult with a qualified attorney for specific advice"],
                "recommendations": ["Contact a qualified attorney in your area"],
                "compliance_level": "medium",
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_ai"
            })
        
        # Use the LangGraph pipeline for comprehensive analysis
        try:
            result = run_pipeline(query)
            
            # Format the response for the frontend
            response = {
                "success": result.get("success", True),
                "analysis": result.get("analysis", {}),
                "disclaimers": result.get("disclaimers", []),
                "warnings": result.get("warnings", []),
                "recommendations": result.get("recommendations", []),
                "compliance_level": result.get("compliance_level", "medium"),
                "timestamp": result.get("timestamp", datetime.now().isoformat()),
                "source": "langgraph_pipeline",
                "metadata": result.get("metadata", {})
            }
            
            logger.info(f"Legal analysis completed successfully for query: {query[:50]}...")
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error in LangGraph pipeline: {str(e)}")
            # Fallback to basic AI service if LangGraph fails
            response = generate_legal_response(
                message=query,
                task_type="research",
                model="default"
            )
            return jsonify({
                "success": False,
                "analysis": {
                    "case_summary": f"Analysis temporarily unavailable: {str(e)}",
                    "key_facts": [],
                    "legal_rules": [],
                    "court_decision": "Analysis not available",
                    "relevance": "Please consult with a qualified attorney",
                    "practical_advice": ["This is general information, not legal advice"],
                    "similar_cases": []
                },
                "disclaimers": [
                    "⚠️ **NOT LEGAL ADVICE**: This analysis is for informational purposes only.",
                    "⚖️ **CONSULT AN ATTORNEY**: Always consult with a qualified, licensed attorney."
                ],
                "warnings": ["Please consult with a qualified attorney for specific advice"],
                "recommendations": ["Contact a qualified attorney in your area"],
                "compliance_level": "high",
                "timestamp": datetime.now().isoformat(),
                "source": "fallback_ai",
                "error": str(e)
            })
            
    except BadRequest as e:
        logger.error(f"Bad request in legal analysis: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in legal analysis: {str(e)}")
        return jsonify({"error": "An error occurred while processing your legal analysis request"}), 500 