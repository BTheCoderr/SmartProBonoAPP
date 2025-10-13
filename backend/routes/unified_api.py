"""
UNIFIED API ROUTES - Single source of truth for all API endpoints
Consolidates all document, AI, and legal analysis functionality
"""

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import logging
import tempfile
import os
from datetime import datetime

from services.unified_document_service import unified_document_service
from services.unified_ai_service import unified_ai_service
from services.auth_service import get_current_user

bp = Blueprint('unified_api', __name__, url_prefix='/api/v1')
logger = logging.getLogger(__name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "document_service": "available",
            "ai_service": "available"
        }
    })

# ============================================================================
# DOCUMENT OPERATIONS
# ============================================================================

@bp.route('/documents/scan', methods=['POST'])
def scan_document():
    """
    Scan and extract text from uploaded documents.
    
    Expected payload:
    - file: The document file to scan
    - document_type: Type of document (optional)
    
    Returns:
    - success: Boolean
    - extracted_text: Extracted text content
    - document_type: Type of document
    - metadata: Additional document information
    """
    try:
        if 'file' not in request.files:
            raise BadRequest("No file provided")
        
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No file selected")
        
        document_type = request.form.get('document_type', 'generic')
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        file.save(temp_file_path)
        
        try:
            # Extract text using unified service
            extracted_text = unified_document_service.extract_text_from_document(temp_file_path)
            
            if not extracted_text:
                return jsonify({
                    "success": False,
                    "error": "Could not extract text from document"
                }), 400
            
            # Get file metadata
            file_size = os.path.getsize(temp_file_path)
            
            return jsonify({
                "success": True,
                "extracted_text": extracted_text,
                "document_type": document_type,
                "metadata": {
                    "filename": file.filename,
                    "file_size": file_size,
                    "extraction_timestamp": datetime.now().isoformat()
                }
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error scanning document: {e}")
        return jsonify({"error": "An error occurred while scanning the document"}), 500

@bp.route('/documents/analyze', methods=['POST'])
def analyze_document():
    """
    Analyze uploaded document for legal information.
    
    Expected payload:
    - file: The document file to analyze
    - document_type: Type of document (optional)
    - questions: List of specific questions (optional)
    
    Returns:
    - success: Boolean
    - analysis: Detailed analysis results
    - document_type: Type of document
    """
    try:
        if 'file' not in request.files:
            raise BadRequest("No file provided")
        
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No file selected")
        
        document_type = request.form.get('document_type', 'generic')
        questions_json = request.form.get('questions', '[]')
        
        try:
            import json
            questions = json.loads(questions_json)
        except:
            questions = []
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"analyze_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        file.save(temp_file_path)
        
        try:
            # Analyze document using unified service
            analysis = unified_document_service.analyze_document(
                temp_file_path, 
                document_type, 
                questions
            )
            
            if not analysis.get('success', False):
                return jsonify({
                    "success": False,
                    "error": analysis.get('error', 'Analysis failed')
                }), 400
            
            return jsonify({
                "success": True,
                "analysis": analysis,
                "document_type": document_type
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        return jsonify({"error": "An error occurred while analyzing the document"}), 500

@bp.route('/documents/generate', methods=['POST'])
def generate_document():
    """
    Generate PDF document from content or template.
    
    Expected payload:
    - content: Content to generate PDF from
    - template_name: Template name (optional)
    - document_type: Type of document (optional)
    
    Returns:
    - success: Boolean
    - pdf_path: Path to generated PDF
    - download_url: URL to download the PDF
    """
    try:
        data = request.json
        if not data:
            raise BadRequest("No data provided")
        
        content = data.get('content')
        template_name = data.get('template_name')
        document_type = data.get('document_type', 'generic')
        
        if not content:
            raise BadRequest("Content is required")
        
        # Generate PDF using unified service
        pdf_path = unified_document_service.generate_pdf(
            content=content,
            template_name=template_name
        )
        
        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({
                "success": False,
                "error": "Failed to generate PDF"
            }), 500
        
        # Create download URL (in production, this would be a proper file serving endpoint)
        download_url = f"/api/v1/documents/download/{os.path.basename(pdf_path)}"
        
        return jsonify({
            "success": True,
            "pdf_path": pdf_path,
            "download_url": download_url,
            "document_type": document_type,
            "generated_at": datetime.now().isoformat()
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return jsonify({"error": "An error occurred while generating the document"}), 500

# ============================================================================
# AI OPERATIONS
# ============================================================================

@bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """
    Chat with AI legal assistant.
    
    Expected payload:
    - message: User message
    - task_type: Type of task (chat, research, draft, analysis)
    - conversation_id: Conversation ID (optional)
    - history: Previous conversation history (optional)
    - model: AI model to use (auto, claude, openai, ollama)
    
    Returns:
    - success: Boolean
    - response: AI response
    - model: Model used
    - conversation_id: Conversation ID
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Message is required")
        
        message = data['message']
        task_type = data.get('task_type', 'chat')
        conversation_id = data.get('conversation_id')
        history = data.get('history', [])
        model = data.get('model', 'auto')
        
        # Get user ID if authenticated
        user_id = None
        try:
            user = get_current_user()
            if user:
                user_id = user.get('id')
        except:
            pass  # User not authenticated
        
        # Use Saul Enhanced AI service for legal operations, with intelligent fallbacks
        try:
            # Import the Saul Enhanced AI service
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from saul_enhanced_ai_service import saul_enhanced_ai
            
            # Generate response using Saul Enhanced AI service
            response = saul_enhanced_ai.generate_legal_response(
                message=message,
                task_type=task_type,
                conversation_id=conversation_id,
                history=history,
                model=model,
                user_id=user_id
            )
        except Exception as e:
            logger.error(f"Saul Enhanced AI service error: {e}")
            # Fallback to simple free AI service
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
                from simple_free_ai import simple_free_ai
                
                response = simple_free_ai.generate_response(
                    message=message,
                    task_type=task_type,
                    conversation_id=conversation_id,
                    user_id=user_id,
                    model=model
                )
            except Exception as fallback_error:
                logger.error(f"Fallback AI service error: {fallback_error}")
                # Final fallback to unified service
                response = unified_ai_service.generate_legal_response(
                    message=message,
                    task_type=task_type,
                    conversation_id=conversation_id,
                    history=history,
                    model=model,
                    user_id=user_id
                )
        
        return jsonify(response)
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@bp.route('/ai/saul/chat', methods=['POST'])
def saul_chat():
    """
    Direct Saul Legal AI chat endpoint.
    
    Expected payload:
    - message: User message
    - task_type: Type of task (chat, research, draft, analysis)
    - conversation_id: Conversation ID (optional)
    - history: Previous conversation history (optional)
    - max_tokens: Maximum tokens to generate (optional, default: 200)
    - temperature: Temperature for generation (optional, default: 0.7)
    
    Returns:
    - success: Boolean
    - response: AI response
    - model: Model used (Saul)
    - conversation_id: Conversation ID
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Message is required")
        
        message = data['message']
        task_type = data.get('task_type', 'chat')
        conversation_id = data.get('conversation_id')
        history = data.get('history', [])
        max_tokens = data.get('max_tokens', 200)
        temperature = data.get('temperature', 0.7)
        
        # Get user ID if authenticated
        user_id = None
        try:
            user = get_current_user()
            if user:
                user_id = user.get('id')
        except:
            pass  # User not authenticated
        
        # Import Saul service
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
        from saul_legal_ai_service import saul_legal_ai
        
        # Generate response using Saul service
        response = saul_legal_ai.generate_response(
            message=message,
            task_type=task_type,
            conversation_id=conversation_id,
            user_id=user_id,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return jsonify(response)
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in Saul chat: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@bp.route('/ai/saul/info', methods=['GET'])
def saul_info():
    """Get information about the Saul Legal AI model"""
    try:
        # Import Saul service
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
        from saul_legal_ai_service import saul_legal_ai
        
        info = saul_legal_ai.get_model_info()
        health = saul_legal_ai.health_check()
        
        return jsonify({
            "model_info": info,
            "health_status": health,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting Saul info: {e}")
        return jsonify({"error": "Failed to get Saul model information"}), 500

@bp.route('/ai/models/available', methods=['GET'])
def available_models():
    """Get information about all available AI models"""
    try:
        # Import Saul Enhanced service
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
        from saul_enhanced_ai_service import saul_enhanced_ai
        
        models = saul_enhanced_ai.get_available_models()
        health = saul_enhanced_ai.health_check()
        
        return jsonify({
            "available_models": models,
            "health_status": health,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return jsonify({"error": "Failed to get model information"}), 500

@bp.route('/ai/analyze-text', methods=['POST'])
def analyze_text():
    """
    Analyze text content for legal information.
    
    Expected payload:
    - text: Text content to analyze
    - document_type: Type of document (optional)
    
    Returns:
    - success: Boolean
    - analysis: Analysis results
    """
    try:
        data = request.json
        if not data or not data.get('text'):
            raise BadRequest("Text content is required")
        
        text = data['text']
        document_type = data.get('document_type', 'generic')
        
        # Analyze text using unified service
        analysis = unified_ai_service.analyze_document_content(text, document_type)
        
        return jsonify(analysis)
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({"error": "An error occurred while analyzing the text"}), 500

# ============================================================================
# LEGAL ANALYSIS (Multi-Agent System)
# ============================================================================

@bp.route('/legal/analyze', methods=['POST'])
def legal_analysis():
    """
    Comprehensive legal analysis using multi-agent system.
    
    Expected payload:
    - query: Legal question or case description
    - jurisdiction: Jurisdiction (ri, ma, fed)
    - case_type: Type of case (optional)
    
    Returns:
    - success: Boolean
    - analysis: Multi-agent analysis results
    - disclaimers: Legal disclaimers
    - warnings: Important warnings
    - recommendations: Practical recommendations
    """
    try:
        data = request.json
        if not data or not data.get('query'):
            raise BadRequest("Query is required")
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'ri')
        case_type = data.get('case_type')
        
        # Import the multi-agent system
        try:
            from legal_ai_backend.langgraph.main_graph import run_pipeline
            
            # Run the multi-agent pipeline
            result = run_pipeline(query)
            
            return jsonify({
                "success": True,
                "analysis": result.get('analysis', {}),
                "disclaimers": result.get('disclaimers', []),
                "warnings": result.get('warnings', []),
                "recommendations": result.get('recommendations', []),
                "jurisdiction": jurisdiction,
                "query": query,
                "timestamp": datetime.now().isoformat()
            })
            
        except ImportError:
            # Fallback to simple AI analysis if multi-agent system not available
            logger.warning("Multi-agent system not available, using fallback")
            
            response = unified_ai_service.generate_legal_response(
                message=query,
                task_type="research",
                model="auto"
            )
            
            return jsonify({
                "success": True,
                "analysis": {
                    "case_summary": [response.get('text', '')],
                    "legal_rules": ["Consult with a qualified attorney for specific legal advice"],
                    "practical_advice": ["This is general information, not legal advice"],
                    "relevance": ["Analysis based on general legal principles"]
                },
                "disclaimers": [
                    "This analysis is for informational purposes only and does not constitute legal advice",
                    "Always consult with a qualified attorney for specific legal advice about your situation"
                ],
                "warnings": [],
                "recommendations": [
                    "Consult with a qualified attorney",
                    "Gather all relevant documents",
                    "Consider your specific circumstances"
                ],
                "jurisdiction": jurisdiction,
                "query": query,
                "timestamp": datetime.now().isoformat()
            })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in legal analysis: {e}")
        return jsonify({"error": "An error occurred while analyzing your legal question"}), 500

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@bp.route('/models', methods=['GET'])
def get_available_models():
    """Get list of available AI models."""
    return jsonify({
        "models": {
            "claude": unified_ai_service.claude_available,
            "openai": unified_ai_service.openai_available,
            "ollama": unified_ai_service.ollama_available
        },
        "default": "auto"
    })

@bp.route('/document-types', methods=['GET'])
def get_document_types():
    """Get list of supported document types."""
    return jsonify({
        "document_types": [
            "contract",
            "lease",
            "agreement",
            "legal_document",
            "court_filing",
            "general"
        ]
    })

@bp.route('/task-types', methods=['GET'])
def get_task_types():
    """Get list of supported task types."""
    return jsonify({
        "task_types": [
            "chat",
            "research", 
            "draft",
            "analysis"
        ]
    })
