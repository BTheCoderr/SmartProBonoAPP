#!/usr/bin/env python3
"""
Combined server with both contact form and document scanner functionality.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tempfile
from datetime import datetime
from simple_ai_service import analyze_document, extract_text_from_document, analyze_with_safety
from config import config

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize CORS with enhanced settings
CORS(app, 
     origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000', 'http://localhost:3002']),
     methods=app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
     allow_headers=app.config.get('CORS_ALLOW_HEADERS', ['Content-Type', 'Authorization']),
     expose_headers=app.config.get('CORS_EXPOSE_HEADERS', ['Content-Range', 'X-Total-Count']),
     supports_credentials=app.config.get('CORS_SUPPORTS_CREDENTIALS', True))

# Resend API configuration
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', 're_N7YNzBXp_HyNzVsWjuLNqxqUQr8oxaxvf')
RESEND_URL = 'https://api.resend.com/emails'

def send_contact_form_email(data):
    """Send contact form email using Resend API."""
    try:
        # Prepare email content
        subject = f"New Contact Form Submission - {data.get('firstName', '')} {data.get('lastName', '')}"
        
        # Create HTML content
        html_content = f"""
        <h2>New Contact Form Submission</h2>
        <p><strong>Name:</strong> {data.get('firstName', '')} {data.get('lastName', '')}</p>
        <p><strong>Email:</strong> {data.get('email', '')}</p>
        <p><strong>Phone:</strong> {data.get('phone', '')}</p>
        <p><strong>Case Type:</strong> {data.get('caseType', '')}</p>
        <p><strong>Urgency:</strong> {data.get('urgency', '')}</p>
        <p><strong>State:</strong> {data.get('state', '')}</p>
        <p><strong>City:</strong> {data.get('city', '')}</p>
        <p><strong>Zip Code:</strong> {data.get('zipCode', '')}</p>
        <p><strong>Contact Method:</strong> {data.get('contactMethod', '')}</p>
        <p><strong>Best Time:</strong> {data.get('bestTime', '')}</p>
        <p><strong>How did you hear about us:</strong> {data.get('hearAbout', '')}</p>
        <p><strong>Do you have an attorney:</strong> {data.get('hasAttorney', '')}</p>
        <p><strong>Case Value:</strong> {data.get('caseValue', '')}</p>
        <p><strong>Message:</strong></p>
        <p>{data.get('message', '')}</p>
        """
        
        # Send email using Resend
        response = requests.post(RESEND_URL, 
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <noreply@smartprobono.org>',
                'to': ['support@smartprobono.org'],
                'subject': subject,
                'html': html_content
            }
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending contact form email: {str(e)}")
        return False

def send_auto_reply(recipient_email, recipient_name):
    """Send auto-reply to contact form submitter."""
    try:
        subject = "Thank you for contacting SmartProBono"
        
        html_content = f"""
        <h2>Thank you for contacting SmartProBono!</h2>
        <p>Dear {recipient_name},</p>
        <p>We have received your message and will get back to you within 24 hours.</p>
        <p>In the meantime, feel free to explore our legal tools and resources.</p>
        <p>Best regards,<br>The SmartProBono Team</p>
        """
        
        response = requests.post(RESEND_URL,
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <noreply@smartprobono.org>',
                'to': [recipient_email],
                'subject': subject,
                'html': html_content
            }
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending auto-reply: {str(e)}")
        return False

def send_bug_report_email(data):
    """Send bug report email using Resend API."""
    try:
        print(f"🐛 DEBUG: send_bug_report_email called with data: {data}")
        subject = f"🐛 Bug Report: {data.get('title', '')}"
        
        html_content = f"""
        <h2>🐛 New Bug Report</h2>
        <p><strong>Title:</strong> {data.get('title', '')}</p>
        <p><strong>Severity:</strong> {data.get('severity', '').upper()}</p>
        <p><strong>Browser:</strong> {data.get('browser', 'Not specified')}</p>
        <p><strong>Device:</strong> {data.get('device', 'Not specified')}</p>
        <p><strong>Reporter Email:</strong> {data.get('email', 'Not provided')}</p>
        <p><strong>Can Contact:</strong> {'Yes' if data.get('canContact') else 'No'}</p>
        <p><strong>Timestamp:</strong> {data.get('timestamp', '')}</p>
        
        <h3>Description:</h3>
        <p>{data.get('description', '')}</p>
        
        <h3>Steps to Reproduce:</h3>
        <p>{data.get('steps', 'Not provided')}</p>
        
        <h3>Expected Behavior:</h3>
        <p>{data.get('expected', 'Not provided')}</p>
        
        <h3>Actual Behavior:</h3>
        <p>{data.get('actual', 'Not provided')}</p>
        """
        
        response = requests.post(RESEND_URL, 
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <onboarding@resend.dev>',
                'to': ['bferrell514@gmail.com'],
                'subject': subject,
                'html': html_content
            }
        )
        
        print(f"🐛 DEBUG: Resend response status: {response.status_code}")
        print(f"🐛 DEBUG: Resend response content: {response.text}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending bug report email: {str(e)}")
        return False

def send_bug_report_auto_reply(recipient_email, bug_title):
    """Send auto-reply to bug report submitter."""
    try:
        subject = "Thank you for reporting a bug - SmartProBono"
        
        html_content = f"""
        <h2>Thank you for reporting a bug!</h2>
        <p>We have received your bug report: <strong>{bug_title}</strong></p>
        <p>Our development team will investigate this issue and work on a fix.</p>
        <p>If you provided your email address, we'll notify you when the issue is resolved.</p>
        <p>Thank you for helping us improve SmartProBono!</p>
        <p>Best regards,<br>The SmartProBono Team</p>
        """
        
        response = requests.post(RESEND_URL,
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <onboarding@resend.dev>',
                'to': [recipient_email],
                'subject': subject,
                'html': html_content
            }
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending bug report auto-reply: {str(e)}")
        return False

def send_feature_request_email(data):
    """Send feature request email using Resend API."""
    try:
        subject = f"💡 Feature Request: {data.get('title', '')}"
        
        html_content = f"""
        <h2>💡 New Feature Request</h2>
        <p><strong>Title:</strong> {data.get('title', '')}</p>
        <p><strong>Category:</strong> {data.get('category', '')}</p>
        <p><strong>Priority:</strong> {data.get('priority', 'medium').upper()}</p>
        <p><strong>Requester Email:</strong> {data.get('email', 'Not provided')}</p>
        <p><strong>Timestamp:</strong> {data.get('timestamp', '')}</p>
        
        <h3>Description:</h3>
        <p>{data.get('description', '')}</p>
        """
        
        response = requests.post(RESEND_URL, 
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <onboarding@resend.dev>',
                'to': ['bferrell514@gmail.com'],
                'subject': subject,
                'html': html_content
            }
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending feature request email: {str(e)}")
        return False

def send_feature_request_auto_reply(recipient_email, feature_title):
    """Send auto-reply to feature request submitter."""
    try:
        subject = "Thank you for your feature request - SmartProBono"
        
        html_content = f"""
        <h2>Thank you for your feature request!</h2>
        <p>We have received your feature request: <strong>{feature_title}</strong></p>
        <p>Our product team will review your suggestion and consider it for future updates.</p>
        <p>If you provided your email address, we'll notify you if this feature is implemented.</p>
        <p>Thank you for helping us improve SmartProBono!</p>
        <p>Best regards,<br>The SmartProBono Team</p>
        """
        
        response = requests.post(RESEND_URL,
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': 'SmartProBono <onboarding@resend.dev>',
                'to': [recipient_email],
                'subject': subject,
                'html': html_content
            }
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending feature request auto-reply: {str(e)}")
        return False

@app.route('/api/contact/submit', methods=['POST'])
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

        # Send contact form email via Resend
        payload = {
            'from': 'SmartProBono <onboarding@resend.dev>',
            'to': ['bferrell514@gmail.com'],
            'subject': f'New Contact Form Submission from {data["firstName"]} {data["lastName"]}',
            'html': f'''
            <h2>New Contact Form Submission</h2>
            <h3>Basic Information</h3>
            <p><strong>Name:</strong> {data["firstName"]} {data["lastName"]}</p>
            <p><strong>Email:</strong> {data["email"]}</p>
            <p><strong>Phone:</strong> {data.get("phone", "N/A")}</p>
            
            <h3>Legal Case Information</h3>
            <p><strong>Case Type:</strong> {data.get("caseType", "N/A")}</p>
            <p><strong>Urgency Level:</strong> {data.get("urgency", "N/A")}</p>
            <p><strong>Case Value:</strong> {data.get("caseValue", "N/A")}</p>
            <p><strong>Has Attorney:</strong> {data.get("hasAttorney", "N/A")}</p>
            
            <h3>Location Information</h3>
            <p><strong>State:</strong> {data.get("state", "N/A")}</p>
            <p><strong>City:</strong> {data.get("city", "N/A")}</p>
            <p><strong>Zip Code:</strong> {data.get("zipCode", "N/A")}</p>
            
            <h3>Contact Preferences</h3>
            <p><strong>Preferred Method:</strong> {data.get("contactMethod", "N/A")}</p>
            <p><strong>Best Time:</strong> {data.get("bestTime", "N/A")}</p>
            <p><strong>How did you hear about us:</strong> {data.get("hearAbout", "N/A")}</p>
            
            <h3>Message</h3>
            <p>{data["message"]}</p>
            ''',
            'text': f'''
            New contact form submission:
            Name: {data["firstName"]} {data["lastName"]}
            Email: {data["email"]}
            Phone: {data.get("phone", "N/A")}
            Case Type: {data.get("caseType", "N/A")}
            Urgency: {data.get("urgency", "N/A")}
            State: {data.get("state", "N/A")}
            Message: {data["message"]}
            '''
        }

        response = requests.post(
            RESEND_URL,
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload
        )

        if response.status_code == 200:
            print("✅ Contact form email sent successfully to bferrell514@gmail.com")
            return jsonify({
                'success': True,
                'message': 'Contact form submitted successfully. We will get back to you within 24 hours.'
            }), 200
        else:
            print(f"❌ Resend API error: {response.status_code} - {response.text}")
            return jsonify({
                'success': False,
                'error': 'Failed to send contact form. Please try again later.'
            }), 500

    except Exception as e:
        print(f"❌ Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500

@app.route('/api/contact/health', methods=['GET'])
def contact_health_check():
    """Health check endpoint for contact service."""
    return jsonify({
        'status': 'healthy',
        'service': 'contact',
        'message': 'Contact service is running'
    }), 200

@app.route('/api/bug-report/submit', methods=['POST'])
def submit_bug_report():
    """Handle bug report submission."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'severity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare email data for bug report
        email_data = {
            'type': 'bug_report',
            'title': data.get('title'),
            'description': data.get('description'),
            'steps': data.get('steps', ''),
            'expected': data.get('expected', ''),
            'actual': data.get('actual', ''),
            'severity': data.get('severity'),
            'browser': data.get('browser', ''),
            'device': data.get('device', ''),
            'email': data.get('email', ''),
            'canContact': data.get('canContact', False),
            'timestamp': datetime.now().isoformat()
        }
        
        # Send bug report email
        print(f"🐛 Attempting to send bug report email for: {email_data.get('title')}")
        success = send_bug_report_email(email_data)
        print(f"🐛 Bug report email result: {success}")
        
        if success:
            # Send auto-reply to the user if email provided
            if data.get('email'):
                send_bug_report_auto_reply(data.get('email'), data.get('title'))
            
            return jsonify({
                'success': True,
                'message': 'Bug report submitted successfully. We will investigate and get back to you soon.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to submit bug report. Please try again later.'
            }), 500
            
    except Exception as e:
        print(f"Error processing bug report: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500

@app.route('/api/feature-request/submit', methods=['POST'])
def submit_feature_request():
    """Handle feature request submission."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare email data for feature request
        email_data = {
            'type': 'feature_request',
            'title': data.get('title'),
            'description': data.get('description'),
            'category': data.get('category'),
            'priority': data.get('priority', 'medium'),
            'email': data.get('email', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # Send feature request email
        print(f"💡 Attempting to send feature request email for: {email_data.get('title')}")
        success = send_feature_request_email(email_data)
        print(f"💡 Feature request email result: {success}")
        
        if success:
            # Send auto-reply to the user if email provided
            if data.get('email'):
                send_feature_request_auto_reply(data.get('email'), data.get('title'))
            
            return jsonify({
                'success': True,
                'message': 'Feature request submitted successfully. Thank you for your suggestion!'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to submit feature request. Please try again later.'
            }), 500
            
    except Exception as e:
        print(f"Error processing feature request: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500

@app.route('/api/scanner/analyze', methods=['POST'])
def analyze_document_route():
    """Analyze a document for legal information"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Get the document type if specified
        document_type = request.form.get('document_type', 'generic')
        
        # Check file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'docx'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'File type not allowed'}), 400
            
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        file.save(temp_file_path)
        
        try:
            # Analyze the document
            analysis = analyze_document(temp_file_path, document_type)
            
            # Remove the temporary file
            os.remove(temp_file_path)
            
            # Return the analysis
            return jsonify({
                "success": True,
                "analysis": analysis,
                "document_type": document_type
            })
        except Exception as e:
            # Clean up file on error
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise e
            
    except Exception as e:
        print(f"❌ Error analyzing document: {str(e)}")
        return jsonify({'error': f'An error occurred while analyzing the document: {str(e)}'}), 500

@app.route('/api/scanner/health', methods=['GET'])
def scanner_health_check():
    """Health check endpoint for scanner service."""
    return jsonify({
        'status': 'healthy',
        'service': 'scanner',
        'message': 'Document scanner service is running'
    }), 200

@app.route('/api/generator/create', methods=['POST'])
def generate_document():
    """Generate a PDF document based on user input"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['document_type', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate PDF using the simple AI service
        from simple_ai_service import generate_pdf_document
        
        pdf_data = generate_pdf_document(
            document_type=data['document_type'],
            content=data['content'],
            title=data.get('title', 'Generated Document'),
            parties=data.get('parties', []),
            additional_info=data.get('additional_info', {})
        )
        
        if pdf_data:
            return jsonify({
                'success': True,
                'pdf_data': pdf_data,
                'message': 'Document generated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate document'
            }), 500
            
    except Exception as e:
        print(f"❌ Error generating document: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred while generating the document: {str(e)}'
        }), 500

@app.route('/api/generator/templates', methods=['GET'])
def get_document_templates():
    """Get available document templates"""
    templates = [
        {
            'id': 'lease_agreement',
            'name': 'Lease Agreement',
            'description': 'Residential rental agreement template',
            'fields': ['landlord_name', 'tenant_name', 'property_address', 'rent_amount', 'lease_term']
        },
        {
            'id': 'service_contract',
            'name': 'Service Contract',
            'description': 'Professional service agreement template',
            'fields': ['service_provider', 'client_name', 'service_description', 'payment_terms', 'duration']
        },
        {
            'id': 'nda',
            'name': 'Non-Disclosure Agreement',
            'description': 'Confidentiality agreement template',
            'fields': ['disclosing_party', 'receiving_party', 'confidential_info', 'duration', 'purpose']
        },
        {
            'id': 'employment_contract',
            'name': 'Employment Contract',
            'description': 'Employee agreement template',
            'fields': ['employer', 'employee_name', 'position', 'salary', 'start_date', 'benefits']
        }
    ]
    
    return jsonify({
        'success': True,
        'templates': templates
    }), 200

@app.route('/api/generator/health', methods=['GET'])
def generator_health_check():
    """Health check endpoint for generator service."""
    return jsonify({
        'status': 'healthy',
        'service': 'generator',
        'message': 'Document generator service is running'
    }), 200

@app.route('/api/scanner/analyze-safe', methods=['POST'])
def analyze_document_safe():
    """Enhanced document analysis with safety and compliance features"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get document type from form data
        document_type = request.form.get('document_type', 'generic')
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Extract text from document
            text = extract_text_from_document(temp_path)
            if not text:
                return jsonify({'error': 'Could not extract text from document'}), 400
            
            # Analyze with safety features
            analysis = analyze_with_safety(text, document_type)
            
            # Add metadata
            analysis['file_name'] = file.filename
            analysis['file_size'] = len(file.read())
            file.seek(0)  # Reset file pointer
            analysis['analysis_timestamp'] = datetime.now().isoformat()
            analysis['safety_checked'] = True
            
            return jsonify({
                'success': True,
                'analysis': analysis,
                'message': 'Document analyzed with safety features'
            }), 200
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"❌ Error in safe document analysis: {str(e)}")
        return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check for all services"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'scanner': 'running',
            'generator': 'running',
            'contact': 'running',
            'safety': 'enabled'
        },
        'version': '2.0.0',
        'features': [
            'Document Analysis',
            'PDF Generation', 
            'Contact Form',
            'Safety & Compliance',
            'UPL Prevention'
        ],
        'message': 'SmartProBono enhanced system is running'
    }), 200

if __name__ == '__main__':
    print("🚀 Starting combined server...")
    print("📧 Contact form ready - sending to bferrell514@gmail.com")
    print("📄 Document scanner ready - analyzing PDFs with real text extraction")
    print("🐛 Bug reports: Connected to email")
    print("💡 Feature requests: Connected to email")
    app.run(host='0.0.0.0', port=3001, debug=True)
