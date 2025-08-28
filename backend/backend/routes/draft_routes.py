from flask import Blueprint, request, jsonify
from datetime import datetime
from services.draft_service import DraftService
from services.auth_service import login_required
from models.draft import Draft

drafts = Blueprint('drafts', __name__)
draft_service = DraftService()

@drafts.route('/api/drafts/<form_type>', methods=['POST'])
@login_required
def save_draft(form_type):
    try:
        data = request.get_json()
        user_id = request.user.id
        
        draft = draft_service.save_draft(
            user_id=user_id,
            form_type=form_type,
            data=data['values'],
            timestamp=data.get('timestamp', datetime.utcnow().timestamp())
        )
        
        return jsonify({
            'message': 'Draft saved successfully',
            'draft_id': draft.id,
            'timestamp': draft.timestamp
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@drafts.route('/api/drafts/<form_type>/latest', methods=['GET'])
@login_required
def get_latest_draft(form_type):
    try:
        user_id = request.user.id
        draft = draft_service.get_latest_draft(user_id, form_type)
        
        if not draft:
            return jsonify({'message': 'No draft found'}), 404
            
        return jsonify({
            'values': draft.data,
            'timestamp': draft.timestamp,
            'draft_id': draft.id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@drafts.route('/api/drafts/<form_type>', methods=['GET'])
@login_required
def get_all_drafts(form_type):
    try:
        user_id = request.user.id
        drafts = draft_service.get_all_drafts(user_id, form_type)
        
        return jsonify({
            'drafts': [{
                'id': draft.id,
                'values': draft.data,
                'timestamp': draft.timestamp
            } for draft in drafts]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@drafts.route('/api/drafts/<form_type>', methods=['DELETE'])
@login_required
def delete_draft(form_type):
    try:
        user_id = request.user.id
        draft_service.delete_drafts(user_id, form_type)
        
        return jsonify({
            'message': 'Drafts deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@drafts.route('/api/drafts/<form_type>/<draft_id>', methods=['DELETE'])
@login_required
def delete_specific_draft(form_type, draft_id):
    try:
        user_id = request.user.id
        draft_service.delete_draft(user_id, form_type, draft_id)
        
        return jsonify({
            'message': 'Draft deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 