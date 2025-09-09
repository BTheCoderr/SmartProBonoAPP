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
