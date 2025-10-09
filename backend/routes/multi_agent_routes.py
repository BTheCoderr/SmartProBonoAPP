"""
Multi-Agent System Routes
FREE models: Ollama + Google Gemini
"""

from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Load environment variables first
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('multi_agent', __name__, url_prefix='/api/multi-agent')

# Import multi-agent service directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from multi_agent_free import multi_agent_free

@bp.route('/agents', methods=['GET'])
def get_agents():
    """Get list of available agents"""
    try:
        agents = multi_agent_free.get_available_agents()
        return jsonify({
            "success": True,
            "agents": agents,
            "message": "Multi-agent system with FREE models (Ollama + Gemini)"
        })
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/process', methods=['POST'])
def process_with_agent():
    """
    Process message with specific agent or auto-route
    
    Body:
    - message: User message (required)
    - agent_id: Specific agent to use (optional)
    - task_type: Type of task for routing (optional)
    - context: Additional context (optional)
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Message is required", "success": False}), 400
        
        message = data['message']
        agent_id = data.get('agent_id')
        task_type = data.get('task_type')
        context = data.get('context', {})
        
        # Process with agent
        response = multi_agent_free.process_with_agent(
            message=message,
            agent_id=agent_id,
            task_type=task_type,
            context=context
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing with agent: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/collaborate', methods=['POST'])
def multi_agent_collaborate():
    """
    Have multiple agents collaborate on a task
    
    Body:
    - message: User message (required)
    - agents: List of agent IDs to consult (required)
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Message is required", "success": False}), 400
        
        if not data.get('agents') or not isinstance(data['agents'], list):
            return jsonify({"error": "Agents list is required", "success": False}), 400
        
        message = data['message']
        agents = data['agents']
        
        # Multi-agent collaboration
        response = multi_agent_free.multi_agent_collaboration(message, agents)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in multi-agent collaboration: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/legal-research', methods=['POST'])
def legal_research():
    """Legal research agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('query'):
            return jsonify({"error": "Query is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=data['query'],
            agent_id='legal_research',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in legal research: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/document-analysis', methods=['POST'])
def document_analysis():
    """Document analysis agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('document'):
            return jsonify({"error": "Document is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=f"Analyze this document: {data['document']}",
            agent_id='document_analysis',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in document analysis: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/case-management', methods=['POST'])
def case_management():
    """Case management agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('task'):
            return jsonify({"error": "Task is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=data['task'],
            agent_id='case_manager',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in case management: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/client-support', methods=['POST'])
def client_support():
    """Client support agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('question'):
            return jsonify({"error": "Question is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=data['question'],
            agent_id='client_support',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in client support: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/court-filing', methods=['POST'])
def court_filing():
    """Court filing agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('filing_task'):
            return jsonify({"error": "Filing task is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=data['filing_task'],
            agent_id='court_filing',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in court filing: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/compliance', methods=['POST'])
def compliance_check():
    """Compliance agent endpoint"""
    try:
        data = request.json
        if not data or not data.get('compliance_question'):
            return jsonify({"error": "Compliance question is required", "success": False}), 400
        
        response = multi_agent_free.process_with_agent(
            message=data['compliance_question'],
            agent_id='compliance',
            context=data.get('context', {})
        )
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in compliance check: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/status', methods=['GET'])
def system_status():
    """Get multi-agent system status"""
    try:
        agents = multi_agent_free.get_available_agents()
        
        return jsonify({
            "success": True,
            "status": "operational",
            "free_models": True,
            "agents": agents,
            "endpoints": {
                "/agents": "List all agents",
                "/process": "Process with specific agent or auto-route",
                "/collaborate": "Multi-agent collaboration",
                "/legal-research": "Legal research agent",
                "/document-analysis": "Document analysis agent",
                "/case-management": "Case management agent",
                "/client-support": "Client support agent",
                "/court-filing": "Court filing agent",
                "/compliance": "Compliance check agent"
            },
            "message": "Multi-agent system running with FREE models (Ollama + Gemini)"
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({"error": str(e), "success": False}), 500
