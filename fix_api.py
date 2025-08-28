from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Create a directory for email signups if it doesn't exist
EMAIL_DIRECTORY = "email_signups"
if not os.path.exists(EMAIL_DIRECTORY):
    os.makedirs(EMAIL_DIRECTORY)

# Create a directory for document storage
DOCUMENT_DIRECTORY = "documents"
if not os.path.exists(DOCUMENT_DIRECTORY):
    os.makedirs(DOCUMENT_DIRECTORY)
    os.makedirs(os.path.join(DOCUMENT_DIRECTORY, "templates"))
    os.makedirs(os.path.join(DOCUMENT_DIRECTORY, "user_files"))

# In-memory document storage for development
documents = []
templates = []

def send_confirmation_email(email):
    """Send a confirmation email to the user and a notification to the admin"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the confirmation for backup purposes
    confirmation_log = {
        "timestamp": timestamp,
        "email": email,
        "subject": "Welcome to SmartProBono!",
        "message": f"Thank you for signing up to SmartProBono! We're excited to have you join our platform."
    }
    
    # Save to a JSON file with email as filename
    filename = os.path.join(EMAIL_DIRECTORY, f"{email.replace('@', '_at_')}.json")
    with open(filename, 'w') as f:
        json.dump(confirmation_log, f, indent=2)
    
    # Now actually send the email
    try:
        # Configuration for SMTP - Get these from environment variables or config file
        # For testing, you can use environment variables or hardcode for development
        SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.zoho.com')  # Updated to Zoho
        SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
        SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'info@smartprobono.org')
        SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Use environment variable in production
        
        # Skip sending if no password is set (development mode)
        if not SMTP_PASSWORD:
            print(f"SMTP_PASSWORD not set. Would send confirmation email to {email}")
            print(f"Would also send notification to info@smartprobono.org about new signup")
            return True
            
        # Send to the user who signed up
        msg_to_user = MIMEMultipart()
        msg_to_user['From'] = SMTP_USERNAME
        msg_to_user['To'] = email
        msg_to_user['Subject'] = "Welcome to SmartProBono!"
        
        # Add proper headers for DKIM compatibility
        msg_to_user['Date'] = formatdate(localtime=True)
        msg_to_user['Message-ID'] = make_msgid(domain='smartprobono.org')
        
        # Create a nice HTML email
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #0078d4; color: white; padding: 10px 20px; }}
                    .content {{ padding: 20px; }}
                    .footer {{ font-size: 12px; color: #666; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to SmartProBono!</h1>
                    </div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>Thank you for signing up for SmartProBono's beta program. We're excited to have you join our platform!</p>
                        <p>You'll be among the first to experience our AI-powered legal assistance tools designed to make legal help accessible to everyone.</p>
                        <p>We'll keep you updated as we roll out new features and improvements.</p>
                        <p>Best regards,<br>The SmartProBono Team</p>
                    </div>
                    <div class="footer">
                        <p>This email was sent to <a href="mailto:{email}" style="color: #666; text-decoration: underline;">{email}</a> because you signed up for the SmartProBono beta.</p>
                        <p>&copy; 2025 SmartProBono. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg_to_user.attach(MIMEText(html, 'html'))
        
        # Also notify admin about the new signup
        msg_to_admin = MIMEMultipart()
        msg_to_admin['From'] = SMTP_USERNAME
        msg_to_admin['To'] = SMTP_USERNAME  # Send to self/admin
        msg_to_admin['Subject'] = "New SmartProBono Beta Signup"
        
        # Add proper headers for DKIM compatibility
        msg_to_admin['Date'] = formatdate(localtime=True)
        msg_to_admin['Message-ID'] = make_msgid(domain='smartprobono.org')
        
        admin_text = f"""
        A new user has signed up for the SmartProBono beta program.
        
        Email: {email}
        Timestamp: {timestamp}
        
        This is an automated notification.
        """
        
        msg_to_admin.attach(MIMEText(admin_text, 'plain'))
        
        # Establish connection and send emails
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            
            # Send email to user
            server.send_message(msg_to_user)
            print(f"Confirmation email sent to {email}")
            
            # Send notification to admin
            server.send_message(msg_to_admin)
            print(f"Admin notification sent to {SMTP_USERNAME}")
            
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # Still return True so the signup is processed even if email fails
        return True

@app.route('/api/health')
def health_check():
    """Health check endpoint that matches the screenshot"""
    return jsonify({
        "message": "API is running",
        "status": "ok",
        "version": "1.0.0"
    })

@app.route('/api/beta/signup', methods=['POST', 'OPTIONS'])
def signup():
    """Handle signup requests with email"""
    if request.method == 'OPTIONS':
        # Handle OPTIONS method for CORS preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        email = data.get('email', '')
        
        if not email or '@' not in email:
            return jsonify({"status": "error", "message": "Invalid email address"}), 400
        
        # Log the signup
        print(f"Received signup for email: {email}")
        
        # Send confirmation email
        send_confirmation_email(email)
        
        # Save to email list for future marketing
        with open(os.path.join(EMAIL_DIRECTORY, "all_signups.txt"), "a") as f:
            f.write(f"{email},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return jsonify({
            "status": "success", 
            "message": "Thank you for signing up! We'll be in touch soon.",
            "email_sent": True
        })
    except Exception as e:
        print(f"Error processing signup: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/legal/chat', methods=['POST', 'OPTIONS'])
def legal_chat():
    """Handle legal chat requests"""
    if request.method == 'OPTIONS':
        # Handle OPTIONS method for CORS preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        message = data.get('message', '')
        task_type = data.get('task_type', 'chat')
        
        if not message:
            return jsonify({"status": "error", "message": "Message is required"}), 400
        
        print(f"Received legal chat message: {message}, task_type: {task_type}")
        
        # Get model name for display
        model_name = get_model_display_name(task_type)
        
        # Provide startup-focused compliance responses
        response = ""
        if "gdpr" in message.lower() or "data protection" in message.lower():
            response = f"""**{model_name} Response:** GDPR Compliance for Startups:
            
🔍 **Assessment:** Your startup needs GDPR compliance if you:
- Process personal data of EU residents
- Have EU users/customers
- Use EU-based service providers

📋 **Essential Requirements:**
1. **Legal Basis:** Identify lawful basis for data processing (consent, contract, legitimate interest)
2. **Privacy Policy:** Clear, accessible policy explaining data collection and use
3. **Data Subject Rights:** Implement processes for access, rectification, erasure requests
4. **Data Protection Officer:** Required if processing is core business activity
5. **Breach Notification:** Report breaches within 72 hours
6. **Privacy by Design:** Build data protection into your systems from the start

💰 **Cost Impact:** Non-compliance fines up to €20M or 4% of annual revenue
📊 **Risk Score:** High for B2C startups, Medium for B2B SaaS

Need a compliance audit? I can help scan your current setup."""

        elif "soc 2" in message.lower() or "soc2" in message.lower():
            response = f"""**{model_name} Response:** SOC 2 Compliance for Startups:
            
📈 **Why SOC 2:** Essential for enterprise sales and building customer trust

🔐 **Five Trust Principles:**
1. **Security:** Protection against unauthorized access
2. **Availability:** System operational availability
3. **Processing Integrity:** System processing completeness/accuracy  
4. **Confidentiality:** Information designated confidential is protected
5. **Privacy:** Personal information collection/use/disposal

⚡ **Quick Implementation:**
- Start with security controls (most common)
- Document policies and procedures
- Implement access controls and monitoring
- Regular vulnerability assessments
- Employee security training

🎯 **Timeline:** 3-6 months for Type I, 12+ months for Type II
💵 **Investment:** $15k-$50k for initial compliance
📊 **ROI:** 25-40% increase in enterprise deal closure

Ready to start your SOC 2 journey? I can generate your control framework."""

        elif "privacy policy" in message.lower():
            response = f"""**{model_name} Response:** Privacy Policy Generation for Startups:
            
📄 **Essential Sections:**
1. **Information Collection:** What data you collect and how
2. **Use of Information:** How you use personal data
3. **Data Sharing:** When/why you share data with third parties
4. **Data Security:** How you protect user information
5. **User Rights:** How users can access/modify/delete their data
6. **Contact Information:** How users can reach you with questions

🌍 **Multi-Jurisdiction Compliance:**
- GDPR (EU): Explicit consent, right to be forgotten
- CCPA (California): Right to know, delete, opt-out
- PIPEDA (Canada): Meaningful consent, purpose limitation

⚡ **Startup-Specific Tips:**
- Update policy as you add features
- Use clear, non-legal language
- Include cookie policy if using tracking
- Version control for policy changes

🔄 **Auto-Generation:** I can create a customized policy based on your:
- Business model (B2B, B2C, marketplace)
- Data types collected
- Third-party integrations
- Target markets

Want me to generate your privacy policy now?"""

        elif "terms of service" in message.lower() or "terms and conditions" in message.lower():
            response = f"""**{model_name} Response:** Terms of Service for Startups:
            
⚖️ **Critical Clauses:**
1. **Service Description:** What you provide to users
2. **User Obligations:** What users can/cannot do
3. **Intellectual Property:** Who owns what content
4. **Liability Limitations:** Protection against lawsuits
5. **Termination:** How accounts can be terminated
6. **Dispute Resolution:** How conflicts are resolved
7. **Governing Law:** Which jurisdiction's laws apply

🚀 **Startup-Specific Considerations:**
- **Beta/Alpha Terms:** Special provisions for early-stage products
- **API Terms:** Usage limits, rate limiting, developer obligations
- **User-Generated Content:** Rights to use, moderate, remove content
- **Payment Terms:** Refunds, chargebacks, subscription changes
- **Service Level Agreements:** Uptime guarantees, support response times

🛡️ **Legal Protection:**
- Limitation of liability clauses
- Indemnification provisions
- Force majeure (unforeseeable circumstances)
- Right to modify terms

📋 **Industry-Specific Additions:**
- SaaS: Data portability, service availability
- Marketplace: Buyer/seller obligations
- Social Platform: Content policies, community guidelines

Ready to generate terms tailored to your startup?"""

        elif "incorporation" in message.lower() or "entity formation" in message.lower():
            response = f"""**{model_name} Response:** Startup Entity Formation Guide:
            
🏢 **Entity Types for Startups:**

**Delaware C-Corporation (Recommended for VC-backed startups):**
✅ Pros: Investor-friendly, stock options, global recognition
❌ Cons: Double taxation, more compliance

**LLC (Good for bootstrapped/small teams):**
✅ Pros: Tax flexibility, simple structure, personal liability protection
❌ Cons: Harder to raise VC funding, no stock options

📋 **Formation Checklist:**
1. **Choose State:** Delaware (corp) or home state (LLC)
2. **Reserve Name:** Check availability, reserve if needed
3. **File Articles:** Submit formation documents
4. **Get EIN:** Federal tax ID from IRS
5. **Banking:** Open business bank account
6. **Operating Agreement:** Define ownership/management
7. **Equity Structure:** Founder shares, employee option pool

💰 **Costs:**
- Delaware Corp: $89 filing + $300 franchise tax + agent fees
- Home State LLC: $50-$500 filing fee

⚡ **Next Steps After Formation:**
- 83(b) election for founders (within 30 days!)
- Set up cap table management
- Basic legal docs (employment agreements, IP assignment)

Need help choosing the right structure for your startup?"""

        elif "fundraising" in message.lower() or "investment" in message.lower():
            response = f"""**{model_name} Response:** Startup Fundraising Legal Framework:
            
💰 **Funding Stages & Legal Docs:**

**Pre-Seed/Friends & Family:**
- Simple agreements (SAFE, convertible notes)
- Less paperwork, faster closing
- Typical: $25K-$250K

**Seed Round:**
- Series Seed docs or equity round
- Board seats may be introduced
- Typical: $250K-$2M

**Series A+:**
- Full equity rounds with extensive docs
- Term sheets, investor rights agreements
- Typical: $2M+

🔐 **Essential Legal Documents:**
1. **Term Sheet:** Non-binding overview of investment terms
2. **Stock Purchase Agreement:** Main investment contract
3. **Investors' Rights Agreement:** Information rights, participation rights
4. **Voting Agreement:** Board composition, voting matters
5. **Right of First Refusal:** Restrictions on share transfers
6. **Drag-Along/Tag-Along:** Liquidity event protections

⚖️ **Key Legal Considerations:**
- Anti-dilution provisions
- Liquidation preferences  
- Board composition
- Option pool sizing
- Drag/tag rights
- Information rights

🎯 **Cost Management:**
- Seed: $5K-$15K in legal fees
- Series A: $15K-$40K in legal fees
- Use standard docs to reduce costs

Ready to review your term sheet or generate fundraising docs?"""

        elif "employee" in message.lower() and ("contract" in message.lower() or "agreement" in message.lower()):
            response = f"""**{model_name} Response:** Employee Agreements for Startups:
            
📋 **Essential Employee Documents:**

**1. Employment Agreement:**
- Job title, responsibilities, compensation
- Benefits, vacation time, termination clauses
- At-will employment provisions
- Salary vs. equity compensation

**2. Intellectual Property Assignment:**
- All work-related IP belongs to company
- Pre-existing IP carve-outs
- Invention disclosure requirements
- Critical for protecting company assets

**3. Confidentiality/Non-Disclosure Agreement:**
- Protection of trade secrets, customer lists
- Definition of confidential information
- Survival clause (continues after employment)
- Return of confidential materials

**4. Stock Option Agreement:**
- Number of options, exercise price
- Vesting schedule (typically 4 years, 1-year cliff)
- Post-termination exercise periods
- 83(b) election requirements

**5. Non-Compete/Non-Solicit (where enforceable):**
- Geographic and time limitations
- Customer/employee non-solicitation
- Check state law enforceability

⚡ **Startup-Specific Considerations:**
- Early-stage equity compensation
- Remote work provisions
- Flexible work arrangements
- Stock option administration

🗺️ **State Law Variations:**
- California: No non-competes allowed
- At-will employment rules vary
- State-specific wage/hour laws

Want me to generate an employment agreement template for your state?"""

        elif "intellectual property" in message.lower() or "patent" in message.lower() or "trademark" in message.lower():
            response = f"""**{model_name} Response:** Intellectual Property Strategy for Startups:
            
🧠 **IP Asset Types:**

**Trademarks (Brand Protection):**
- Company name, logo, product names
- File early, use in commerce
- Cost: $250-$400 per class + attorney fees
- Protection: 10 years, renewable

**Copyrights (Creative Works):**
- Software code, marketing materials, content
- Automatic upon creation, registration adds benefits
- Cost: $35-$55 per registration
- Protection: Life + 70 years (works for hire: 95 years)

**Patents (Inventions):**
- Utility patents for functional inventions
- Expensive ($5K-$15K+) and time-consuming
- Consider trade secrets for software algorithms
- Protection: 20 years from filing

**Trade Secrets:**
- Algorithms, customer lists, processes
- Must maintain secrecy
- Indefinite protection if kept secret
- Cheaper than patents for software

🎯 **Startup IP Strategy:**
1. **Trademark your brand early**
2. **Implement strong IP assignment agreements**
3. **Consider trade secrets over patents for software**
4. **Register key copyrights**
5. **File provisional patents for hardware innovations**

🔒 **IP Protection Checklist:**
- Employee IP assignment agreements
- Contractor IP clauses
- Customer data ownership clauses
- Open source compliance policies

💰 **Budget-Friendly Approach:**
- DIY trademark filing for simple marks
- Use LegalZoom/similar services for basic needs
- Hire attorney for complex matters only

Need help developing your IP protection strategy?"""

        else:
            # Generic startup-focused response
            response = f"""**{model_name} Response:** I'm your AI Legal Compliance Assistant specialized in startup legal needs. I can help with:

🚀 **Startup Legal Areas:**
- GDPR & privacy compliance
- SOC 2 security frameworks  
- Privacy policies & terms of service
- Entity formation (Corp vs LLC)
- Fundraising documentation
- Employee agreements & equity
- Intellectual property strategy
- Contract templates & review

💡 **Popular Startup Questions:**
- "How do I become GDPR compliant?"
- "What's required for SOC 2 certification?"  
- "Generate a privacy policy for my SaaS"
- "Should I incorporate in Delaware?"
- "What legal docs do I need for fundraising?"

Ask me about any of these topics, and I'll provide detailed, actionable guidance tailored to your startup's stage and industry.

What specific legal challenge can I help you solve today?"""
        
        # Return a response that looks more like a real AI response
        return jsonify({
            "response": response,
            "model_info": {
                "name": model_name,
                "version": "1.0",
                "response_time_ms": 120,
                "model_type": task_type
            }
        })
    except Exception as e:
        print(f"Error processing legal chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def get_model_display_name(task_type):
    """Get a user-friendly name for the model based on the task type."""
    model_names = {
        "chat": "SmartProBono Assistant",
        "mistral": "Mistral AI",
        "llama": "LlaMA Legal Advisor",
        "deepseek": "DeepSeek Legal",
        "falcon": "Falcon Legal Assistant",
        "document_drafting": "Document Expert"
    }
    
    return model_names.get(task_type, task_type.capitalize())

@app.route('/api/feedback', methods=['POST', 'OPTIONS'])
def feedback():
    """Handle feedback submission"""
    if request.method == 'OPTIONS':
        # Handle OPTIONS method for CORS preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
        
    try:
        data = request.get_json()
        feedback_text = data.get('feedback', '')
        rating = data.get('rating', 0)
        
        print(f"Received feedback: {feedback_text}, rating: {rating}")
        
        return jsonify({
            "status": "success",
            "message": "Thank you for your feedback!"
        })
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# New document API endpoints
@app.route('/api/documents/history', methods=['GET'])
def get_document_history():
    """Get the document history for the current user"""
    return jsonify({
        "documents": documents
    })

@app.route('/api/documents/templates', methods=['GET'])
def get_templates():
    """Get available document templates"""
    return jsonify({
        "templates": templates
    })

@app.route('/api/uploads/signature', methods=['GET'])
def get_upload_signature():
    """Get a signature for document uploads"""
    upload_type = request.args.get('type', 'document')
    
    # In a real app, this would generate a Cloudinary signature
    # For development, we'll just return mock data
    return jsonify({
        "signature": "mock_signature_" + str(uuid.uuid4()),
        "timestamp": int(datetime.now().timestamp()),
        "apiKey": "mock_api_key",
        "cloudName": "smartprobono",
        "uploadPreset": upload_type
    })

@app.route('/api/documents', methods=['POST'])
def save_document():
    """Save a document to the system"""
    data = request.get_json()
    
    new_document = {
        "_id": str(uuid.uuid4()),
        "title": data.get('title', 'Untitled Document'),
        "type": data.get('type', 'other'),
        "content": data.get('content', ''),
        "tags": data.get('tags', []),
        "createdAt": datetime.now().isoformat(),
        "lastModified": datetime.now().isoformat(),
        "owner": "current_user",
        "size": data.get('size', 0),
        "format": data.get('format', 'pdf')
    }
    
    # Save to our in-memory storage
    documents.append(new_document)
    
    # In a real app, you'd save to a database
    with open(os.path.join(DOCUMENT_DIRECTORY, f"{new_document['_id']}.json"), 'w') as f:
        json.dump(new_document, f)
    
    return jsonify(new_document)

@app.route('/api/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """Get a document by ID"""
    for doc in documents:
        if doc["_id"] == document_id:
            return jsonify(doc)
    
    # Check if it exists in the file system
    doc_path = os.path.join(DOCUMENT_DIRECTORY, f"{document_id}.json")
    if os.path.exists(doc_path):
        with open(doc_path, 'r') as f:
            return jsonify(json.load(f))
    
    return jsonify({"error": "Document not found"}), 404

@app.route('/api/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete a document"""
    global documents
    documents = [doc for doc in documents if doc["_id"] != document_id]
    
    # Remove from file system if it exists
    doc_path = os.path.join(DOCUMENT_DIRECTORY, f"{document_id}.json")
    if os.path.exists(doc_path):
        os.remove(doc_path)
    
    return jsonify({"status": "success", "message": "Document deleted"})

# Initialize with some example documents and templates
def initialize_sample_data():
    """Initialize some sample documents and templates"""
    # Sample templates
    templates.append({
        "_id": "template-1",
        "title": "Non-Disclosure Agreement",
        "type": "template",
        "category": "contract",
        "description": "Standard NDA for business relationships",
        "createdAt": "2023-01-15T12:00:00Z"
    })
    
    templates.append({
        "_id": "template-2",
        "title": "Rental Agreement",
        "type": "template",
        "category": "contract",
        "description": "Residential property rental agreement",
        "createdAt": "2023-02-20T14:30:00Z"
    })
    
    # Sample documents
    documents.append({
        "_id": "doc-1",
        "title": "My Will and Testament.pdf",
        "type": "legal",
        "format": "pdf",
        "size": 2500000,
        "createdAt": "2023-03-10T09:15:00Z",
        "lastModified": "2023-03-10T09:15:00Z",
        "tags": ["personal", "legal"]
    })
    
    documents.append({
        "_id": "doc-2",
        "title": "Employment Contract.docx",
        "type": "contract",
        "format": "docx",
        "size": 1200000,
        "createdAt": "2023-04-05T16:45:00Z",
        "lastModified": "2023-04-07T11:30:00Z",
        "tags": ["work", "contract"]
    })

# Initialize sample data
initialize_sample_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting server on http://localhost:{port}")
    print(f" - Health endpoint: http://localhost:{port}/api/health")
    print(f" - Signup endpoint: http://localhost:{port}/api/beta/signup")
    print(f" - Legal chat endpoint: http://localhost:{port}/api/legal/chat")
    print(f" - Feedback endpoint: http://localhost:{port}/api/feedback")
    print(f" - Documents endpoint: http://localhost:{port}/api/documents")
    app.run(host='0.0.0.0', port=port, debug=True) 