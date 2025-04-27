"""
Email Service for SmartProBono
Handles sending verification emails, password reset emails, and other notifications
"""
import os
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

logger = logging.getLogger(__name__)

# Email configuration from environment variables
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'noreply@smartprobono.example.com')
EMAIL_FROM_NAME = os.environ.get('EMAIL_FROM_NAME', 'SmartProBono')
APP_URL = os.environ.get('APP_URL', 'http://localhost:3000')

class EmailService:
    """Service for sending emails from the application"""
    
    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        """
        Send an email
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content as fallback
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not EMAIL_USERNAME or not EMAIL_PASSWORD:
            logger.warning("Email credentials not configured. Email would have been sent to: %s", to_email)
            logger.info("Email subject: %s", subject)
            logger.info("Email content: %s", html_content[:100] + "..." if len(html_content) > 100 else html_content)
            # Return True in development to not block the flow
            return True
            
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = formataddr((EMAIL_FROM_NAME, EMAIL_FROM))
            message['To'] = to_email
            
            # Add text part if provided
            if text_content:
                message.attach(MIMEText(text_content, 'plain'))
                
            # Add HTML part
            message.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(message)
                
            logger.info("Email sent successfully to %s", to_email)
            return True
            
        except Exception as e:
            logger.error("Failed to send email: %s", str(e))
            return False
    
    @classmethod
    def send_verification_email(cls, to_email, username, verification_link):
        """
        Send an email verification link
        
        Args:
            to_email (str): Recipient email address
            username (str): User's username
            verification_link (str): Email verification link
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = "Verify Your SmartProBono Account"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a69bd; color: white; padding: 10px 20px; }}
                .content {{ padding: 20px; border: 1px solid #ddd; }}
                .button {{ display: inline-block; background-color: #4a69bd; color: white; 
                          padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to SmartProBono!</h1>
                </div>
                <div class="content">
                    <p>Hi {username},</p>
                    <p>Thank you for registering with SmartProBono. Please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_link}" class="button">Verify Email Address</a>
                    </p>
                    <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
                    <p>{verification_link}</p>
                    <p>This link will expire in 48 hours.</p>
                    <p>If you did not create an account, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; {datetime.now().year} SmartProBono. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to SmartProBono!
        
        Hi {username},
        
        Thank you for registering with SmartProBono. Please verify your email address by clicking the link below:
        
        {verification_link}
        
        This link will expire in 48 hours.
        
        If you did not create an account, please ignore this email.
        
        © {datetime.now().year} SmartProBono. All rights reserved.
        """
        
        return cls.send_email(to_email, subject, html_content, text_content)
    
    @classmethod
    def send_password_reset_email(cls, to_email, username, reset_link):
        """
        Send a password reset link
        
        Args:
            to_email (str): Recipient email address
            username (str): User's username
            reset_link (str): Password reset link
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = "Reset Your SmartProBono Password"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a69bd; color: white; padding: 10px 20px; }}
                .content {{ padding: 20px; border: 1px solid #ddd; }}
                .button {{ display: inline-block; background-color: #4a69bd; color: white; 
                          padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>Hi {username},</p>
                    <p>We received a request to reset your SmartProBono password. Click the button below to reset it:</p>
                    <p style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </p>
                    <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
                    <p>{reset_link}</p>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you did not request a password reset, please ignore this email or contact support if you have concerns.</p>
                </div>
                <div class="footer">
                    <p>&copy; {datetime.now().year} SmartProBono. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request
        
        Hi {username},
        
        We received a request to reset your SmartProBono password. Please use the following link to reset it:
        
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you did not request a password reset, please ignore this email or contact support if you have concerns.
        
        © {datetime.now().year} SmartProBono. All rights reserved.
        """
        
        return cls.send_email(to_email, subject, html_content, text_content)
    
    @classmethod
    def send_security_alert_email(cls, to_email, username, event_type, event_time, ip_address, user_agent):
        """
        Send a security alert email
        
        Args:
            to_email (str): Recipient email address
            username (str): User's username
            event_type (str): Type of security event (e.g., "New Login", "Password Changed")
            event_time (datetime): Time of the event
            ip_address (str): IP address associated with the event
            user_agent (str): User agent associated with the event
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = f"Security Alert: {event_type} on Your SmartProBono Account"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #e74c3c; color: white; padding: 10px 20px; }}
                .content {{ padding: 20px; border: 1px solid #ddd; }}
                .event-details {{ background-color: #f8f9fa; padding: 15px; margin: 15px 0; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Security Alert</h1>
                </div>
                <div class="content">
                    <p>Hi {username},</p>
                    <p>We detected a {event_type.lower()} on your SmartProBono account. If this was you, you can ignore this email.</p>
                    <div class="event-details">
                        <p><strong>Event:</strong> {event_type}</p>
                        <p><strong>Time:</strong> {event_time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                        <p><strong>IP Address:</strong> {ip_address}</p>
                        <p><strong>Device:</strong> {user_agent[:100] + '...' if len(user_agent) > 100 else user_agent}</p>
                    </div>
                    <p>If you did not perform this action, please secure your account by changing your password immediately and contact our support team.</p>
                </div>
                <div class="footer">
                    <p>&copy; {datetime.now().year} SmartProBono. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Security Alert: {event_type} on Your SmartProBono Account
        
        Hi {username},
        
        We detected a {event_type.lower()} on your SmartProBono account. If this was you, you can ignore this email.
        
        Event Details:
        - Event: {event_type}
        - Time: {event_time.strftime('%Y-%m-%d %H:%M:%S UTC')}
        - IP Address: {ip_address}
        - Device: {user_agent[:100] + '...' if len(user_agent) > 100 else user_agent}
        
        If you did not perform this action, please secure your account by changing your password immediately and contact our support team.
        
        © {datetime.now().year} SmartProBono. All rights reserved.
        """
        
        return cls.send_email(to_email, subject, html_content, text_content)

def send_document_share_email(recipient_email, subject, message, document_title, share_link):
    """
    Send an email to a recipient with a link to a shared document.
    
    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Email subject
        message (str): Personal message from the sender
        document_title (str): Title of the shared document
        share_link (str): Link to access the shared document
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create email content with HTML formatting
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #3f51b5; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .message {{ border-left: 3px solid #3f51b5; padding-left: 10px; margin: 15px 0; }}
                    .button {{ display: inline-block; background-color: #3f51b5; color: white; padding: 10px 20px; 
                               text-decoration: none; border-radius: 4px; margin-top: 20px; }}
                    .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>SmartProBono Document Shared</h2>
                    </div>
                    <div class="content">
                        <p>Someone has shared a document with you via SmartProBono.</p>
                        <h3>Document: {document_title}</h3>
                        
                        <div class="message">
                            <p>{message}</p>
                        </div>
                        
                        <p>To view the document, please click the button below:</p>
                        <a href="{share_link}" class="button">View Document</a>
                        
                        <p>Or copy this link to your browser:</p>
                        <p>{share_link}</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message from SmartProBono. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Using the same approach as EmailService.send_email
        if not EMAIL_USERNAME or not EMAIL_PASSWORD:
            logger.warning(f"Email credentials not configured. Email would have been sent to: {recipient_email}")
            logger.info(f"Email subject: {subject}")
            logger.info(f"Email content: {html_content[:100]}..." if len(html_content) > 100 else html_content)
            # Return True in development to not block the flow
            return True
            
        # Create message
        message_obj = MIMEMultipart('alternative')
        message_obj['Subject'] = subject
        message_obj['From'] = formataddr((EMAIL_FROM_NAME, EMAIL_FROM))
        message_obj['To'] = recipient_email
        
        # Add HTML part
        message_obj.attach(MIMEText(html_content, 'html'))
        
        # Send email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(message_obj)
            
        logger.info(f"Email sent to {recipient_email} for document: {document_title}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False 