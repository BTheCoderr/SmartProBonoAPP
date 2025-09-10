"""
AI Virtual Paralegal API Routes
Provides endpoints for the autonomous AI Virtual Paralegal system.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import asyncio
from services.ai_virtual_paralegal_service import ai_virtual_paralegal

logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('ai_virtual_paralegal', __name__, url_prefix='/api/v1/ai-virtual-paralegal')

@bp.route('/status', methods=['GET'])
def get_ai_status():
    """Get AI Virtual Paralegal status."""
    try:
        status = ai_virtual_paralegal.get_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error getting AI status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/start', methods=['POST'])
def start_ai_workflow():
    """Start the AI Virtual Paralegal workflow."""
    try:
        # Run the async workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal.start_ai_workflow())
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error starting AI workflow: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/stop', methods=['POST'])
def stop_ai_workflow():
    """Stop the AI Virtual Paralegal workflow."""
    try:
        ai_virtual_paralegal.is_active = False
        ai_virtual_paralegal.workflow_state = "idle"
        ai_virtual_paralegal._log("info", "AI Virtual Paralegal stopped by user", "Main Controller")
        
        return jsonify({
            'success': True,
            'message': 'AI Virtual Paralegal stopped'
        })
    except Exception as e:
        logger.error(f"Error stopping AI workflow: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/process-client', methods=['POST'])
def process_client():
    """Process a new client using AI analysis."""
    try:
        data = request.json
        if not data or not data.get('name'):
            return jsonify({'success': False, 'error': 'Client data is required'}), 400
        
        # Run the async client processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal.process_new_client(data))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/research-case-law', methods=['POST'])
def research_case_law():
    """Research case law for a specific case."""
    try:
        data = request.json
        if not data or not data.get('title'):
            return jsonify({'success': False, 'error': 'Case data is required'}), 400
        
        # Run the async case law research
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal.research_case_law(data))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error researching case law: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/generate-document', methods=['POST'])
def generate_document():
    """Generate a legal document using AI."""
    try:
        data = request.json
        if not data or not data.get('document_type'):
            return jsonify({'success': False, 'error': 'Document type is required'}), 400
        
        # Run the async document generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal.generate_document(
            data['document_type'], 
            data.get('case_data', {})
        ))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get AI activity logs."""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = ai_virtual_paralegal.get_logs(limit)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        })
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get AI Virtual Paralegal dashboard data."""
    try:
        status = ai_virtual_paralegal.get_status()
        recent_logs = ai_virtual_paralegal.get_logs(10)
        
        # Mock dashboard statistics
        dashboard_data = {
            'ai_status': status,
            'capabilities': [
                {
                    'name': 'Case Law Research',
                    'status': 'active',
                    'description': 'CourtListener API + ChromaDB',
                    'last_used': '2025-09-09 19:15:32'
                },
                {
                    'name': 'Document Generation',
                    'status': 'active',
                    'description': 'AI-powered form creation',
                    'last_used': '2025-09-09 19:16:45'
                },
                {
                    'name': 'Task Scheduling',
                    'status': 'active',
                    'description': 'Automated deadline management',
                    'last_used': '2025-09-09 19:17:12'
                },
                {
                    'name': 'Client Communication',
                    'status': 'active',
                    'description': 'AI-generated updates',
                    'last_used': '2025-09-09 19:18:03'
                }
            ],
            'workflow_steps': [
                'Analyze New Client',
                'Research Case Law',
                'Generate Documents',
                'Schedule Tasks',
                'Monitor Deadlines',
                'Update Client'
            ],
            'recent_activity': recent_logs,
            'statistics': {
                'cases_processed_today': 12,
                'documents_generated': 8,
                'tasks_scheduled': 15,
                'clients_updated': 5
            }
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
    except Exception as e:
        logger.error(f"Error getting dashboard: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/execute-task', methods=['POST'])
def execute_task():
    """Execute a specific AI task."""
    try:
        data = request.json
        task_name = data.get('task_name', 'Unknown Task')
        
        # Simulate task execution
        ai_virtual_paralegal._log("info", f"Executing task: {task_name}", "Task Executor")
        
        # Simulate processing time
        import time
        time.sleep(1)
        
        ai_virtual_paralegal._log("success", f"Completed task: {task_name}", "Task Executor")
        
        return jsonify({
            'success': True,
            'message': f'Task "{task_name}" executed successfully',
            'execution_time': '1.0 seconds'
        })
    except Exception as e:
        logger.error(f"Error executing task: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
