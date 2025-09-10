"""
Virtual Paralegal CRM API Routes
Provides CRM functionality for virtual paralegals to manage clients, cases, and tasks.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('virtual_paralegal_crm', __name__, url_prefix='/api/v1/virtual-paralegal')

# Mock data storage (in production, this would be a database)
clients_db = []
cases_db = []
tasks_db = []
next_id = 1

def get_next_id():
    global next_id
    next_id += 1
    return next_id

@bp.route('/clients', methods=['GET'])
def get_clients():
    """Get all clients with optional filtering."""
    try:
        status = request.args.get('status')
        search = request.args.get('search', '').lower()
        
        filtered_clients = clients_db.copy()
        
        if status:
            filtered_clients = [c for c in filtered_clients if c.get('status') == status]
        
        if search:
            filtered_clients = [
                c for c in filtered_clients 
                if search in c.get('name', '').lower() or 
                   search in c.get('email', '').lower()
            ]
        
        return jsonify({
            'success': True,
            'clients': filtered_clients,
            'total': len(filtered_clients)
        })
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/clients', methods=['POST'])
def create_client():
    """Create a new client."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        client = {
            'id': get_next_id(),
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'status': data.get('status', 'active'),
            'cases': 0,
            'lastContact': datetime.now().strftime('%Y-%m-%d'),
            'avatar': ''.join([name[0] for name in data['name'].split()[:2]]).upper(),
            'createdAt': datetime.now().isoformat(),
            'notes': data.get('notes', '')
        }
        
        clients_db.append(client)
        
        return jsonify({
            'success': True,
            'client': client
        }), 201
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Update an existing client."""
    try:
        data = request.json
        
        client = next((c for c in clients_db if c['id'] == client_id), None)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Update fields
        for key, value in data.items():
            if key in client:
                client[key] = value
        
        client['updatedAt'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'client': client
        })
    except Exception as e:
        logger.error(f"Error updating client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Delete a client."""
    try:
        global clients_db
        clients_db = [c for c in clients_db if c['id'] != client_id]
        
        # Also delete associated cases and tasks
        global cases_db, tasks_db
        cases_db = [c for c in cases_db if c.get('clientId') != client_id]
        tasks_db = [t for t in tasks_db if t.get('clientId') != client_id]
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/cases', methods=['GET'])
def get_cases():
    """Get all cases with optional filtering."""
    try:
        client_id = request.args.get('clientId')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        filtered_cases = cases_db.copy()
        
        if client_id:
            filtered_cases = [c for c in filtered_cases if c.get('clientId') == int(client_id)]
        
        if status:
            filtered_cases = [c for c in filtered_cases if c.get('status') == status]
        
        if priority:
            filtered_cases = [c for c in filtered_cases if c.get('priority') == priority]
        
        return jsonify({
            'success': True,
            'cases': filtered_cases,
            'total': len(filtered_cases)
        })
    except Exception as e:
        logger.error(f"Error fetching cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/cases', methods=['POST'])
def create_case():
    """Create a new case."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'clientId', 'type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        case = {
            'id': get_next_id(),
            'title': data['title'],
            'clientId': data['clientId'],
            'type': data['type'],
            'status': data.get('status', 'pending'),
            'priority': data.get('priority', 'medium'),
            'dueDate': data.get('dueDate', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'progress': data.get('progress', 0),
            'documents': data.get('documents', 0),
            'lastUpdate': datetime.now().strftime('%Y-%m-%d'),
            'createdAt': datetime.now().isoformat(),
            'description': data.get('description', ''),
            'notes': data.get('notes', '')
        }
        
        cases_db.append(case)
        
        # Update client's case count
        client = next((c for c in clients_db if c['id'] == data['clientId']), None)
        if client:
            client['cases'] += 1
        
        return jsonify({
            'success': True,
            'case': case
        }), 201
    except Exception as e:
        logger.error(f"Error creating case: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/cases/<int:case_id>', methods=['PUT'])
def update_case(case_id):
    """Update an existing case."""
    try:
        data = request.json
        
        case = next((c for c in cases_db if c['id'] == case_id), None)
        if not case:
            return jsonify({'success': False, 'error': 'Case not found'}), 404
        
        # Update fields
        for key, value in data.items():
            if key in case:
                case[key] = value
        
        case['lastUpdate'] = datetime.now().strftime('%Y-%m-%d')
        case['updatedAt'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'case': case
        })
    except Exception as e:
        logger.error(f"Error updating case: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering."""
    try:
        case_id = request.args.get('caseId')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        filtered_tasks = tasks_db.copy()
        
        if case_id:
            filtered_tasks = [t for t in filtered_tasks if t.get('caseId') == int(case_id)]
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.get('status') == status]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority]
        
        return jsonify({
            'success': True,
            'tasks': filtered_tasks,
            'total': len(filtered_tasks)
        })
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'caseId']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        task = {
            'id': get_next_id(),
            'title': data['title'],
            'caseId': data['caseId'],
            'type': data.get('type', 'general'),
            'status': data.get('status', 'pending'),
            'priority': data.get('priority', 'medium'),
            'dueDate': data.get('dueDate', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')),
            'createdAt': datetime.now().isoformat(),
            'description': data.get('description', ''),
            'notes': data.get('notes', '')
        }
        
        tasks_db.append(task)
        
        return jsonify({
            'success': True,
            'task': task
        }), 201
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        stats = {
            'clients': {
                'total': len(clients_db),
                'active': len([c for c in clients_db if c.get('status') == 'active']),
                'inactive': len([c for c in clients_db if c.get('status') == 'inactive'])
            },
            'cases': {
                'total': len(cases_db),
                'pending': len([c for c in cases_db if c.get('status') == 'pending']),
                'in_progress': len([c for c in cases_db if c.get('status') == 'in_progress']),
                'completed': len([c for c in cases_db if c.get('status') == 'completed'])
            },
            'tasks': {
                'total': len(tasks_db),
                'pending': len([t for t in tasks_db if t.get('status') == 'pending']),
                'in_progress': len([t for t in tasks_db if t.get('status') == 'in_progress']),
                'completed': len([t for t in tasks_db if t.get('status') == 'completed']),
                'overdue': len([t for t in tasks_db if t.get('status') == 'overdue'])
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Initialize with some sample data
def init_sample_data():
    """Initialize with sample data for demonstration."""
    global clients_db, cases_db, tasks_db, next_id
    
    if not clients_db:  # Only initialize if empty
        clients_db.extend([
            {
                'id': 1,
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'phone': '(555) 123-4567',
                'status': 'active',
                'cases': 2,
                'lastContact': '2025-09-08',
                'avatar': 'JS',
                'createdAt': '2025-09-01T10:00:00',
                'notes': 'Prefers email communication'
            },
            {
                'id': 2,
                'name': 'Maria Garcia',
                'email': 'maria.garcia@email.com',
                'phone': '(555) 234-5678',
                'status': 'active',
                'cases': 1,
                'lastContact': '2025-09-07',
                'avatar': 'MG',
                'createdAt': '2025-09-02T14:30:00',
                'notes': 'Spanish speaker'
            }
        ])
        
        cases_db.extend([
            {
                'id': 1,
                'title': 'Immigration - Green Card Application',
                'clientId': 1,
                'type': 'Immigration',
                'status': 'in_progress',
                'priority': 'high',
                'dueDate': '2025-10-15',
                'progress': 65,
                'documents': 12,
                'lastUpdate': '2025-09-09',
                'createdAt': '2025-09-01T10:00:00',
                'description': 'I-485 adjustment of status application',
                'notes': 'Waiting for biometrics appointment'
            },
            {
                'id': 2,
                'title': 'Divorce Proceedings',
                'clientId': 1,
                'type': 'Family Law',
                'status': 'pending',
                'priority': 'medium',
                'dueDate': '2025-11-20',
                'progress': 30,
                'documents': 8,
                'lastUpdate': '2025-09-05',
                'createdAt': '2025-09-03T09:15:00',
                'description': 'Uncontested divorce with minor children',
                'notes': 'Need to file financial disclosures'
            }
        ])
        
        tasks_db.extend([
            {
                'id': 1,
                'title': 'File I-485 Application',
                'caseId': 1,
                'type': 'document',
                'status': 'pending',
                'priority': 'high',
                'dueDate': '2025-09-15',
                'createdAt': '2025-09-01T10:00:00',
                'description': 'Submit completed I-485 form with supporting documents',
                'notes': 'All documents ready, just need final review'
            },
            {
                'id': 2,
                'title': 'Schedule Biometrics Appointment',
                'caseId': 1,
                'type': 'appointment',
                'status': 'in_progress',
                'priority': 'medium',
                'dueDate': '2025-09-12',
                'createdAt': '2025-09-02T11:00:00',
                'description': 'Call USCIS to schedule biometrics appointment',
                'notes': 'Client prefers morning appointments'
            }
        ])
        
        next_id = 3

# Initialize sample data when module is imported
init_sample_data()
