"""
Case notes API routes.

This module provides API endpoints for managing case notes:
- List notes for a case
- Add notes to a case
- Update and delete notes
"""
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from backend.models.case import Case, CaseNote, CaseEvent, EventType
from backend.models.user import User

case_note_bp = Blueprint('case_note', __name__)

# Helper function to record note events
def record_note_event(
    case_id: UUID,
    event_type: EventType,
    description: str,
    user_id: UUID,
    note_id: Optional[UUID] = None,
    event_metadata: Optional[Dict[str, Any]] = None
) -> CaseEvent:
    """Record a note-related event in the case timeline."""
    event_metadata_dict = event_metadata or {}
    if note_id:
        event_metadata_dict["note_id"] = str(note_id)
        
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

@case_note_bp.route('/api/cases/<uuid:case_id>/notes', methods=['GET'])
@jwt_required()
def get_case_notes(case_id):
    """
    Get all notes for a case.
    
    Query parameters:
    - sort: Sort field (created_at)
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
    sort_order = request.args.get('order', 'desc')
    
    # Start building the query
    query = CaseNote.query.filter_by(case_id=case_id)
    
    # Don't show private notes to clients unless they created them
    if user.role == 'client':
        query = query.filter((CaseNote.is_private == False) | (CaseNote.created_by == user_id))
    
    # Apply sorting
    if sort_order == 'asc':
        query = query.order_by(CaseNote.created_at)
    else:
        query = query.order_by(CaseNote.created_at.desc())
    
    # Get notes with user information
    notes = query.options(joinedload(CaseNote.user)).all()
    
    # Format the response
    result = []
    for note in notes:
        user_name = "Unknown User"
        if note.user:
            user_name = f"{note.user.first_name} {note.user.last_name}"
            
        result.append({
            "id": note.id,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "is_private": note.is_private,
            "created_by": {
                "id": note.created_by,
                "name": user_name
            }
        })
    
    return jsonify(result)

@case_note_bp.route('/api/cases/<uuid:case_id>/notes', methods=['POST'])
@jwt_required()
def create_case_note(case_id):
    """Add a new note to a case."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the case
    case = Case.query.get_or_404(case_id)
    
    # Check permissions
    if (user.role == 'client' and case.client_id != user_id) or \
       (user.role == 'attorney' and case.assigned_to != user_id and not user.is_admin):
        return jsonify({"error": "You don't have permission to add notes to this case"}), 403
    
    # Get request data
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('content'):
        return jsonify({"error": "Note content is required"}), 400
    
    try:
        # Create new note
        new_note = CaseNote(
            case_id=case_id,
            content=data['content'],
            created_by=user_id,
            is_private=data.get('is_private', False)
        )
        
        # Save to database
        current_app.db.session.add(new_note)
        current_app.db.session.commit()
        
        # Record the event (don't record private notes in the timeline)
        if not bool(new_note.is_private):
            record_note_event(
                case_id=case_id,
                event_type=EventType.NOTE_ADDED,
                description=f"New note added" + (f" by {user.first_name} {user.last_name}" if user else ""),
                user_id=user_id,
                note_id=UUID(str(new_note.id))
            )
        
        return jsonify({
            "id": new_note.id,
            "content": new_note.content,
            "created_at": new_note.created_at.isoformat(),
            "is_private": new_note.is_private,
            "message": "Note added successfully"
        }), 201
        
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error adding note: {str(e)}")
        return jsonify({"error": "Failed to add note"}), 500

@case_note_bp.route('/api/notes/<uuid:note_id>', methods=['PUT'])
@jwt_required()
def update_case_note(note_id):
    """Update an existing note."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the note
    note = CaseNote.query.get_or_404(note_id)
    
    # Users can only edit their own notes, unless they are admins
    if note.created_by != user_id and not user.is_admin:
        return jsonify({"error": "You can only edit your own notes"}), 403
    
    # Get request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    
    try:
        # Update note content
        if 'content' in data:
            note.content = data['content']
        
        # Update privacy setting
        if 'is_private' in data:
            note.is_private = data['is_private']
        
        # Save changes
        current_app.db.session.commit()
        
        return jsonify({
            "id": note.id,
            "content": note.content,
            "is_private": note.is_private,
            "message": "Note updated successfully"
        })
        
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error updating note: {str(e)}")
        return jsonify({"error": "Failed to update note"}), 500

@case_note_bp.route('/api/notes/<uuid:note_id>', methods=['DELETE'])
@jwt_required()
def delete_case_note(note_id):
    """Delete a note."""
    # Get the current user
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Get the note
    note = CaseNote.query.get_or_404(note_id)
    
    # Users can only delete their own notes, unless they are admins
    if note.created_by != user_id and not user.is_admin:
        return jsonify({"error": "You can only delete your own notes"}), 403
    
    try:
        # Store case ID before deletion for event recording
        case_id = note.case_id
        
        # Delete the note
        current_app.db.session.delete(note)
        current_app.db.session.commit()
        
        # Record the deletion event (only for admins or if it wasn't private)
        if user.is_admin or not note.is_private:
            record_note_event(
                case_id=case_id,
                event_type=EventType.OTHER,
                description=f"Note deleted by {user.first_name} {user.last_name}",
                user_id=user_id
            )
        
        return jsonify({"message": "Note deleted successfully"})
        
    except Exception as e:
        current_app.db.session.rollback()
        current_app.logger.error(f"Error deleting note: {str(e)}")
        return jsonify({"error": "Failed to delete note"}), 500 