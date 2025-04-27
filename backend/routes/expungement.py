from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.user import User
import hashlib

expungement = Blueprint('expungement', __name__, url_prefix='/api/expungement')

# Mock expungement eligibility rules by state
# In a production app, this would be stored in a database
STATE_RULES = {
    'CA': {
        'name': 'California',
        'description': 'California allows for expungement of most misdemeanors and some felonies after completion of probation.',
        'requirements': [
            'Completed probation for the offense',
            'Not currently charged with another crime',
            'Not serving a sentence for another crime',
            'At least 1 year has passed since conviction for misdemeanors',
            'At least 3 years have passed since conviction for eligible felonies'
        ],
        'eligibility': {
            'misdemeanor': {
                'waiting_period': 1,  # years
                'ineligible_offenses': ['DUI', 'sex_crimes']
            },
            'felony': {
                'waiting_period': 3,  # years
                'ineligible_offenses': ['murder', 'sex_crimes', 'child_abuse']
            },
            'arrest': {
                'waiting_period': 0,  # years
                'ineligible_offenses': []  # All arrests can be expunged if not charged
            }
        },
        'forms': {
            'misdemeanor': 'CR-180',
            'felony': 'CR-180',
            'arrest': 'CR-180'
        }
    },
    'NY': {
        'name': 'New York',
        'description': 'New York allows for sealing of certain criminal records after a waiting period.',
        'requirements': [
            'No more than 2 misdemeanors or 1 felony conviction',
            'At least 10 years since last conviction',
            'Not convicted of a sex offense or violent felony',
            'No pending criminal charges'
        ],
        'eligibility': {
            'misdemeanor': {
                'waiting_period': 10,  # years
                'ineligible_offenses': ['sex_crimes', 'violent_felony']
            },
            'felony': {
                'waiting_period': 10,  # years
                'ineligible_offenses': ['sex_crimes', 'violent_felony', 'class_A_felony']
            },
            'arrest': {
                'waiting_period': 0,  # years
                'ineligible_offenses': []  # All arrests can be expunged if not charged
            }
        },
        'forms': {
            'misdemeanor': 'CPL 160.59',
            'felony': 'CPL 160.59',
            'arrest': 'CPL 160.59'
        }
    }
}

@expungement.route('/check-eligibility', methods=['POST'])
def check_eligibility():
    try:
        data = request.get_json()
        
        # Extract required data
        state = data.get('state')
        case_type = data.get('caseType')
        
        # Validate input
        if not state or not case_type:
            return jsonify({
                'eligible': False,
                'reason': 'Missing required information: state and case type are required'
            }), 400
            
        # Check if we have rules for this state
        if state not in STATE_RULES:
            return jsonify({
                'eligible': False,
                'reason': f'Expungement rules for {state} are not available yet'
            }), 404
            
        # Get state rules
        state_rule = STATE_RULES[state]
        
        # Check if the case type is supported
        if case_type not in state_rule['eligibility']:
            return jsonify({
                'eligible': False,
                'reason': f'Case type {case_type} is not supported for {state}'
            }), 400
            
        # For simplicity, we'll assume eligibility based on the case type
        # In a real application, you would need more detailed information
        
        # Return eligibility info
        return jsonify({
            'eligible': True,
            'state': state,
            'caseType': case_type,
            'requirements': state_rule['requirements'],
            'nextSteps': [
                f'Fill out form {state_rule["forms"][case_type]}',
                'Gather supporting documents',
                'File with the court'
            ]
        })
        
    except Exception as e:
        return jsonify({
            'eligible': False,
            'reason': f'An error occurred: {str(e)}'
        }), 500

@expungement.route('/rules/<state>', methods=['GET'])
def get_state_rules(state):
    try:
        # Check if we have rules for this state
        if state not in STATE_RULES:
            return jsonify({
                'error': f'Expungement rules for {state} are not available yet'
            }), 404
            
        # Return the rules
        return jsonify(STATE_RULES[state])
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@expungement.route('/start', methods=['POST'])
@jwt_required()
def start_expungement_process():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        required_fields = ['state', 'caseType', 'caseDetails']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
            
        # Create a new expungement case with a unique ID
        # In a real app, this would be stored in a database
        case_id = hashlib.md5(f"{user_id}_{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Create case object
        case = {
            'id': case_id,
            'user_id': user_id,
            'state': data['state'],
            'caseType': data['caseType'],
            'caseDetails': data['caseDetails'],
            'status': 'started',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # In a real app, you would save this to a database
        # For demo purposes, we'll just return the case
        
        return jsonify({
            'success': True,
            'case': case,
            'message': 'Expungement process started successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@expungement.route('/<case_id>/progress', methods=['PUT'])
@jwt_required()
def save_progress(case_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # In a real app, you would update the case in your database
        # For demo purposes, we'll just acknowledge the update
        
        return jsonify({
            'success': True,
            'case_id': case_id,
            'message': 'Progress saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@expungement.route('/documents/<state>/<case_type>', methods=['GET'])
def get_required_documents(state, case_type):
    try:
        # Check if we have rules for this state
        if state not in STATE_RULES:
            return jsonify({
                'error': f'Expungement rules for {state} are not available yet'
            }), 404
            
        # Check if the case type is supported
        if case_type not in STATE_RULES[state]['eligibility']:
            return jsonify({
                'error': f'Case type {case_type} is not supported for {state}'
            }), 400
            
        # Return the required documents
        # In a real app, this would be more detailed
        documents = [
            {
                'name': f"{STATE_RULES[state]['forms'][case_type]} - Petition for Dismissal",
                'description': 'The main form to request expungement',
                'required': True
            },
            {
                'name': 'Court Case Information',
                'description': 'Docket or case information from the court',
                'required': True
            },
            {
                'name': 'Proof of Identity',
                'description': 'Copy of your ID or driver\'s license',
                'required': True
            },
            {
                'name': 'Proof of Completion of Sentence',
                'description': 'Documents showing you completed all terms of your sentence',
                'required': True
            }
        ]
        
        return jsonify(documents)
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500 