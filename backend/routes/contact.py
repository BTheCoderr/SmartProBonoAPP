"""
Contact form routes for handling contact form submissions.
"""
from flask import Blueprint, request, jsonify
from services.resend_email_service import resend_email_service
import logging

logger = logging.getLogger(__name__)

contact_bp = Blueprint('contact', __name__, url_prefix='/api/contact')

@contact_bp.route('/submit', methods=['POST'])
def submit_contact_form():
    """Handle contact form submission."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Send contact form email
        success = resend_email_service.send_contact_form_email(data)
        
        if success:
            # Send auto-reply to the user
            recipient_name = f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
            resend_email_service.send_auto_reply(data.get('email'), recipient_name)
            
            return jsonify({
                'success': True,
                'message': 'Contact form submitted successfully. We will get back to you within 24 hours.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send contact form. Please try again later.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500

@contact_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for contact service."""
    return jsonify({
        'status': 'healthy',
        'service': 'contact',
        'message': 'Contact service is running'
    }), 200
