from flask import Blueprint, request, jsonify, current_app, send_file
import os
import requests
from datetime import datetime
import json
import asyncio
from models.database import db
import random
from services.legal_assistant_service import LegalAssistantService
from ai.document_analyzer import DocumentAnalyzer

legal_ai_bp = Blueprint('legal_ai', __name__, url_prefix='/api/legal')

# Constants
CHAT_HISTORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'chat_history')
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)
os.makedirs(os.path.join(CHAT_HISTORY_DIR, 'files'), exist_ok=True)

# Initialize legal assistant service
legal_assistant = LegalAssistantService()

# Fallback responses for when the LLM service is unavailable
FALLBACK_RESPONSES = [
    "I'm sorry, but I'm having trouble connecting to my knowledge base at the moment. Please try again in a few moments.",
    "It seems that my connection to the legal database is temporarily unavailable. Please try your question again shortly.",
    "I apologize for the inconvenience, but I can't access my full capabilities right now. This is a temporary issue that should resolve shortly.",
    "I'm currently experiencing some technical difficulties. Your question about legal matters is important, and I should be able to help you again soon."
]

def save_message(message):
    """Save a chat message to the history file"""
    try:
        history_file = os.path.join(CHAT_HISTORY_DIR, f"history_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(history_file, 'a') as f:
            json.dump(message, f)
            f.write('\n')
    except Exception as e:
        current_app.logger.error(f"Failed to save message: {str(e)}")

def get_fallback_response():
    """Get a random fallback response"""
    return random.choice(FALLBACK_RESPONSES)

def get_static_tenant_rights_response():
    """Get a static response about tenant rights (for fallback)"""
    return {
        "response": """As a tenant, you generally have the following rights:

1. The right to a habitable living space (working plumbing, heating, electricity, etc.)
2. The right to privacy and protection against unauthorized entry
3. The right to the return of your security deposit with an itemized list of deductions
4. Protection against retaliation for exercising your legal rights
5. The right to sue your landlord for violations

These rights can vary significantly by location, so check your local and state laws for specifics.""",
        "source": "static_response",
        "timestamp": datetime.now().isoformat()
    }

@legal_ai_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history for a user"""
    user_id = request.args.get('user_id', 'anonymous')
    limit = request.args.get('limit', 50, type=int)
    
    try:
        history_file = os.path.join(CHAT_HISTORY_DIR, f"history_{datetime.now().strftime('%Y%m%d')}.jsonl")
        if not os.path.exists(history_file):
            return jsonify({"history": []})
            
        with open(history_file, 'r') as f:
            lines = f.readlines()
            # Filter by user_id and limit results
            history = [json.loads(line) for line in lines if json.loads(line).get('user_id') == user_id][-limit:]
            return jsonify({"history": history})
    except Exception as e:
        current_app.logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({"error": "Failed to retrieve chat history", "history": []}), 500

@legal_ai_bp.route('/chat', methods=['POST'])
async def chat():
    """Enhanced legal chat endpoint with citation support"""
    data = request.get_json()
    message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')
    jurisdiction = data.get('jurisdiction')
    model_id = data.get('model_id')  # Optional model selection
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
        
    current_app.logger.info(f"Legal AI chat request: {message[:100]}...")
    
    try:
        # Save the user message
        save_message({
            "user_id": user_id,
            "sender": "user",
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "jurisdiction": jurisdiction,
            "model_id": model_id
        })
        
        # Use the enhanced legal assistant service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        response = await legal_assistant.get_legal_response_with_citations(
            query=message,
            jurisdiction=jurisdiction,
            model_id=model_id
        )
        
        # Extract response text
        response_text = response.get('text', '')
        
        # Extract citations
        citations = response.get('citations', [])
        
        # Get legal resources based on detected domain
        domain = response.get('domain', 'general')
        resources = legal_assistant.get_legal_resources(domain, jurisdiction)
        
        # Log the response
        await legal_assistant.log_interaction(message, response, user_id)
        
        # Save assistant response
        save_message({
            "user_id": user_id,
            "sender": "assistant",
            "message": response_text,
            "citations": citations,
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "jurisdiction": jurisdiction,
            "model_id": response.get('model_used', model_id)
        })
        
        # Return structured response
        return jsonify({
            "response": response_text,
            "citations": citations,
            "domain": domain,
            "jurisdiction": response.get('jurisdiction'),
            "confidence": response.get('confidence', {}),
            "resources": resources,
            "model_used": response.get('model_used', model_id),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error processing legal AI request: {str(e)}")
        
        # Save error message
        save_message({
            "user_id": user_id,
            "sender": "system",
            "message": f"Error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })
        
        # Return fallback response
        fallback = get_fallback_response()
        return jsonify({
            "response": fallback,
            "error": str(e),
            "fallback": True,
            "timestamp": datetime.now().isoformat()
        }), 500

@legal_ai_bp.route('/chat/files/<filename>', methods=['GET'])
def get_chat_file(filename):
    """Get a file uploaded during chat"""
    try:
        file_path = os.path.join(CHAT_HISTORY_DIR, 'files', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
            
        return send_file(file_path)
    except Exception as e:
        current_app.logger.error(f"Error retrieving chat file: {str(e)}")
        return jsonify({"error": "Failed to retrieve file"}), 500

@legal_ai_bp.route('/rights', methods=['POST'])
async def explain_rights():
    """Explain rights in a specific legal domain and jurisdiction"""
    data = request.get_json()
    domain = data.get('domain', 'general')
    jurisdiction = data.get('jurisdiction')
    specific_topic = data.get('topic', '')
    user_id = data.get('user_id', 'anonymous')
    model_id = data.get('model_id')  # Optional model selection
    
    # Construct a query based on the domain and topic
    query = f"Explain my rights regarding {specific_topic} in {domain}"
    if jurisdiction:
        query += f" in {jurisdiction}"
    
    try:
        # Use the enhanced legal assistant service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        response = await legal_assistant.get_legal_response_with_citations(
            query=query,
            jurisdiction=jurisdiction,
            model_id=model_id
        )
        
        # Extract response text
        response_text = response.get('text', '')
        
        # Extract citations
        citations = response.get('citations', [])
        
        # Get legal resources
        resources = legal_assistant.get_legal_resources(domain, jurisdiction)
        
        # Log the interaction
        await legal_assistant.log_interaction(query, response, user_id)
        
        # Return structured response
        return jsonify({
            "response": response_text,
            "citations": citations,
            "domain": domain,
            "jurisdiction": jurisdiction,
            "resources": resources,
            "model_used": response.get('model_used', model_id),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        current_app.logger.error(f"Error explaining rights: {str(e)}")
        
        # Return fallback response
        fallback = get_static_tenant_rights_response() if domain == 'tenant_rights' else get_fallback_response()
        return jsonify({
            "response": fallback,
            "error": str(e),
            "fallback": True,
            "timestamp": datetime.now().isoformat()
        }), 500

@legal_ai_bp.route('/domains', methods=['GET'])
def get_legal_domains():
    """Get available legal domains and jurisdictions"""
    try:
        # Extract domain info from legal assistant
        domains = []
        for domain_name, domain_info in legal_assistant.legal_domains.items():
            domains.append({
                'id': domain_name,
                'name': domain_name.replace('_', ' ').title(),
                'keywords': domain_info.get('keywords', [])[:5],  # Include just first 5 keywords as examples
                'description': domain_info.get('description', ''),
                'hasSpecializedModel': domain_info.get('has_specialized_model', False)
            })
            
        return jsonify({
            "domains": domains,
            "jurisdictions": legal_assistant.jurisdictions
        })
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving legal domains: {str(e)}")
        return jsonify({"error": "Failed to retrieve legal domains"}), 500

@legal_ai_bp.route('/resources', methods=['GET'])
def get_resources():
    """Get legal resources for a specific domain and jurisdiction"""
    domain = request.args.get('domain', 'general')
    jurisdiction = request.args.get('jurisdiction')
    
    try:
        resources = legal_assistant.get_legal_resources(domain, jurisdiction)
        return jsonify({"resources": resources})
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving legal resources: {str(e)}")
        return jsonify({"error": "Failed to retrieve legal resources", "resources": []}), 500

@legal_ai_bp.route('/analyze', methods=['POST'])
async def analyze_legal_query():
    """
    Analyze a legal query and provide relevant information.
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request'}), 400
            
        query = data['query']
        jurisdiction = data.get('jurisdiction')
        
        # Get legal response with citations
        legal_assistant = LegalAssistantService()
        response = await legal_assistant.get_legal_response_with_citations(query, jurisdiction)
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error analyzing legal query: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing the query'}), 500

@legal_ai_bp.route('/jurisdictions', methods=['GET'])
def get_jurisdictions():
    """Get available jurisdictions for legal questions"""
    try:
        jurisdictions = []
        for jur_id in legal_assistant.jurisdictions:
            jurisdictions.append({
                'id': jur_id,
                'name': jur_id.replace('_', ' ').title(),
                'hasSpecificLaws': jur_id not in ['general', 'international']
            })
        
        return jsonify({
            "jurisdictions": jurisdictions,
            "default": "federal"
        })
    except Exception as e:
        current_app.logger.error(f"Error retrieving jurisdictions: {str(e)}")
        return jsonify({"error": "Failed to retrieve jurisdictions"}), 500

@legal_ai_bp.route('/citations/<citation_id>', methods=['GET'])
def get_citation_details(citation_id):
    """Get detailed information about a specific citation"""
    try:
        # Retrieve citation details from legal assistant
        citation = legal_assistant.get_citation_details(citation_id)
        if not citation:
            return jsonify({"error": "Citation not found"}), 404
            
        return jsonify(citation)
    except Exception as e:
        current_app.logger.error(f"Error retrieving citation details: {str(e)}")
        return jsonify({"error": "Failed to retrieve citation details"}), 500

@legal_ai_bp.route('/models', methods=['GET'])
def get_available_models():
    """Get available AI models for legal assistance"""
    try:
        # Retrieve model information from legal assistant
        models = legal_assistant.get_available_models()
        return jsonify({
            "models": models,
            "default": models[0]['id'] if models else None
        })
    except Exception as e:
        current_app.logger.error(f"Error retrieving available models: {str(e)}")
        return jsonify({"error": "Failed to retrieve available models"}), 500

@legal_ai_bp.route('/chat/specialized', methods=['POST'])
async def chat_specialized():
    """Chat with a specialized legal model for a specific domain"""
    data = request.get_json()
    message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')
        jurisdiction = data.get('jurisdiction')
    domain = data.get('domain', 'general')
    model_id = data.get('model_id')  # Optional model selection
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
        
    current_app.logger.info(f"Specialized legal AI chat request for domain {domain}: {message[:100]}...")
    
    try:
        # Use the specialized legal assistant
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        response = await legal_assistant.get_specialized_legal_response(
            query=message,
            domain=domain,
            jurisdiction=jurisdiction,
            model_id=model_id
        )
        
        # Process and return response
        response_text = response.get('text', '')
        citations = response.get('citations', [])
        resources = legal_assistant.get_legal_resources(domain, jurisdiction)
        
        # Log the interaction
        await legal_assistant.log_interaction(message, response, user_id)
        
        # Save messages
        save_message({
            "user_id": user_id,
            "sender": "user",
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "jurisdiction": jurisdiction,
            "model_id": model_id
        })
        
        save_message({
            "user_id": user_id,
            "sender": "assistant",
            "message": response_text,
            "citations": citations,
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "jurisdiction": jurisdiction,
            "model_id": response.get('model_used', model_id)
        })
        
        # Return structured response
        return jsonify({
            "response": response_text,
            "citations": citations,
            "domain": domain,
            "jurisdiction": jurisdiction,
            "model_used": response.get('model_used', model_id),
            "confidence": response.get('confidence', {}),
            "resources": resources,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error processing specialized legal AI request: {str(e)}")
        
        # Return fallback response
        return jsonify({
            "response": get_fallback_response(),
            "error": str(e),
            "fallback": True,
            "timestamp": datetime.now().isoformat()
        }), 500

@legal_ai_bp.route('/analyze/document', methods=['POST'])
async def analyze_document():
    """
    Analyze a legal document and extract key information.
    
    The request should contain:
    - text: The document text to analyze
    OR
    - file: The document file to analyze (multipart/form-data)
    
    Optional parameters:
    - document_type: Hint for the document type (e.g., 'lease', 'contract', 'legal_brief')
    """
    try:
        # Get document content
        if request.is_json:
            data = request.get_json()
            text = data.get('text')
            doc_type = data.get('document_type')
            
            if not text:
                return jsonify({
                    'error': 'Missing text parameter in JSON'
                }), 400
                
        elif request.content_type and 'multipart/form-data' in request.content_type:
            # Handle file upload
            if 'file' not in request.files:
                return jsonify({
                    'error': 'No file provided'
                }), 400
                
            file = request.files['file']
            if file.filename == '':
                    return jsonify({
                    'error': 'Empty filename'
                }), 400
                
            # Check if file type is supported
            if not allowed_file(file.filename):
                return jsonify({
                    'error': 'Unsupported file type. Supported types: .pdf, .docx, .txt, .rtf'
                }), 400
                
            # Extract text from file
            text = extract_file_content(file)
            if text is None:
                        return jsonify({
                    'error': 'Failed to extract text from file'
                }), 400
                
            doc_type = request.form.get('document_type')
        else:
            return jsonify({
                'error': 'Invalid content type. Use JSON or multipart/form-data'
            }), 400
            
        # Initialize document analyzer
        document_analyzer = DocumentAnalyzer()
        
        # Analyze the document
        analysis_result = document_analyzer.analyze_document(text, doc_type)
        
        # Add disclaimer for AI-generated content
        analysis_result['disclaimer'] = (
            "This document analysis is provided by an AI system and should be considered "
            "for informational purposes only. The accuracy of the analysis may vary, and "
            "it should not be considered legal advice. Please consult with a qualified legal "
            "professional for specific guidance on your legal matters."
        )
        
        # Add timestamp
        analysis_result['timestamp'] = datetime.now().isoformat()
        
        # Return analysis results
        return jsonify(analysis_result)
        
    except Exception as e:
        current_app.logger.error(f"Error analyzing document: {str(e)}")
        return jsonify({
            'error': 'An error occurred while analyzing the document',
            'details': str(e)
        }), 500

def allowed_file(filename: str) -> bool:
    """Check if file type is allowed."""
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'rtf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def extract_file_content(file) -> Optional[str]:
    """Extract text content from uploaded file."""
    try:
        filename = file.filename
        ext = filename.rsplit('.', 1)[1].lower()
        
        if ext == 'pdf':
            # Extract text from PDF
            import pdfplumber
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
            
        elif ext in ['docx', 'doc']:
            # Extract text from Word document
            import docx
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
            
        elif ext in ['txt', 'rtf']:
            # Simple text files
            return file.read().decode('utf-8', errors='replace')
            
        return None
    except Exception as e:
        current_app.logger.error(f"Error extracting file content: {str(e)}")
        return None 