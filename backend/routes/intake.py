from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import json
from datetime import datetime
import logging
from backend.services.auth_service import require_auth, get_current_user
from backend.services.ai_service import analyze_case, generate_case_summary

bp = Blueprint('intake', __name__)
logger = logging.getLogger(__name__)

@bp.route('/submit', methods=['POST'])
def submit_intake():
    """Submit initial legal intake information"""
    try:
        data = request.json
        if not data:
            raise BadRequest("Missing intake data")
            
        # Validate required fields
        required_fields = ['full_name', 'contact_info', 'legal_issue_type', 'description']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f"Missing required field: {field}")
        
        # Process intake submission
        # In a real app, this would be saved to a database
        intake_id = f"intake_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Optional user association
        user_id = None
        try:
            user = get_current_user()
            if user:
                user_id = user.get('id')
        except:
            # User not authenticated - still allow intake as guest
            pass
        
        # Store intake data
        intake_data = {
            "id": intake_id,
            "user_id": user_id,
            "full_name": data['full_name'],
            "contact_info": data['contact_info'],
            "legal_issue_type": data['legal_issue_type'],
            "description": data['description'],
            "additional_info": data.get('additional_info', {}),
            "status": "submitted",
            "submitted_at": datetime.now().isoformat()
        }
        
        # AI analysis for initial assessment and routing
        try:
            assessment = analyze_case(data)
            intake_data['assessment'] = assessment
        except Exception as e:
            logger.error(f"Error during case analysis: {str(e)}")
            # Continue with intake even if AI analysis fails
            intake_data['assessment'] = {
                "error": "Analysis unavailable", 
                "priority": "medium"
            }
        
        # Generate case reference number
        case_reference = f"CASE-{datetime.now().strftime('%Y%m%d')}-{intake_id[-6:]}"
        
        return jsonify({
            "success": True,
            "intake_id": intake_id,
            "case_reference": case_reference,
            "message": "Your intake form has been submitted successfully.",
            "next_steps": [
                "A legal aid representative will review your case within 1-2 business days.",
                "You will receive an email confirmation with your case details."
            ]
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in intake submission: {str(e)}")
        return jsonify({"error": "An error occurred while processing your intake. Please try again."}), 500

@bp.route('/status/<intake_id>', methods=['GET'])
def check_intake_status(intake_id):
    """Check status of an intake submission"""
    try:
        # In a real app, this would fetch from a database
        # Mocked response for demonstration
        intake_status = {
            "id": intake_id,
            "status": "under_review",
            "submitted_at": "2023-11-10T14:30:00Z",
            "last_updated": "2023-11-11T09:15:00Z",
            "next_steps": [
                "Case evaluation in progress",
                "Estimated assignment: 1-2 business days"
            ],
            "notes": "Your case is being reviewed by our legal team."
        }
        
        return jsonify(intake_status)
    except Exception as e:
        logger.error(f"Error checking intake status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/legal-issue-types', methods=['GET'])
def get_legal_issue_types():
    """Get list of legal issue types for intake form"""
    try:
        issue_types = [
            {
                "id": "housing",
                "name": "Housing & Eviction",
                "description": "Issues related to housing, eviction, landlord disputes, or tenant rights"
            },
            {
                "id": "family",
                "name": "Family Law",
                "description": "Issues related to divorce, child custody, domestic violence, or family matters"
            },
            {
                "id": "immigration",
                "name": "Immigration",
                "description": "Issues related to immigration status, visas, citizenship, or deportation"
            },
            {
                "id": "employment",
                "name": "Employment",
                "description": "Issues related to employment, workplace discrimination, wages, or benefits"
            },
            {
                "id": "consumer",
                "name": "Consumer Rights",
                "description": "Issues related to debt collection, bankruptcy, or consumer protection"
            },
            {
                "id": "criminal",
                "name": "Criminal Record",
                "description": "Issues related to expungement, record sealing, or criminal justice"
            },
            {
                "id": "benefits",
                "name": "Public Benefits",
                "description": "Issues related to public benefits, disability, or healthcare access"
            },
            {
                "id": "other",
                "name": "Other",
                "description": "Other legal issues not listed above"
            }
        ]
        
        return jsonify({"issue_types": issue_types})
    except Exception as e:
        logger.error(f"Error getting legal issue types: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/additional-questions/<issue_type>', methods=['GET'])
def get_additional_questions(issue_type):
    """Get additional intake questions for a specific legal issue type"""
    try:
        # Map of issue types to additional questions
        questions_map = {
            "housing": [
                {
                    "id": "housing_situation",
                    "type": "select",
                    "label": "What is your current housing situation?",
                    "options": ["Renting", "Own home", "Public housing", "Staying with family/friends", "Homeless", "Other"],
                    "required": True
                },
                {
                    "id": "eviction_notice",
                    "type": "radio",
                    "label": "Have you received an eviction notice?",
                    "options": ["Yes", "No"],
                    "required": True
                },
                {
                    "id": "eviction_date",
                    "type": "date",
                    "label": "If yes, what is the eviction date?",
                    "required": False,
                    "dependent_on": {
                        "field": "eviction_notice",
                        "value": "Yes"
                    }
                }
            ],
            "immigration": [
                {
                    "id": "immigration_status",
                    "type": "select",
                    "label": "What is your current immigration status?",
                    "options": ["U.S. Citizen", "Permanent Resident", "Visa Holder", "Refugee/Asylee", "Undocumented", "Other"],
                    "required": True
                },
                {
                    "id": "immigration_issue",
                    "type": "multiselect",
                    "label": "What immigration issues are you facing?",
                    "options": ["Visa Application", "Green Card", "Citizenship", "Deportation/Removal", "Family Petition", "Asylum", "Other"],
                    "required": True
                }
            ],
            "family": [
                {
                    "id": "family_issue",
                    "type": "select",
                    "label": "What family law issue are you dealing with?",
                    "options": ["Divorce", "Child Custody", "Child Support", "Domestic Violence", "Restraining Order", "Other"],
                    "required": True
                },
                {
                    "id": "children_involved",
                    "type": "radio",
                    "label": "Are children involved in this case?",
                    "options": ["Yes", "No"],
                    "required": True
                }
            ],
            "criminal": [
                {
                    "id": "record_type",
                    "type": "select",
                    "label": "What type of record issue are you dealing with?",
                    "options": ["Expungement", "Record Sealing", "Arrest without Conviction", "Pardon", "Other"],
                    "required": True
                },
                {
                    "id": "conviction_date",
                    "type": "date",
                    "label": "Date of conviction (if applicable)",
                    "required": False
                },
                {
                    "id": "completed_sentence",
                    "type": "radio",
                    "label": "Have you completed your sentence?",
                    "options": ["Yes", "No", "Not applicable"],
                    "required": True
                }
            ]
        }
        
        # Default questions for any issue type
        default_questions = [
            {
                "id": "urgency",
                "type": "select",
                "label": "How urgent is your situation?",
                "options": ["Emergency - Within 24 hours", "Urgent - Within a week", "Important - Within a month", "Not time sensitive"],
                "required": True
            },
            {
                "id": "income",
                "type": "select",
                "label": "What is your annual household income range?",
                "options": ["Under $15,000", "$15,000 - $30,000", "$30,000 - $50,000", "$50,000 - $75,000", "Over $75,000", "Prefer not to say"],
                "required": False
            }
        ]
        
        # Get questions for the specific issue type or default to empty list
        type_specific_questions = questions_map.get(issue_type, [])
        
        # Combine default and type-specific questions
        all_questions = type_specific_questions + default_questions
        
        return jsonify({"questions": all_questions})
    except Exception as e:
        logger.error(f"Error getting additional questions: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/admin/list', methods=['GET'])
@require_auth
def admin_list_intakes():
    """Admin endpoint to list intake submissions"""
    try:
        # In a real app, this would fetch from a database with proper authorization
        # Mocked response for demonstration
        intakes = [
            {
                "id": "intake_20231110143045",
                "case_reference": "CASE-20231110-143045",
                "full_name": "John Smith",
                "legal_issue_type": "housing",
                "status": "assigned",
                "submitted_at": "2023-11-10T14:30:45Z",
                "priority": "high",
                "assigned_to": "lawyer123"
            },
            {
                "id": "intake_20231109102030",
                "case_reference": "CASE-20231109-102030",
                "full_name": "Maria Rodriguez",
                "legal_issue_type": "immigration",
                "status": "under_review",
                "submitted_at": "2023-11-09T10:20:30Z",
                "priority": "medium",
                "assigned_to": null
            }
        ]
        
        return jsonify({"intakes": intakes})
    except Exception as e:
        logger.error(f"Error listing intakes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/admin/assign', methods=['POST'])
@require_auth
def admin_assign_intake():
    """Admin endpoint to assign an intake to a lawyer"""
    try:
        data = request.json
        if not data or not data.get('intake_id') or not data.get('lawyer_id'):
            raise BadRequest("Missing intake_id or lawyer_id")
            
        intake_id = data['intake_id']
        lawyer_id = data['lawyer_id']
        notes = data.get('notes', '')
        
        # In a real app, this would update the database
        # Mocked response for demonstration
        
        return jsonify({
            "success": True,
            "intake_id": intake_id,
            "lawyer_id": lawyer_id,
            "status": "assigned",
            "assigned_at": datetime.now().isoformat(),
            "message": "Case assigned successfully"
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error assigning intake: {str(e)}")
        return jsonify({"error": str(e)}), 500 