"""
Email service for sending contact form emails and notifications.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from flask import current_app

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails."""
    
    def __init__(self):
        try:
            self.smtp_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
            self.smtp_port = current_app.config.get('MAIL_PORT', 587)
            self.use_tls = current_app.config.get('MAIL_USE_TLS', True)
            self.username = current_app.config.get('MAIL_USERNAME')
            self.password = current_app.config.get('MAIL_PASSWORD')
            self.default_sender = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@smartprobono.org')
        except RuntimeError:
            # Working outside of application context - use defaults
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
            self.use_tls = True
            self.username = None
            self.password = None
            self.default_sender = 'noreply@smartprobono.org'
    
    def send_contact_form_email(self, form_data: Dict[str, Any]) -> bool:
        """Send contact form email."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.default_sender
            msg['To'] = 'bferrell@smartprobono.org'  # Your professional email
            msg['Subject'] = f"New Contact Form Submission from {form_data.get('firstName', '')} {form_data.get('lastName', '')}"
            
            # Create email body
            body = f"""
New contact form submission received:

Name: {form_data.get('firstName', '')} {form_data.get('lastName', '')}
Email: {form_data.get('email', '')}
Phone: {form_data.get('phone', 'N/A')}

Message:
{form_data.get('message', '')}

---
This message was sent from the SmartProBono contact form.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email if credentials are configured
            if self.username and self.password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                server.quit()
                logger.info(f"Contact form email sent successfully to {msg['To']}")
                return True
            else:
                # Log email content instead of sending (for development)
                logger.info(f"Email would be sent to {msg['To']}: {body}")
                return True
                
        except Exception as e:
            logger.error(f"Error sending contact form email: {str(e)}")
            return False
    
    def send_auto_reply(self, recipient_email: str, recipient_name: str) -> bool:
        """Send auto-reply to contact form submitter."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.default_sender
            msg['To'] = recipient_email
            msg['Subject'] = "Thank you for contacting SmartProBono"
            
            body = f"""
Dear {recipient_name},

Thank you for reaching out to SmartProBono! We have received your message and will get back to you within 24 hours.

Your message is important to us, and we're here to help with your legal needs.

Best regards,
The SmartProBono Team

---
SmartProBono - Making Legal Help Accessible
Email: bferrell@smartprobono.org
Phone: (401) 217-9799
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email if credentials are configured
            if self.username and self.password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                server.quit()
                logger.info(f"Auto-reply sent successfully to {recipient_email}")
                return True
            else:
                # Log email content instead of sending (for development)
                logger.info(f"Auto-reply would be sent to {recipient_email}: {body}")
                return True
                
        except Exception as e:
            logger.error(f"Error sending auto-reply: {str(e)}")
            return False

# Global email service instance - will be initialized when app context is available
email_service = None

def get_email_service():
    """Get email service instance, creating it if needed"""
    global email_service
    if email_service is None:
        email_service = EmailService()
    return email_service
