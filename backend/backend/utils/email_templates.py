"""
Email templates for the application.
"""
from flask import render_template_string

# Template for welcome email
WELCOME_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #1976d2; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background-color: #1976d2; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to SmartProBono</h1>
    </div>
    <div class="content">
        <p>Hello {{name}},</p>
        <p>Thank you for registering with SmartProBono. We're excited to have you join our platform.</p>
        <p>With your account, you can:</p>
        <ul>
            <li>Access free legal resources</li>
            <li>Create and manage legal documents</li>
            <li>Connect with legal professionals</li>
            <li>Track your cases and forms</li>
        </ul>
        <p style="text-align: center; margin-top: 30px;">
            <a href="{{login_url}}" class="button">Login to Your Account</a>
        </p>
    </div>
    <div class="footer">
        <p>© 2025 SmartProBono. All rights reserved.</p>
        <p>If you did not sign up for this service, please disregard this email.</p>
    </div>
</body>
</html>
"""

# Template for password reset email
PASSWORD_RESET_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #1976d2; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background-color: #1976d2; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }
        .alert { background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 10px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Password Reset Request</h1>
    </div>
    <div class="content">
        <p>Hello {{name}},</p>
        <p>We received a request to reset your password for your SmartProBono account.</p>
        <p style="text-align: center; margin-top: 30px;">
            <a href="{{reset_url}}" class="button">Reset Your Password</a>
        </p>
        <div class="alert">
            <p>This link will expire in 30 minutes.</p>
            <p>If you did not request a password reset, please ignore this email or contact support.</p>
        </div>
    </div>
    <div class="footer">
        <p>© 2025 SmartProBono. All rights reserved.</p>
    </div>
</body>
</html>
"""

# Template for document sharing email
DOCUMENT_SHARE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #1976d2; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background-color: #1976d2; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }
        .document-box { background-color: #e3f2fd; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Document Shared With You</h1>
    </div>
    <div class="content">
        <p>Hello,</p>
        <p>{{sender_name}} has shared a document with you via SmartProBono.</p>
        <div class="document-box">
            <h3>{{document_title}}</h3>
            <p>{{document_description}}</p>
        </div>
        <p style="text-align: center; margin-top: 30px;">
            <a href="{{document_url}}" class="button">View Document</a>
        </p>
        {% if message %}
        <p><strong>Message from {{sender_name}}:</strong></p>
        <p>{{message}}</p>
        {% endif %}
    </div>
    <div class="footer">
        <p>© 2025 SmartProBono. All rights reserved.</p>
    </div>
</body>
</html>
"""

# Template for form submission confirmation
FORM_SUBMISSION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #1976d2; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background-color: #1976d2; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }
        .info-box { background-color: #e8f4f8; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Form Submission Confirmation</h1>
    </div>
    <div class="content">
        <p>Hello {{name}},</p>
        <p>Thank you for submitting the {{form_type}} form. Your submission has been received and is being processed.</p>
        <div class="info-box">
            <h3>Submission Details:</h3>
            <p><strong>Reference ID:</strong> {{reference_id}}</p>
            <p><strong>Submitted:</strong> {{submission_date}}</p>
            <p><strong>Status:</strong> {{status}}</p>
        </div>
        <p style="text-align: center; margin-top: 30px;">
            <a href="{{status_url}}" class="button">Check Status</a>
        </p>
        <p>If you have any questions or need assistance, please don't hesitate to contact us.</p>
    </div>
    <div class="footer">
        <p>© 2025 SmartProBono. All rights reserved.</p>
    </div>
</body>
</html>
"""

def render_welcome_email(name, login_url):
    """Render welcome email template."""
    return render_template_string(
        WELCOME_EMAIL_TEMPLATE,
        name=name,
        login_url=login_url
    )

def render_password_reset_email(name, reset_url):
    """Render password reset email template."""
    return render_template_string(
        PASSWORD_RESET_TEMPLATE,
        name=name,
        reset_url=reset_url
    )

def render_document_share_email(sender_name, document_title, document_description, document_url, message=None):
    """Render document sharing email template."""
    return render_template_string(
        DOCUMENT_SHARE_TEMPLATE,
        sender_name=sender_name,
        document_title=document_title,
        document_description=document_description,
        document_url=document_url,
        message=message
    )

def render_form_submission_email(name, form_type, reference_id, submission_date, status, status_url):
    """Render form submission confirmation email template."""
    return render_template_string(
        FORM_SUBMISSION_TEMPLATE,
        name=name,
        form_type=form_type,
        reference_id=reference_id,
        submission_date=submission_date,
        status=status,
        status_url=status_url
    ) 