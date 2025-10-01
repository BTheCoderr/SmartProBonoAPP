"""
SmartProBono Agent API Routes
Provides endpoints for the AI agent integration with SmartProBono
"""

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import json
import logging
from datetime import datetime

from services.auth_service import require_auth, get_current_user
from services.smartprobono_agent_service import SmartProBonoAgentService
from utils.audit_decorators import audit_log

bp = Blueprint('smartprobono_agent', __name__)
logger = logging.getLogger(__name__)

@bp.route('/agent/chat', methods=['POST'])
@require_auth
@audit_log()
def agent_chat():
    """Enhanced agent chat with SmartProBono-specific capabilities"""
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Missing message")
        
        user_input = data['message']
        conversation_context = data.get('context', {})
        user_role = data.get('user_role', 'client')
        verbose = data.get('verbose', False)
        
        logger.info(f"Received SmartProBono agent chat request: {user_input[:100]}...")
        
        # Get current user context
        try:
            current_user = get_current_user()
            user_id = current_user.get('id') if current_user else None
            user_role = current_user.get('role', user_role) if current_user else user_role
        except:
            user_id = None
        
        # Initialize agent service
        agent_service = SmartProBonoAgentService()
        
        # Process with enhanced capabilities
        response = agent_service.process_request(
            user_input=user_input,
            user_context={
                'user_id': user_id,
                'user_role': user_role,
                'timestamp': datetime.utcnow().isoformat(),
                **conversation_context
            },
            user_role=user_role,
            verbose=verbose
        )
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat(),
            'user_role': user_role,
            'agent_version': '1.0.0'
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in agent chat: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/agent/execute-task', methods=['POST'])
@require_auth
@audit_log()
def execute_agent_task():
    """Execute complex multi-step tasks"""
    try:
        data = request.json
        if not data or not data.get('task'):
            raise BadRequest("Missing task description")
        
        task_description = data['task']
        task_context = data.get('context', {})
        verbose = data.get('verbose', False)
        
        logger.info(f"Received SmartProBono agent task: {task_description[:100]}...")
        
        # Get current user context
        try:
            current_user = get_current_user()
            user_id = current_user.get('id') if current_user else None
            user_role = current_user.get('role', 'client') if current_user else 'client'
        except:
            user_id = None
            user_role = 'client'
        
        # Initialize agent service
        agent_service = SmartProBonoAgentService()
        
        # Execute the task
        result = agent_service.process_request(
            user_input=f"Execute this task: {task_description}",
            user_context={
                'user_id': user_id,
                'user_role': user_role,
                'task_type': 'complex_execution',
                'timestamp': datetime.utcnow().isoformat(),
                **task_context
            },
            user_role=user_role,
            verbose=verbose
        )
        
        return jsonify({
            'task': task_description,
            'result': result,
            'timestamp': datetime.utcnow().isoformat(),
            'user_role': user_role,
            'status': 'completed'
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error executing agent task: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/agent/capabilities', methods=['GET'])
@require_auth
def get_agent_capabilities():
    """Get information about agent capabilities"""
    try:
        capabilities = {
            'case_management': [
                'create_case',
                'update_case_status',
                'search_cases',
                'get_case_details'
            ],
            'client_management': [
                'add_client',
                'update_client',
                'search_clients'
            ],
            'document_processing': [
                'analyze_document',
                'generate_document',
                'update_document_status'
            ],
            'legal_research': [
                'search_case_law',
                'check_compliance'
            ],
            'communication': [
                'send_notification',
                'schedule_meeting'
            ],
            'audit_logging': [
                'log_activity'
            ]
        }
        
        return jsonify({
            'capabilities': capabilities,
            'version': '1.0.0',
            'description': 'SmartProBono AI Agent with comprehensive legal platform integration'
        })
        
    except Exception as e:
        logger.error(f"Error getting agent capabilities: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/agent/status', methods=['GET'])
def get_agent_status():
    """Get agent status and health information"""
    try:
        # Check if agent service can be initialized
        try:
            agent_service = SmartProBonoAgentService()
            agent_healthy = True
            api_available = not agent_service.mock_mode
        except Exception as e:
            agent_healthy = False
            api_available = False
            logger.warning(f"Agent service initialization failed: {str(e)}")
        
        return jsonify({
            'status': 'healthy' if agent_healthy else 'unhealthy',
            'api_available': api_available,
            'mock_mode': not api_available,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/agent/test', methods=['POST'])
@require_auth
def test_agent():
    """Test agent functionality with a simple request"""
    try:
        data = request.json
        test_message = data.get('message', 'Hello, can you help me with my legal case?')
        
        # Get current user context
        try:
            current_user = get_current_user()
            user_role = current_user.get('role', 'client') if current_user else 'client'
        except:
            user_role = 'client'
        
        # Initialize agent service
        agent_service = SmartProBonoAgentService()
        
        # Process test request
        response = agent_service.process_request(
            user_input=test_message,
            user_context={
                'user_role': user_role,
                'test_mode': True,
                'timestamp': datetime.utcnow().isoformat()
            },
            user_role=user_role,
            verbose=True
        )
        
        return jsonify({
            'test_message': test_message,
            'response': response,
            'user_role': user_role,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error testing agent: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'error'
        }), 500

@bp.route('/agent/conversation', methods=['POST'])
@require_auth
@audit_log()
def start_conversation():
    """Start a new conversation session with the agent"""
    try:
        data = request.json
        initial_message = data.get('message', 'Hello, I need help with my legal case.')
        conversation_type = data.get('type', 'general')
        
        # Get current user context
        try:
            current_user = get_current_user()
            user_id = current_user.get('id') if current_user else None
            user_role = current_user.get('role', 'client') if current_user else 'client'
        except:
            user_id = None
            user_role = 'client'
        
        # Initialize agent service
        agent_service = SmartProBonoAgentService()
        
        # Start conversation
        response = agent_service.process_request(
            user_input=initial_message,
            user_context={
                'user_id': user_id,
                'user_role': user_role,
                'conversation_type': conversation_type,
                'session_start': datetime.utcnow().isoformat()
            },
            user_role=user_role
        )
        
        return jsonify({
            'conversation_id': f"conv_{user_id}_{int(datetime.utcnow().timestamp())}",
            'initial_message': initial_message,
            'response': response,
            'user_role': user_role,
            'conversation_type': conversation_type,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'started'
        })
        
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/agent/help', methods=['GET'])
def get_agent_help():
    """Get help information about using the agent"""
    try:
        help_info = {
            'overview': 'SmartProBono AI Agent provides intelligent assistance for legal case management, document analysis, and legal research.',
            'capabilities': [
                'Create and manage legal cases',
                'Analyze legal documents with AI',
                'Search case law and legal precedents',
                'Manage client relationships',
                'Send notifications and schedule meetings',
                'Generate legal documents',
                'Track case progress and compliance'
            ],
            'example_requests': [
                'Create a new immigration case for client John Smith',
                'Search for all open criminal defense cases',
                'Analyze the contract document for compliance issues',
                'Research case law for contract disputes',
                'Send a status update to client 12345',
                'Schedule a meeting with attorney for case review'
            ],
            'usage_tips': [
                'Be specific about case types and client information',
                'Provide context when requesting document analysis',
                'Include relevant details for case law searches',
                'Specify notification preferences for communications'
            ]
        }
        
        return jsonify(help_info)
        
    except Exception as e:
        logger.error(f"Error getting agent help: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
