"""
Case deadlines API routes.

This module provides the API endpoints for managing case deadlines:
- List deadlines for a case
- Create, update, and delete deadlines
- Mark deadlines as completed
- Get upcoming deadlines
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from backend.models.case import (
    Case, CaseEvent, CaseDeadline,
    EventType, Priority, DeadlineStatus
)
from backend.models.user import User
from backend.utils.auth import role_required
from backend.utils.pagination import paginate_results

case_deadline_bp = Blueprint('case_deadline', __name__)

# Helper function to record case events for deadlines
def record_deadline_event(
    case_id: UUID,
    event_type: EventType,
    description: str,
    user_id: UUID,
    deadline_id: Optional[UUID] = None,
    event_metadata: Optional[Dict[str, Any]] = None
) -> CaseEvent:
    """Record a deadline-related event in the case timeline."""
    event_metadata_dict = event_metadata or {}
    if deadline_id:
        event_metadata_dict["deadline_id"] = str(deadline_id)
        
    # Create the event
    new_event = CaseEvent(
        case_id=case_id,
        event_type=event_type,
        description=description,
        created_by=user_id,
        event_metadata=event_metadata_dict
    )
    current_app.db.session.add(new_event)
    current_app.db.session.commit()
    return new_event

#
# Deadline Routes
#

@case_deadline_bp.route('/api/cases/<uuid:case_id>/deadlines', methods=['GET'])
@jwt_required()
def get_deadlines(case_id):
    """
    Get all deadlines for a case.
    
    Query parameters:
    - status: Filter by deadline status (pending, completed, missed)
    - priority: Filter by priority (low, medium, high, critical)
    - sort: Sort field (due_date, created_at, priority)
    - order: Sort order (asc, desc)
    """
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the case
    case = Case.query.get_or_404(case_id)
    
    # Check permissions
    if (user.role == 'client' and case.client_id != user_id) or \
       (user.role == 'attorney' and case.assigned_to != user_id and not user.is_admin):
        return jsonify({"error": "You don't have permission to view this case"}), 403
    
    # Get query parameters
    status = request.args.get('status')
    priority = request.args.get('priority')
    sort_by = request.args.get('sort', 'due_date')
    sort_order = request.args.get('order', 'asc')
    
    # Start building the query
    query = CaseDeadline.query.filter_by(case_id=case_id)
    
    # Apply filters
    if status:
        query = query.filter(CaseDeadline.status == DeadlineStatus[status.upper()])
    
    if priority:
        query = query.filter(CaseDeadline.priority == Priority[priority.upper()])
    
    # Apply sorting
    if sort_order == 'desc':
        query = query.order_by(getattr(CaseDeadline, sort_by).desc())
    else:
        query = query.order_by(getattr(CaseDeadline, sort_by))
    
    # Get the deadlines with user information
    deadlines = query.options(joinedload(CaseDeadline.user)).all()
    
    # Format the response
    result = []
    for deadline in deadlines:
        user_name = "Unknown User"
        if deadline.user:
            user_name = f"{deadline.user.first_name} {deadline.user.last_name}"
            
        result.append({
            "id": deadline.id,
            "title": deadline.title,
            "description": deadline.description,
            "due_date": deadline.due_date.isoformat(),
            "priority": deadline.priority.value,
            "status": deadline.status.value,
            "created_at": deadline.created_at.isoformat(),
            "created_by": {
                "id": deadline.created_by,
                "name": user_name
            }
        })
    
    return jsonify(result)

@case_deadline_bp.route('/api/cases/<uuid:case_id>/deadlines', methods=['POST'])
@jwt_required()
def create_deadline(case_id):
    """Create a new deadline for a case."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the case
    case = Case.query.get_or_404(case_id)
    
    # Check permissions (only attorneys and admins can create deadlines)
    if user.role == 'client' and not user.is_admin:
        return jsonify({"error": "Clients cannot create deadlines"}), 403
    
    if user.role == 'attorney' and case.assigned_to != user_id and not user.is_admin:
        return jsonify({"error": "You are not assigned to this case"}), 403
    
    # Get request data
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('due_date'):
        return jsonify({"error": "Title and due date are required"}), 400
    
    try:
        # Parse due date
        due_date = datetime.fromisoformat(data['due_date'])
        
        # Create new deadline
        new_deadline = CaseDeadline(
            case_id=case_id,
            title=data['title'],
            description=data.get('description'),
            due_date=due_date,
            priority=Priority[data.get('priority', 'MEDIUM').upper()],
            status=DeadlineStatus.PENDING,
            created_by=user_id
        )
        
        # Save to database
        current_app.db.session.add(new_deadline)
        current_app.db.session.commit()
        
        # Record the event
        record_deadline_event(
            case_id=case_id,
            event_type=EventType.DEADLINE_ADDED,
            description=f"New deadline added: {data['title']} (due {due_date.strftime('%Y-%m-%d')})",
            user_id=user_id,
            deadline_id=UUID(str(new_deadline.id))
        )
        
        return jsonify({
            "id": new_deadline.id,
            "title": new_deadline.title,
            "due_date": new_deadline.due_date.isoformat(),
            "message": "Deadline created successfully"
        }), 201
        
    except ValueError:
        return jsonify({"error": "Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error creating deadline: {str(e)}")
        return jsonify({"error": "Failed to create deadline"}), 500

@case_deadline_bp.route('/api/deadlines/<uuid:deadline_id>', methods=['PUT'])
@jwt_required()
def update_deadline(deadline_id):
    """Update an existing deadline."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the deadline
    deadline = CaseDeadline.query.get_or_404(deadline_id)
    
    # Get the case
    case = Case.query.get_or_404(deadline.case_id)
    
    # Check permissions
    if user.role == 'client' and not user.is_admin:
        return jsonify({"error": "Clients cannot update deadlines"}), 403
    
    if user.role == 'attorney' and case.assigned_to != user_id and not user.is_admin:
        return jsonify({"error": "You are not assigned to this case"}), 403
    
    # Get request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    
    try:
        # Track changes for event logging
        changes = []
        
        # Update basic fields
        if 'title' in data and data['title'] != deadline.title:
            deadline.title = data['title']
            changes.append(f"Title updated to '{data['title']}'")
            
        if 'description' in data and data['description'] != deadline.description:
            deadline.description = data['description']
            changes.append("Description updated")
            
        # Update due date
        if 'due_date' in data:
            try:
                new_due_date = datetime.fromisoformat(data['due_date'])
                if new_due_date != deadline.due_date:
                    old_date = deadline.due_date.strftime('%Y-%m-%d')
                    deadline.due_date = new_due_date
                    new_date = new_due_date.strftime('%Y-%m-%d')
                    changes.append(f"Due date changed from {old_date} to {new_date}")
            except ValueError:
                return jsonify({"error": "Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
                
        # Update priority
        if 'priority' in data:
            try:
                new_priority = Priority[data['priority'].upper()]
                if new_priority != deadline.priority:
                    old_priority = deadline.priority.value
                    deadline.priority = new_priority
                    changes.append(f"Priority changed from {old_priority} to {new_priority.value}")
            except KeyError:
                return jsonify({"error": f"Invalid priority value: {data['priority']}"}), 400
                
        # Update status
        if 'status' in data:
            try:
                new_status = DeadlineStatus[data['status'].upper()]
                if new_status != deadline.status:
                    old_status = deadline.status.value
                    deadline.status = new_status
                    changes.append(f"Status changed from {old_status} to {new_status.value}")
                    
                    # If marked as completed, record special event
                    if new_status == DeadlineStatus.COMPLETED:
                        record_deadline_event(
                            case_id=deadline.case_id,
                            event_type=EventType.DEADLINE_UPDATED,
                            description=f"Deadline completed: {deadline.title}",
                            user_id=user_id,
                            deadline_id=UUID(str(deadline.id)),
                            event_metadata={"action": "completed"}
                        )
            except KeyError:
                return jsonify({"error": f"Invalid status value: {data['status']}"}), 400
        
        # Save changes
        current_app.db.session.commit()
        
        # If there were changes but not already logged as completed, record generic update
        if changes and not ('status' in data and data['status'].upper() == 'COMPLETED'):
            record_deadline_event(
                case_id=deadline.case_id,
                event_type=EventType.DEADLINE_UPDATED,
                description=f"Deadline updated: {', '.join(changes)}",
                user_id=user_id,
                deadline_id=UUID(str(deadline.id))
            )
        
        return jsonify({
            "id": deadline.id,
            "title": deadline.title,
            "due_date": deadline.due_date.isoformat(),
            "status": deadline.status.value,
            "message": "Deadline updated successfully",
            "changes": changes
        })
        
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error updating deadline: {str(e)}")
        return jsonify({"error": "Failed to update deadline"}), 500

@case_deadline_bp.route('/api/deadlines/<uuid:deadline_id>', methods=['DELETE'])
@jwt_required()
def delete_deadline(deadline_id):
    """Delete a deadline."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the deadline
    deadline = CaseDeadline.query.get_or_404(deadline_id)
    
    # Get the case
    case = Case.query.get_or_404(deadline.case_id)
    
    # Check permissions (only attorneys assigned to the case and admins can delete deadlines)
    if not user.is_admin:
        if user.role != 'attorney' or case.assigned_to != user_id:
            return jsonify({"error": "You don't have permission to delete this deadline"}), 403
    
    try:
        # Record the event before deletion
        deadline_title = deadline.title
        case_id = deadline.case_id
        
        # Delete the deadline
        current_app.db.session.delete(deadline)
        current_app.db.session.commit()
        
        # Record event
        record_deadline_event(
            case_id=case_id,
            event_type=EventType.OTHER,
            description=f"Deadline deleted: {deadline_title}",
            user_id=user_id
        )
        
        return jsonify({"message": "Deadline deleted successfully"})
        
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error deleting deadline: {str(e)}")
        return jsonify({"error": "Failed to delete deadline"}), 500

@case_deadline_bp.route('/api/deadlines/upcoming', methods=['GET'])
@jwt_required()
def get_upcoming_deadlines():
    """
    Get upcoming deadlines for the authenticated user.
    
    Query parameters:
    - days: Number of days to look ahead (default: 14)
    - status: Filter by status (default: pending)
    - limit: Maximum number of deadlines to return (default: 10)
    """
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get query parameters
    days = request.args.get('days', 14, type=int)
    limit = request.args.get('limit', 10, type=int)
    status = request.args.get('status', 'PENDING')
    
    # Calculate date range
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today.replace(hour=23, minute=59, second=59) + datetime.timedelta(days=days)
    
    # Build query based on user role
    if user.role == 'client':
        # For clients, get deadlines from their cases
        query = CaseDeadline.query.join(Case).filter(
            Case.client_id == user_id,
            CaseDeadline.due_date >= today,
            CaseDeadline.due_date <= end_date
        )
    elif user.role == 'attorney':
        # For attorneys, get deadlines from cases assigned to them
        query = CaseDeadline.query.join(Case).filter(
            Case.assigned_to == user_id,
            CaseDeadline.due_date >= today,
            CaseDeadline.due_date <= end_date
        )
    else:
        # For admins, get all deadlines
        query = CaseDeadline.query.filter(
            CaseDeadline.due_date >= today,
            CaseDeadline.due_date <= end_date
        )
    
    # Apply status filter if provided
    if status:
        query = query.filter(CaseDeadline.status == DeadlineStatus[status.upper()])
    
    # Order by due date and limit results
    deadlines = query.order_by(CaseDeadline.due_date).limit(limit).all()
    
    # Format response
    result = []
    for deadline in deadlines:
        # Get case information
        case = Case.query.get(deadline.case_id)
        
        result.append({
            "id": deadline.id,
            "title": deadline.title,
            "description": deadline.description,
            "due_date": deadline.due_date.isoformat(),
            "priority": deadline.priority.value,
            "status": deadline.status.value,
            "case": {
                "id": case.id,
                "title": case.title,
                "case_type": case.case_type.value
            }
        })
    
    return jsonify(result) 