from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import os
import json
from datetime import datetime
from backend.services.auth_service import require_auth, get_current_user
from backend.services.document_service import generate_document
from backend.services.ai_service import analyze_eligibility

bp = Blueprint('immigration', __name__)

@bp.route('/forms', methods=['GET'])
def get_immigration_forms():
    """Get available immigration forms"""
    try:
        # In a real app, these would be fetched from a database
        available_forms = [
            {
                "id": "i-90",
                "name": "I-90 Application to Replace Permanent Resident Card",
                "description": "Use this form to apply for a replacement or renewal of your Green Card."
            },
            {
                "id": "i-130",
                "name": "I-130 Petition for Alien Relative",
                "description": "Use this form if you are a U.S. citizen or lawful permanent resident and want to establish the relationship to certain alien relatives who wish to immigrate to the United States."
            },
            {
                "id": "i-485",
                "name": "I-485 Application to Register Permanent Residence",
                "description": "Use this form to apply for lawful permanent resident status."
            },
            {
                "id": "n-400",
                "name": "N-400 Application for Naturalization",
                "description": "Use this form to apply for U.S. citizenship."
            }
        ]
        return jsonify({"forms": available_forms})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/forms/<form_id>', methods=['GET'])
def get_form_details(form_id):
    """Get details for a specific immigration form"""
    try:
        # In a real app, this would be fetched from a database
        form_details = {
            "i-90": {
                "id": "i-90",
                "name": "I-90 Application to Replace Permanent Resident Card",
                "description": "Use this form to apply for a replacement or renewal of your Green Card.",
                "fee": 455,
                "processing_time": "8-10 months",
                "required_documents": [
                    "Copy of your Permanent Resident Card",
                    "Government-issued identification with photograph",
                    "Birth certificate or passport",
                    "Evidence of name change (if applicable)"
                ],
                "eligibility_criteria": [
                    "You are a lawful permanent resident of the United States",
                    "Your card is expired or will expire within the next 6 months",
                    "Your card is lost, stolen, damaged, or destroyed",
                    "Your name or other biographic information has changed"
                ]
            },
            "i-130": {
                "id": "i-130",
                "name": "I-130 Petition for Alien Relative",
                "description": "Use this form if you are a U.S. citizen or lawful permanent resident and want to establish the relationship to certain alien relatives who wish to immigrate to the United States.",
                "fee": 535,
                "processing_time": "7-15 months",
                "required_documents": [
                    "Proof of your U.S. citizenship or permanent residence",
                    "Evidence of qualifying relationship",
                    "Marriage certificate (if applicable)",
                    "Divorce decrees from previous marriages (if applicable)"
                ],
                "eligibility_criteria": [
                    "You are a U.S. citizen or lawful permanent resident",
                    "You have a qualifying relationship with the relative",
                    "You can financially support the relative at 125% above the poverty guidelines"
                ]
            },
            "i-485": {
                "id": "i-485",
                "name": "I-485 Application to Register Permanent Residence",
                "description": "Use this form to apply for lawful permanent resident status.",
                "fee": 1140,
                "processing_time": "8-14 months",
                "required_documents": [
                    "Birth certificate",
                    "Valid passport",
                    "Two passport-style photos",
                    "Medical examination (Form I-693)",
                    "Approved immigrant petition (if applicable)"
                ],
                "eligibility_criteria": [
                    "You are physically present in the United States",
                    "You are eligible to receive an immigrant visa",
                    "An immigrant visa is immediately available at the time of filing"
                ]
            },
            "n-400": {
                "id": "n-400",
                "name": "N-400 Application for Naturalization",
                "description": "Use this form to apply for U.S. citizenship.",
                "fee": 725,
                "processing_time": "8-12 months",
                "required_documents": [
                    "Permanent Resident Card (Green Card)",
                    "Tax returns for the past 5 years",
                    "Travel history for the past 5 years",
                    "Two passport-style photos"
                ],
                "eligibility_criteria": [
                    "You are at least 18 years old",
                    "You have been a permanent resident for at least 5 years (or 3 years if married to a U.S. citizen)",
                    "You have continuous residence and physical presence in the U.S.",
                    "You can read, write, speak, and understand English",
                    "You have knowledge of U.S. history and government",
                    "You are a person of good moral character"
                ]
            }
        }
        
        if form_id not in form_details:
            return jsonify({"error": "Form not found"}), 404
            
        return jsonify(form_details[form_id])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/check-eligibility', methods=['POST'])
def check_eligibility():
    """Check eligibility for an immigration form"""
    try:
        data = request.json
        if not data or not data.get('form_id') or not data.get('answers'):
            raise BadRequest("Missing form_id or answers")
            
        form_id = data['form_id']
        answers = data['answers']
        
        # This would call an AI service in a real application
        eligibility_result = analyze_eligibility(form_id, answers)
        
        return jsonify(eligibility_result)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/submit-form', methods=['POST'])
@require_auth
def submit_immigration_form():
    """Submit an immigration form"""
    try:
        current_user = get_current_user()
        data = request.json
        
        if not data or not data.get('form_id') or not data.get('form_data'):
            raise BadRequest("Missing form_id or form_data")
            
        form_id = data['form_id']
        form_data = data['form_data']
        
        # In a real app, this would be saved to a database
        submission = {
            "id": f"submission_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": current_user['id'],
            "form_id": form_id,
            "form_data": form_data,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat(),
            "documents": []
        }
        
        # Generate any necessary documents
        document_results = generate_document(form_id, form_data)
        submission['documents'] = document_results
        
        return jsonify({
            "success": True,
            "submission_id": submission['id'],
            "documents": document_results
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/track/<submission_id>', methods=['GET'])
@require_auth
def track_submission(submission_id):
    """Track status of an immigration form submission"""
    try:
        # In a real app, this would fetch from a database
        # Mocked response for demonstration
        submission_status = {
            "id": submission_id,
            "status": "processing",
            "submitted_at": "2023-11-10T14:30:00Z",
            "last_updated": "2023-11-11T09:15:00Z",
            "next_steps": [
                "Document review in progress",
                "Estimated completion: 5-7 business days"
            ],
            "notes": "Your application has been received and is being processed."
        }
        
        return jsonify(submission_status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 