from flask import Blueprint, request, jsonify, current_app
from models.database import db
from routes.auth import token_required
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json

load_dotenv()

bp = Blueprint('support', __name__)

def send_support_email(subject, message, user_email=None):
    """Send support email to admin and confirmation to user"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        admin_email = os.getenv('ADMIN_EMAIL')
        
        # Send to admin
        admin_msg = MIMEMultipart()
        admin_msg['From'] = smtp_username
        admin_msg['To'] = admin_email
        admin_msg['Subject'] = f'Support Request: {subject}'
        
        admin_body = f"""
        New Support Request
        
        From: {user_email if user_email else 'Anonymous'}
        Subject: {subject}
        
        Message:
        {message}
        
        Timestamp: {datetime.utcnow().isoformat()}
        """
        
        admin_msg.attach(MIMEText(admin_body, 'plain'))
        
        # Send confirmation to user if email provided
        if user_email:
            user_msg = MIMEMultipart()
            user_msg['From'] = smtp_username
            user_msg['To'] = user_email
            user_msg['Subject'] = 'Support Request Received'
            
            user_body = f"""
            Thank you for contacting SmartProBono support.
            
            We have received your request and will respond within 24-48 hours.
            
            Your request details:
            Subject: {subject}
            Message: {message}
            
            Best regards,
            SmartProBono Support Team
            """
            
            user_msg.attach(MIMEText(user_body, 'plain'))
        
        # Send emails
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        server.send_message(admin_msg)
        if user_email:
            server.send_message(user_msg)
            
        server.quit()
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error sending support email: {str(e)}")
        return False

@bp.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['subject', 'message']
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    try:
        # Store contact submission
        contact_data = {
            'subject': data['subject'],
            'message': data['message'],
            'email': data.get('email'),
            'name': data.get('name'),
            'phone': data.get('phone'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Save to file system for MVP
        filename = f"data/contact/contact_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('data/contact', exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(contact_data, f, indent=2)
        
        # Send email notifications
        if not send_support_email(
            data['subject'],
            data['message'],
            data.get('email')
        ):
            return jsonify({
                'warning': 'Request saved but email notification failed',
                'request': contact_data
            }), 201
        
        return jsonify({
            'message': 'Contact request submitted successfully',
            'request': contact_data
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error submitting contact form: {str(e)}")
        return jsonify({'error': 'Could not submit contact form'}), 500

@bp.route('/support', methods=['POST'])
@token_required
def submit_support_ticket(current_user):
    """Submit support ticket (for logged-in users)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['subject', 'message', 'priority']
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    if data['priority'] not in ['low', 'medium', 'high', 'urgent']:
        return jsonify({'error': 'Invalid priority level'}), 400
    
    try:
        # Store support ticket
        ticket_data = {
            'user_id': current_user.id,
            'user_email': current_user.email,
            'subject': data['subject'],
            'message': data['message'],
            'priority': data['priority'],
            'status': 'open',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Save to file system for MVP
        filename = f"data/support/ticket_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('data/support', exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(ticket_data, f, indent=2)
        
        # Send email notifications
        if not send_support_email(
            f"[{data['priority'].upper()}] {data['subject']}",
            data['message'],
            current_user.email
        ):
            return jsonify({
                'warning': 'Ticket saved but email notification failed',
                'ticket': ticket_data
            }), 201
        
        return jsonify({
            'message': 'Support ticket submitted successfully',
            'ticket': ticket_data
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error submitting support ticket: {str(e)}")
        return jsonify({'error': 'Could not submit support ticket'}), 500

@bp.route('/support/tickets', methods=['GET'])
@token_required
def get_user_tickets(current_user):
    """Get user's support tickets"""
    try:
        # For MVP, read from file system
        tickets = []
        if os.path.exists('data/support'):
            for filename in os.listdir('data/support'):
                if filename.endswith('.json'):
                    with open(f'data/support/{filename}', 'r') as f:
                        ticket = json.load(f)
                        if ticket.get('user_id') == current_user.id:
                            tickets.append(ticket)
        
        return jsonify({
            'tickets': sorted(tickets, key=lambda x: x['timestamp'], reverse=True)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting support tickets: {str(e)}")
        return jsonify({'error': 'Could not fetch support tickets'}), 500

@bp.route('/faq', methods=['GET'])
def get_faq():
    """Get FAQ items"""
    faqs = [
        {
            'question': 'What is SmartProBono?',
            'answer': 'SmartProBono is a platform that connects individuals needing legal assistance with pro bono attorneys.'
        },
        {
            'question': 'How do I get started?',
            'answer': 'Sign up for an account, verify your email, and complete your profile. Then you can start searching for attorneys or legal resources.'
        },
        {
            'question': 'Is this service free?',
            'answer': 'Yes, SmartProBono is free for clients seeking legal assistance. Attorneys volunteer their time pro bono.'
        },
        {
            'question': 'How are attorneys verified?',
            'answer': 'Attorneys must provide their bar number and undergo verification before being able to offer services.'
        },
        {
            'question': 'What types of legal issues can I get help with?',
            'answer': 'SmartProBono covers various areas including family law, housing, employment, immigration, and more.'
        }
    ]
    
    return jsonify({'faqs': faqs}) 