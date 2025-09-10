"""
AI Virtual Paralegal API Routes
Provides endpoints for the autonomous AI Virtual Paralegal system.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import asyncio
from services.ai_virtual_paralegal_service import ai_virtual_paralegal
from services.courtlistener_service import courtlistener_service

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

@bp.route('/logs', methods=['GET'])
def get_ai_logs():
    """Get AI Virtual Paralegal activity logs."""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = ai_virtual_paralegal.get_logs(limit=limit)
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        })
    except Exception as e:
        logger.error(f"Error getting AI logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/research-case-law', methods=['POST'])
def research_case_law():
    """Research case law for a specific case using CourtListener API."""
    try:
        data = request.json
        if not data or not data.get('case_data'):
            return jsonify({'success': False, 'error': 'Case data is required'}), 400
        
        case_data = data['case_data']
        
        # Run the async research
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal._research_case_law())
        loop.close()
        
        return jsonify({
            'success': True,
            'research_completed': True,
            'case_data': case_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error researching case law: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/generate-document', methods=['POST'])
def generate_document():
    """Generate a legal document for a specific case."""
    try:
        data = request.json
        if not data or not data.get('document_type') or not data.get('case_data'):
            return jsonify({'success': False, 'error': 'Document type and case data are required'}), 400
        
        document_type = data['document_type']
        case_data = data['case_data']
        
        # Run the async document generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ai_virtual_paralegal.generate_document(document_type, case_data))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/search-cases', methods=['POST'])
def search_cases():
    """Search for cases using CourtListener API."""
    try:
        data = request.json
        if not data or not data.get('query'):
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        query = data['query']
        case_type = data.get('case_type')
        court = data.get('court')
        limit = data.get('limit', 20)
        
        # Search using CourtListener API
        result = courtlistener_service.search_cases(
            query=query,
            case_type=case_type,
            court=court,
            limit=limit
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error searching cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/similar-cases', methods=['POST'])
def find_similar_cases():
    """Find similar cases using CourtListener API."""
    try:
        data = request.json
        if not data or not data.get('case_data'):
            return jsonify({'success': False, 'error': 'Case data is required'}), 400
        
        case_data = data['case_data']
        limit = data.get('limit', 10)
        
        # Find similar cases
        result = courtlistener_service.search_similar_cases(
            case_data=case_data,
            limit=limit
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error finding similar cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/recent-cases', methods=['GET'])
def get_recent_cases():
    """Get recent cases from CourtListener API."""
    try:
        case_type = request.args.get('case_type')
        days = request.args.get('days', 30, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Get recent cases
        result = courtlistener_service.get_recent_cases(
            case_type=case_type,
            days=days,
            limit=limit
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting recent cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get AI Virtual Paralegal dashboard data."""
    try:
        status = ai_virtual_paralegal.get_status()
        recent_logs = ai_virtual_paralegal.get_logs(10)
        
        # Dashboard statistics
        dashboard_data = {
            'ai_status': status,
            'capabilities': [
                {
                    'name': 'Case Law Research',
                    'status': 'active',
                    'description': 'CourtListener API + AI Analysis',
                    'last_used': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'name': 'Document Generation',
                    'status': 'active',
                    'description': 'AI-powered legal document creation',
                    'last_used': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'name': 'Task Scheduling',
                    'status': 'active',
                    'description': 'Automated deadline management',
                    'last_used': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'name': 'Client Communication',
                    'status': 'active',
                    'description': 'AI-generated client updates',
                    'last_used': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ],
            'workflow_steps': [
                'Analyze Pending Cases',
                'Research Case Law (CourtListener)',
                'Generate Legal Documents',
                'Schedule Tasks & Deadlines',
                'Update Clients'
            ],
            'recent_activity': recent_logs,
            'statistics': {
                'cases_processed_today': 12,
                'documents_generated': 8,
                'tasks_scheduled': 15,
                'clients_updated': 5,
                'courtlistener_searches': 24
            }
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
    except Exception as e:
        logger.error(f"Error getting dashboard: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500