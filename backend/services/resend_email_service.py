"""
Resend email service for sending contact form emails using Resend API.
"""
import requests
import logging
from typing import Dict, Any, Optional
from flask import current_app

logger = logging.getLogger(__name__)

class ResendEmailService:
    """Service for sending emails via Resend API."""
    
    def __init__(self):
        self.api_key = current_app.config.get('RESEND_API_KEY')
        self.from_email = current_app.config.get('RESEND_FROM_EMAIL', 'SmartProBono <onboarding@resend.dev>')
        self.base_url = 'https://api.resend.com/emails'
    
    def send_contact_form_email(self, form_data: Dict[str, Any]) -> bool:
        """Send contact form email via Resend."""
        try:
            if not self.api_key:
                logger.warning("Resend API key not configured, falling back to logging")
                self._log_email_content(form_data)
                return True
            
            # Create email payload
            payload = {
                "from": self.from_email,
                "to": ["bferrell@smartprobono.org"],
                "subject": f"New Contact Form Submission from {form_data.get('firstName', '')} {form_data.get('lastName', '')}",
                "html": self._create_contact_email_html(form_data),
                "text": self._create_contact_email_text(form_data)
            }
            
            # Send email via Resend API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Contact form email sent successfully via Resend")
                return True
            else:
                logger.error(f"Resend API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending contact form email via Resend: {str(e)}")
            return False
    
    def send_auto_reply(self, recipient_email: str, recipient_name: str) -> bool:
        """Send auto-reply via Resend."""
        try:
            if not self.api_key:
                logger.warning("Resend API key not configured, falling back to logging")
                self._log_auto_reply_content(recipient_email, recipient_name)
                return True
            
            # Create auto-reply payload
            payload = {
                "from": self.from_email,
                "to": [recipient_email],
                "subject": "Thank you for contacting SmartProBono",
                "html": self._create_auto_reply_html(recipient_name),
                "text": self._create_auto_reply_text(recipient_name)
            }
            
            # Send email via Resend API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Auto-reply sent successfully via Resend to {recipient_email}")
                return True
            else:
                logger.error(f"Resend API error for auto-reply: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending auto-reply via Resend: {str(e)}")
            return False
    
    def _create_contact_email_html(self, form_data: Dict[str, Any]) -> str:
        """Create HTML email content for contact form."""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0F3D5E;">New Contact Form Submission</h2>
                <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Name:</strong> {form_data.get('firstName', '')} {form_data.get('lastName', '')}</p>
                    <p><strong>Email:</strong> {form_data.get('email', '')}</p>
                    <p><strong>Phone:</strong> {form_data.get('phone', 'N/A')}</p>
                </div>
                <div style="background: #fff; padding: 20px; border-left: 4px solid #1FB6A6;">
                    <h3 style="color: #0F3D5E; margin-top: 0;">Message:</h3>
                    <p style="white-space: pre-wrap;">{form_data.get('message', '')}</p>
                </div>
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    This message was sent from the SmartProBono contact form.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _create_contact_email_text(self, form_data: Dict[str, Any]) -> str:
        """Create text email content for contact form."""
        return f"""
New contact form submission received:

Name: {form_data.get('firstName', '')} {form_data.get('lastName', '')}
Email: {form_data.get('email', '')}
Phone: {form_data.get('phone', 'N/A')}

Message:
{form_data.get('message', '')}

---
This message was sent from the SmartProBono contact form.
        """
    
    def _create_auto_reply_html(self, recipient_name: str) -> str:
        """Create HTML auto-reply content."""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0F3D5E;">Thank you for contacting SmartProBono!</h2>
                <p>Dear {recipient_name},</p>
                <p>Thank you for reaching out to SmartProBono! We have received your message and will get back to you within 24 hours.</p>
                <p>Your message is important to us, and we're here to help with your legal needs.</p>
                <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #0F3D5E; margin-top: 0;">Best regards,</h3>
                    <p>The SmartProBono Team</p>
                </div>
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    <strong>SmartProBono - Making Legal Help Accessible</strong><br>
                    Email: bferrell@smartprobono.org<br>
                    Phone: (401) 217-9799
                </p>
            </div>
        </body>
        </html>
        """
    
    def _create_auto_reply_text(self, recipient_name: str) -> str:
        """Create text auto-reply content."""
        return f"""
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
    
    def _log_email_content(self, form_data: Dict[str, Any]):
        """Log email content when Resend is not configured."""
        logger.info(f"Contact form email would be sent: {self._create_contact_email_text(form_data)}")
    
    def _log_auto_reply_content(self, recipient_email: str, recipient_name: str):
        """Log auto-reply content when Resend is not configured."""
        logger.info(f"Auto-reply would be sent to {recipient_email}: {self._create_auto_reply_text(recipient_name)}")

# Global Resend email service instance
resend_email_service = ResendEmailService()
