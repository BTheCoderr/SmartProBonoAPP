"""
API Server for Legal AI Backend.
Provides REST API endpoints for the LangGraph legal AI system.
"""
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from langgraph.main_graph import run_pipeline

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "legal-ai-backend",
        "version": "1.0.0"
    })

@app.route('/api/legal-analysis', methods=['POST'])
def legal_analysis():
    """
    Main endpoint for legal analysis.
    
    Expected JSON payload:
    {
        "query": "I was charged with gun possession, what should I do?",
        "jurisdiction": "ri"  # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing required field: query",
                "success": False
            }), 400
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'ri')
        
        logger.info(f"Processing legal analysis request: {query[:50]}...")
        
        # Run the pipeline
        result = run_pipeline(query)
        
        # Add request metadata
        result['request_metadata'] = {
            'query': query,
            'jurisdiction': jurisdiction,
            'timestamp': result.get('timestamp', ''),
            'pipeline_version': '1.0.0'
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in legal analysis endpoint: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/case-search', methods=['POST'])
def case_search():
    """
    Endpoint for case law search only (without full analysis).
    
    Expected JSON payload:
    {
        "query": "gun possession",
        "jurisdiction": "ri",
        "case_type": "criminal"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing required field: query",
                "success": False
            }), 400
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'ri')
        case_type = data.get('case_type', 'general')
        
        logger.info(f"Processing case search request: {query}")
        
        # Create context for search
        context = {
            "topic": "general",
            "jurisdiction": jurisdiction,
            "case_type": case_type,
            "keywords": query.split(),
            "original_input": query
        }
        
        # Import search functions
        from agents.courtlistener_agent import search_live
        from agents.vector_agent import search_local
        
        # Run searches
        courtlistener_results = search_live(context)
        vector_results = search_local(context)
        
        return jsonify({
            "success": True,
            "courtlistener_results": courtlistener_results,
            "vector_results": vector_results,
            "query": query,
            "jurisdiction": jurisdiction
        })
        
    except Exception as e:
        logger.error(f"Error in case search endpoint: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/vector-stats', methods=['GET'])
def vector_stats():
    """Get statistics about the vector store."""
    try:
        from agents.vector_agent import VectorAgent
        
        agent = VectorAgent()
        stats = agent.get_collection_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"Error getting vector stats: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

# ===== NEW ENHANCED FEATURES =====

@app.route('/api/realtime-updates', methods=['GET'])
def get_realtime_updates():
    """Get real-time case law updates."""
    try:
        from agents.realtime_agent import check_for_updates, get_urgent_updates
        
        # Check for new updates
        updates = check_for_updates()
        urgent_updates = get_urgent_updates()
        
        return jsonify({
            "success": True,
            "updates": [
                {
                    "case_id": update.case_id,
                    "case_name": update.case_name,
                    "court": update.court,
                    "jurisdiction": update.jurisdiction,
                    "update_type": update.update_type,
                    "description": update.description,
                    "timestamp": update.timestamp.isoformat(),
                    "urgency": update.urgency,
                    "action_required": update.action_required
                }
                for update in updates
            ],
            "urgent_updates": [
                {
                    "case_id": update.case_id,
                    "case_name": update.case_name,
                    "urgency": update.urgency,
                    "action_required": update.action_required
                }
                for update in urgent_updates
            ],
            "total_updates": len(updates),
            "urgent_count": len(urgent_updates)
        })
        
    except Exception as e:
        logger.error(f"Error getting real-time updates: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/realtime-subscribe', methods=['POST'])
def subscribe_to_updates():
    """Subscribe to real-time updates for a query."""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing required field: query",
                "success": False
            }), 400
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'ri')
        
        from agents.realtime_agent import subscribe_to_updates
        
        success = subscribe_to_updates(query, jurisdiction)
        
        return jsonify({
            "success": success,
            "message": "Subscribed to updates" if success else "Failed to subscribe",
            "query": query,
            "jurisdiction": jurisdiction
        })
        
    except Exception as e:
        logger.error(f"Error subscribing to updates: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/advanced-reasoning', methods=['POST'])
def advanced_reasoning():
    """Perform advanced legal reasoning analysis."""
    try:
        data = request.get_json()
        
        if not data or 'issue' not in data:
            return jsonify({
                "error": "Missing required field: issue",
                "success": False
            }), 400
        
        issue = data['issue']
        facts = data.get('facts', [])
        jurisdiction = data.get('jurisdiction', 'federal')
        
        from agents.advanced_reasoning_agent import analyze_legal_issue
        
        analysis = analyze_legal_issue(issue, facts, jurisdiction)
        
        return jsonify({
            "success": True,
            "analysis": {
                "issue": analysis.issue,
                "conclusion": analysis.conclusion,
                "confidence": analysis.confidence,
                "reasoning_chain": [
                    {
                        "step_number": step.step_number,
                        "reasoning_type": step.reasoning_type.value,
                        "premise": step.premise,
                        "conclusion": step.conclusion,
                        "confidence": step.confidence
                    }
                    for step in analysis.reasoning_chain
                ],
                "applicable_rules": [
                    {
                        "rule_id": rule.rule_id,
                        "rule_text": rule.rule_text,
                        "jurisdiction": rule.jurisdiction,
                        "authority_level": rule.authority_level,
                        "applicability": rule.applicability
                    }
                    for rule in analysis.applicable_rules
                ],
                "alternative_conclusions": analysis.alternative_conclusions,
                "policy_considerations": analysis.policy_considerations,
                "potential_weaknesses": analysis.potential_weaknesses
            }
        })
        
    except Exception as e:
        logger.error(f"Error in advanced reasoning: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/voice-process', methods=['POST'])
def process_voice():
    """Process voice input and return structured response."""
    try:
        # In a real implementation, this would handle audio data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing required field: text",
                "success": False
            }), 400
        
        text = data['text']
        language = data.get('language', 'en-US')
        
        from agents.voice_agent import voice_agent
        
        # Parse the voice command
        command = voice_agent._parse_voice_command(text)
        
        return jsonify({
            "success": True,
            "command": {
                "command_type": command.command_type,
                "text": command.text,
                "confidence": command.confidence,
                "intent": command.intent,
                "entities": command.entities
            },
            "is_valid": voice_agent.validate_voice_command(command)
        })
        
    except Exception as e:
        logger.error(f"Error processing voice input: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/document-analyze', methods=['POST'])
def analyze_document():
    """Analyze a legal document."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing required field: text",
                "success": False
            }), 400
        
        text = data['text']
        filename = data.get('filename')
        
        from agents.document_analysis_agent import analyze_document
        
        analysis = analyze_document(text, filename)
        
        return jsonify({
            "success": True,
            "analysis": {
                "document_type": analysis.document_type.value,
                "summary": analysis.summary,
                "confidence": analysis.confidence,
                "key_entities": [
                    {
                        "entity_type": entity.entity_type,
                        "text": entity.text,
                        "confidence": entity.confidence,
                        "context": entity.context
                    }
                    for entity in analysis.key_entities
                ],
                "legal_concepts": analysis.legal_concepts,
                "important_dates": analysis.important_dates,
                "parties": analysis.parties,
                "legal_issues": analysis.legal_issues,
                "recommendations": analysis.recommendations,
                "risk_assessment": analysis.risk_assessment
            }
        })
        
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/legal-forms', methods=['GET'])
def get_legal_forms():
    """Get available legal forms for generation."""
    try:
        forms = [
            {
                "id": "contract_template",
                "name": "Basic Contract Template",
                "description": "Standard contract template for various agreements",
                "category": "contracts",
                "fields": ["parties", "terms", "consideration", "duration"]
            },
            {
                "id": "cease_desist",
                "name": "Cease and Desist Letter",
                "description": "Template for cease and desist letters",
                "category": "correspondence",
                "fields": ["recipient", "violation", "demand", "deadline"]
            },
            {
                "id": "power_of_attorney",
                "name": "Power of Attorney",
                "description": "Power of attorney form template",
                "category": "legal_forms",
                "fields": ["principal", "agent", "powers", "duration"]
            },
            {
                "id": "will_template",
                "name": "Basic Will Template",
                "description": "Simple will template",
                "category": "estate_planning",
                "fields": ["testator", "beneficiaries", "executor", "assets"]
            }
        ]
        
        return jsonify({
            "success": True,
            "forms": forms
        })
        
    except Exception as e:
        logger.error(f"Error getting legal forms: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route('/api/generate-form', methods=['POST'])
def generate_legal_form():
    """Generate a legal form based on template and data."""
    try:
        data = request.get_json()
        
        if not data or 'form_id' not in data or 'form_data' not in data:
            return jsonify({
                "error": "Missing required fields: form_id and form_data",
                "success": False
            }), 400
        
        form_id = data['form_id']
        form_data = data['form_data']
        
        # In a real implementation, this would generate actual forms
        # For now, return a template response
        generated_form = {
            "form_id": form_id,
            "generated_at": "2024-01-01T00:00:00Z",
            "status": "generated",
            "download_url": f"/api/forms/{form_id}/download",
            "preview": f"Generated {form_id} form with provided data"
        }
        
        return jsonify({
            "success": True,
            "form": generated_form
        })
        
    except Exception as e:
        logger.error(f"Error generating form: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "success": False
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error",
        "success": False
    }), 500

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Legal AI API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)
