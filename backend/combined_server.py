#!/usr/bin/env python3
"""
Combined server with both contact form and document scanner functionality.
Now includes full CRM system integration.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables FIRST
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tempfile
from datetime import datetime
from simple_ai_service import analyze_document, extract_text_from_document, analyze_with_safety
from config import config
import asyncio
import threading

# Import CRM system components
from database import init_db
from register_crm_only import register_crm_blueprints

# Import WebSocket support
try:
    from websocket_server import start_websocket_server, send_notification, send_case_update
    WEBSOCKET_AVAILABLE = True
except ImportError:
    print("WebSocket support not available. Install with: pip install websockets")
    WEBSOCKET_AVAILABLE = False

app = Flask(__name__)

# Enable debug mode
app.config['DEBUG'] = True

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Ensure database URL is properly set
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartprobono_dev.db'

# Initialize database
init_db(app)

# Register CRM blueprints only
register_crm_blueprints(app)

# Register Analytics API routes
try:
    from routes.analytics_api import bp as analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api')
    print("✅ Analytics API routes registered")
except ImportError as e:
    print(f"⚠️ Analytics API routes not available: {e}")

# Register Document Collaboration API routes
try:
    from routes.document_collaboration_api import bp as doc_collab_bp
    app.register_blueprint(doc_collab_bp, url_prefix='/api')
    print("✅ Document Collaboration API routes registered")
except ImportError as e:
    print(f"⚠️ Document Collaboration API routes not available: {e}")

# Register Voice API routes
try:
    from routes.voice_api import voice_bp
    app.register_blueprint(voice_bp)  # Blueprint already has /api/voice prefix
    print("✅ Voice API routes registered")
except ImportError as e:
    print(f"⚠️ Voice API routes not available: {e}")

# Register Court Filing API routes
try:
    from routes.court_filing_api import court_filing_bp
    app.register_blueprint(court_filing_bp)  # Blueprint already has /api/court-filing prefix
    print("✅ Court Filing API routes registered")
except ImportError as e:
    print(f"⚠️ Court Filing API routes not available: {e}")

# Register Enhanced API v2 routes
try:
    from routes.enhanced_api import enhanced_api_bp
    app.register_blueprint(enhanced_api_bp)  # Blueprint already has /api/v2 prefix
    print("✅ Enhanced API v2 routes registered")
except ImportError as e:
    print(f"⚠️ Enhanced API v2 routes not available: {e}")

# Register Legal AI routes
try:
    from routes.legal_ai import bp as legal_ai_bp
    app.register_blueprint(legal_ai_bp, url_prefix='/api/v1/legal')
    print("✅ Legal AI routes registered")
except ImportError as e:
    print(f"⚠️ Legal AI routes not available: {e}")

# Register CourtListener routes
try:
    from routes.courtlistener_api import courtlistener_bp
    app.register_blueprint(courtlistener_bp, url_prefix='/api/courtlistener')
    print("✅ CourtListener API routes registered")
except ImportError as e:
    print(f"⚠️ CourtListener API routes not available: {e}")

# Register Multi-Agent routes
try:
    from routes.multi_agent_routes import bp as multi_agent_bp
    app.register_blueprint(multi_agent_bp)  # Blueprint already has /api/multi-agent prefix
    print("✅ Multi-Agent System routes registered (FREE models: Ollama + Gemini)")
except ImportError as e:
    print(f"⚠️ Multi-Agent routes not available: {e}")

# Register Orchestrated AI routes (Multi-model collaboration)
try:
    from routes.orchestrated_routes import bp as orchestrated_bp
    app.register_blueprint(orchestrated_bp)  # Blueprint already has /api/orchestrated prefix
    print("✅ Orchestrated AI routes registered (4-5 models per response)")
except ImportError as e:
    print(f"⚠️ Orchestrated AI routes not available: {e}")

# Initialize CORS with enhanced settings for development
CORS(app, 
     origins=app.config.get('CORS_ORIGINS', [
         'http://localhost:3000', 
         'http://localhost:3001', 
         'http://localhost:3002', 
         'http://127.0.0.1:3000', 
         'http://127.0.0.1:3001', 
         'http://127.0.0.1:3002',
         'https://smartprobono.org',
         'https://www.smartprobono.org',
         'null'  # Allow file:// protocol for testing
     ]),
     methods=app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
     allow_headers=app.config.get('CORS_ALLOW_HEADERS', ['Content-Type', 'Authorization', 'X-Requested-With']),
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
                'to': ['bferrell@smartprobono.org'],
                'subject': subject,
                'html': html_content
            },
            timeout=30  # Add timeout for security
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
        , timeout=30)
        
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
                'to': ['bferrell@smartprobono.org'],
                'subject': subject,
                'html': html_content
            }
        , timeout=30)
        
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
        , timeout=30)
        
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
                'to': ['bferrell@smartprobono.org'],
                'subject': subject,
                'html': html_content
            }
        , timeout=30)
        
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
        , timeout=30)
        
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
            'to': ['bferrell@smartprobono.org'],
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
        , timeout=30)

        if response.status_code == 200:
            print("✅ Contact form email sent successfully to bferrell@smartprobono.org")
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

@app.route('/api/onboarding', methods=['GET'])
def onboarding_data():
    """Get onboarding data for the frontend."""
    return jsonify({
        'success': True,
        'onboarding': {
            'steps': [
                {
                    'id': 1,
                    'title': 'Welcome to SmartProBono',
                    'description': 'Your AI-powered legal assistant is ready to help',
                    'icon': 'shield',
                    'completed': False
                },
                {
                    'id': 2,
                    'title': 'Choose Your Legal Need',
                    'description': 'Select from document analysis, generation, or legal chat',
                    'icon': 'document',
                    'completed': False
                },
                {
                    'id': 3,
                    'title': 'Get Started',
                    'description': 'Begin using our legal tools and AI assistance',
                    'icon': 'play',
                    'completed': False
                }
            ],
            'features': [
                'AI Legal Chat',
                'Document Scanner',
                'PDF Generator',
                'Court Filing Assistant',
                'CRM System'
            ],
            'welcome_message': 'Welcome to SmartProBono! We\'re here to make legal help accessible, affordable, and easy to understand for everyone.'
        }
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
            'safety': 'enabled',
            'websocket': 'available' if WEBSOCKET_AVAILABLE else 'unavailable'
        },
        'version': '2.0.0',
        'features': [
            'Document Analysis',
            'PDF Generation', 
            'Contact Form',
            'Safety & Compliance',
            'UPL Prevention',
            'Real-Time Features' if WEBSOCKET_AVAILABLE else 'Real-Time Features (Disabled)'
        ],
        'message': 'SmartProBono enhanced system is running'
    }), 200

# ===== WEBSOCKET INTEGRATION ENDPOINTS =====

@app.route('/api/notifications/send', methods=['POST'])
def send_notification_endpoint():
    """Send a notification via WebSocket"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({
            'error': 'WebSocket support not available',
            'success': False
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'type' not in data:
            return jsonify({
                'error': 'Missing required field: type',
                'success': False
            }), 400
        
        notification_type = data['type']
        notification_data = data.get('data', {})
        recipient_id = data.get('recipient_id')
        room_id = data.get('room_id')
        
        # Send notification asynchronously
        def send_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_notification(
                notification_type, 
                notification_data, 
                recipient_id, 
                room_id
            ))
            loop.close()
        
        thread = threading.Thread(target=send_async)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Notification sent',
            'type': notification_type
        }), 200
        
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return jsonify({
            'error': f'Failed to send notification: {str(e)}',
            'success': False
        }), 500

@app.route('/api/case-updates/send', methods=['POST'])
def send_case_update_endpoint():
    """Send a case update via WebSocket"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({
            'error': 'WebSocket support not available',
            'success': False
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'case_id' not in data:
            return jsonify({
                'error': 'Missing required field: case_id',
                'success': False
            }), 400
        
        case_id = data['case_id']
        update_data = data.get('update', {})
        user_id = data.get('user_id')
        
        # Send case update asynchronously
        def send_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_case_update(case_id, update_data, user_id))
            loop.close()
        
        thread = threading.Thread(target=send_async)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Case update sent',
            'case_id': case_id
        }), 200
        
    except Exception as e:
        print(f"Error sending case update: {str(e)}")
        return jsonify({
            'error': f'Failed to send case update: {str(e)}',
            'success': False
        }), 500

@app.route('/api/websocket/status', methods=['GET'])
def websocket_status():
    """Get WebSocket server status"""
    return jsonify({
        'websocket_available': WEBSOCKET_AVAILABLE,
        'websocket_url': 'ws://localhost:8765' if WEBSOCKET_AVAILABLE else None,
        'message': 'WebSocket server is running' if WEBSOCKET_AVAILABLE else 'WebSocket server not available'
    }), 200

if __name__ == '__main__':
    print("🚀 Starting SmartProBono Combined Server...")
    print("=" * 50)
    print("📧 Contact form ready - sending to bferrell@smartprobono.org")
    print("📄 Document scanner ready - analyzing PDFs with real text extraction")
    print("🐛 Bug reports: Connected to email")
    print("💡 Feature requests: Connected to email")
    print("=" * 50)
    print("🎯 CRM SYSTEM NOW CONNECTED!")
    print("👥 Client Portal: /api/v1/crm/client/*")
    print("⚖️ Lawyer Dashboard: /api/v1/crm/lawyer/*")
    print("💰 Bondsman Dashboard: /api/v1/crm/bondsman/*")
    print("📅 Court Dates: /api/v1/crm/court-dates")
    print("🔔 Notifications: /api/v1/crm/notifications")
    print("=" * 50)
    
    # Start WebSocket server if available
    if WEBSOCKET_AVAILABLE:
        print("🔌 REAL-TIME FEATURES ENABLED!")
        print("📡 WebSocket server: ws://localhost:8765")
        print("💬 Live chat: Available")
        print("🔔 Real-time notifications: Available")
        print("📄 Document collaboration: Available")
        
        # Start WebSocket server in a separate thread
        def start_websocket():
            asyncio.run(start_websocket_server())
        
        ws_thread = threading.Thread(target=start_websocket, daemon=True)
        ws_thread.start()
        print("✅ WebSocket server started in background")
    else:
        print("⚠️ WebSocket support not available - install with: pip install websockets")
    
    print("🎤 VOICE FEATURES ENABLED!")
    print("🗣️ Speech-to-text: /api/voice/speech-to-text")
    print("🔊 Text-to-speech: /api/voice/text-to-speech")
    print("🤖 Voice commands: /api/voice/command")
    print("📊 Voice analysis: /api/voice/analyze")
    print("📁 Audio upload: /api/voice/upload-audio")
    print("💾 Audio download: /api/voice/download-audio")
    
    print("⚖️ COURT FILING ASSISTANCE ENABLED!")
    print("📋 Court rules: /api/court-filing/rules")
    print("📄 Filing templates: /api/court-filing/templates")
    print("📝 Document generation: /api/court-filing/generate")
    print("📁 Create filing: /api/court-filing/filings")
    print("💰 Calculate fees: /api/court-filing/fees")
    print("⏰ Filing deadlines: /api/court-filing/deadlines")
    print("✅ Validate filing: /api/court-filing/validate")
    
    print("=" * 50)
    print("🌐 Server running on: http://localhost:3001")
    print("🔗 Test CRM: python test_crm_connection.py")
    print("🔗 Test WebSocket: ws://localhost:8765")
    app.run(host='127.0.0.1', port=3001, debug=True)  # Debug mode enabled
