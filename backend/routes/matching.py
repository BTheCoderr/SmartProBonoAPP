from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.database import db
from models.attorney_request import AttorneyRequest
from models.case import Case
from datetime import datetime
from routes.auth import token_required
import json

matching_bp = Blueprint('matching', __name__)

def calculate_match_score(client, attorney):
    """Calculate match score between client and attorney with enhanced criteria"""
    score = 0
    max_score = 100
    
    # Match based on legal issue type and practice areas (40 points max)
    if attorney.practice_areas and client.legal_issue_type:
        practice_areas = attorney.practice_areas.split(',')
        if client.legal_issue_type in practice_areas:
            score += 40  # Exact match
        else:
            # Check for related practice areas
            related_areas = {
                'Immigration': ['Family Law', 'Civil Rights'],
                'Family Law': ['Immigration', 'Civil Rights'],
                'Civil Rights': ['Employment Law', 'Criminal Law'],
                'Employment Law': ['Civil Rights', 'Business Law'],
                'Criminal Law': ['Civil Rights', 'Family Law'],
                'Business Law': ['Employment Law', 'Contract Law']
            }
            if client.legal_issue_type in related_areas:
                for related in related_areas[client.legal_issue_type]:
                    if related in practice_areas:
                        score += 20  # Partial match for related area
                        break
    
    # Match based on languages (20 points max)
    if attorney.languages and hasattr(client, 'preferred_language'):
        attorney_languages = set(attorney.languages.split(','))
        client_languages = set([client.preferred_language])
        if hasattr(client, 'languages'):
            client_languages.update(client.languages.split(','))
        
        # Calculate language match score
        common_languages = attorney_languages.intersection(client_languages)
        if common_languages:
            if client.preferred_language in common_languages:
                score += 20  # Full points if preferred language matches
            else:
                score += 15  # Partial points if other languages match
    
    # Match based on location (20 points max)
    if attorney.state and client.state:
        if attorney.state == client.state:
            score += 20  # Same state
        else:
            # Define regions for partial matching
            regions = {
                'West': ['CA', 'OR', 'WA', 'NV', 'AZ'],
                'Northeast': ['NY', 'NJ', 'CT', 'MA', 'RI'],
                'Southeast': ['FL', 'GA', 'SC', 'NC', 'AL'],
                'Midwest': ['IL', 'IN', 'OH', 'MI', 'WI']
            }
            # Check if in same region
            for region, states in regions.items():
                if attorney.state in states and client.state in states:
                    score += 10  # Same region
                    break
    
    # Match based on availability and workload (20 points max)
    if attorney.availability:
        try:
            availability = json.loads(attorney.availability)
            # Calculate weekly availability hours
            total_hours = sum(len(day['hours']) for day in availability if day.get('hours'))
            
            # Get current case load
            active_cases = Case.query.filter_by(
                lawyer_id=attorney.id,
                status='IN_PROGRESS'
            ).count()
            
            # Calculate availability score based on hours and case load
            availability_score = min(20, total_hours - (active_cases * 2))  # Reduce score for each active case
            score += max(0, availability_score)  # Don't go negative
            
            # Bonus points for immediate availability
            if total_hours > 10 and active_cases < 3:
                score += 5  # Bonus for high availability and low case load
                
        except Exception as e:
            current_app.logger.error(f"Error calculating availability score: {str(e)}")
    
    # Experience bonus (up to 10 bonus points)
    if hasattr(attorney, 'years_of_experience'):
        experience_bonus = min(10, attorney.years_of_experience)  # Cap at 10 points
        score = min(100, score + experience_bonus)  # Don't exceed 100
    
    return score

@matching_bp.route('/find-attorneys', methods=['POST'])
@token_required
def find_attorneys(current_user):
    """Find matching attorneys for a client with enhanced filtering"""
    if current_user.role != 'client':
        return jsonify({'error': 'Only clients can search for attorneys'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No search criteria provided'}), 400
    
    # Get base query for attorneys
    query = User.query.filter_by(role='attorney', is_verified=True)
    
    # Apply filters if provided
    if data.get('practice_area'):
        query = query.filter(User.practice_areas.like(f"%{data['practice_area']}%"))
    if data.get('language'):
        query = query.filter(User.languages.like(f"%{data['language']}%"))
    if data.get('state'):
        query = query.filter_by(state=data['state'])
    if data.get('min_experience'):
        query = query.filter(User.years_of_experience >= data['min_experience'])
    
    attorneys = query.all()
    
    # Calculate match scores with detailed information
    matches = []
    for attorney in attorneys:
        score = calculate_match_score(current_user, attorney)
        if score >= 50:  # Only include matches above 50%
            attorney_dict = attorney.to_dict()
            attorney_dict.update({
                'match_score': score,
                'matching_criteria': {
                    'practice_area_match': bool(attorney.practice_areas and 
                        current_user.legal_issue_type in attorney.practice_areas),
                    'language_match': bool(attorney.languages and 
                        current_user.preferred_language in attorney.languages.split(',')),
                    'location_match': attorney.state == current_user.state,
                    'availability': json.loads(attorney.availability) if attorney.availability else None,
                    'years_of_experience': attorney.years_of_experience
                },
                'active_cases': Case.query.filter_by(
                    lawyer_id=attorney.id,
                    status='IN_PROGRESS'
                ).count()
            })
            matches.append(attorney_dict)
    
    # Sort by match score and limit results
    matches.sort(key=lambda x: (x['match_score'], x['years_of_experience']), reverse=True)
    
    return jsonify({
        'matches': matches[:10],  # Top 10 matches
        'total_matches': len(matches),
        'search_criteria': data
    })

@matching_bp.route('/request-attorney/<attorney_id>', methods=['POST'])
@token_required
def request_attorney(current_user, attorney_id):
    """Request to connect with an attorney"""
    if current_user.role != 'client':
        return jsonify({'error': 'Only clients can request attorneys'}), 403
    
    attorney = User.query.get(attorney_id)
    if not attorney or attorney.role != 'attorney':
        return jsonify({'error': 'Attorney not found'}), 404
    
    # Check if request already exists
    existing_request = AttorneyRequest.query.filter_by(
        client_id=current_user.id,
        attorney_id=attorney_id,
        status='pending'
    ).first()
    
    if existing_request:
        return jsonify({'error': 'A pending request already exists'}), 400
    
    data = request.get_json() or {}
    
    try:
        # Create connection request
        attorney_request = AttorneyRequest(
            client_id=current_user.id,
            attorney_id=attorney_id,
            status='pending',
            message=data.get('message', ''),
            legal_issue_type=current_user.legal_issue_type,
            case_description=data.get('case_description', '')
        )
        
        db.session.add(attorney_request)
        db.session.commit()
        
        # TODO: Send notification to attorney
        
        return jsonify({
            'message': 'Connection request sent successfully',
            'request': attorney_request.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating connection request: {str(e)}")
        return jsonify({'error': 'Could not create connection request'}), 500

@matching_bp.route('/attorney/requests', methods=['GET'])
@token_required
def get_attorney_requests(current_user):
    """Get connection requests for an attorney"""
    if current_user.role != 'attorney':
        return jsonify({'error': 'Only attorneys can view requests'}), 403
    
    try:
        # Get all requests for this attorney
        requests = AttorneyRequest.query.filter_by(
            attorney_id=current_user.id
        ).order_by(AttorneyRequest.created_at.desc()).all()
        
        return jsonify({
            'requests': [request.to_dict() for request in requests]
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching attorney requests: {str(e)}")
        return jsonify({'error': 'Could not fetch requests'}), 500

@matching_bp.route('/attorney/respond/<request_id>', methods=['POST'])
@token_required
def respond_to_request(current_user, request_id):
    """Respond to a connection request"""
    if current_user.role != 'attorney':
        return jsonify({'error': 'Only attorneys can respond to requests'}), 403
    
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({'error': 'Action (accept/reject) is required'}), 400
    
    action = data['action']
    if action not in ['accept', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    
    try:
        # Get the request
        attorney_request = AttorneyRequest.query.get(request_id)
        if not attorney_request:
            return jsonify({'error': 'Request not found'}), 404
            
        # Verify this attorney is the recipient
        if attorney_request.attorney_id != current_user.id:
            return jsonify({'error': 'Not authorized to respond to this request'}), 403
            
        # Update request status
        attorney_request.status = 'accepted' if action == 'accept' else 'rejected'
        db.session.commit()
        
        # TODO: Send notification to client
        
        return jsonify({
            'message': f'Request {action}ed successfully',
            'request': attorney_request.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error responding to request: {str(e)}")
        return jsonify({'error': 'Could not update request'}), 500

@matching_bp.route('/client/requests', methods=['GET'])
@token_required
def get_client_requests(current_user):
    """Get connection requests made by a client"""
    if current_user.role != 'client':
        return jsonify({'error': 'Only clients can view their requests'}), 403
    
    try:
        # Get all requests made by this client
        requests = AttorneyRequest.query.filter_by(
            client_id=current_user.id
        ).order_by(AttorneyRequest.created_at.desc()).all()
        
        return jsonify({
            'requests': [request.to_dict() for request in requests]
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching client requests: {str(e)}")
        return jsonify({'error': 'Could not fetch requests'}), 500 