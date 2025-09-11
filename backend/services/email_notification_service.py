"""
Email Notification Service for SmartProBono
Handles email notifications for court dates, case updates, and system alerts.
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from flask import current_app
from backend.database import db
from backend.models import CourtDate, User, Case, Notification
import logging
import threading
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EmailNotificationService:
    """Service for sending email notifications."""
    
    def __init__(self):
        self.smtp_server = current_app.config.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = current_app.config.get('SMTP_PORT', 587)
        self.sender_email = current_app.config.get('SENDER_EMAIL')
        self.sender_password = current_app.config.get('SENDER_PASSWORD')
        self.sender_name = current_app.config.get('SENDER_NAME', 'SmartProBono')
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None, attachments: List[Dict] = None):
        """Send an email to a recipient."""
        try:
            if not self.sender_email or not self.sender_password:
                logger.warning("Email credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text body
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML body if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    with open(attachment['file_path'], 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {attachment["filename"]}'
                        )
                        msg.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_court_date_reminder(self, court_date_id: int, reminder_type: str = 'upcoming'):
        """Send court date reminder email."""
        try:
            court_date = CourtDate.query.get(court_date_id)
            if not court_date:
                return False
            
            client = User.query.get(court_date.client_id)
            if not client or not client.email:
                return False
            
            # Determine subject and content based on reminder type
            if reminder_type == 'upcoming':
                subject = f"Upcoming Court Date: {court_date.title}"
                days_until = (court_date.scheduled_date - datetime.utcnow()).days
                urgency = "urgent" if days_until <= 1 else "important"
            elif reminder_type == 'tomorrow':
                subject = f"Court Date Tomorrow: {court_date.title}"
                urgency = "urgent"
            elif reminder_type == 'today':
                subject = f"Court Date Today: {court_date.title}"
                urgency = "urgent"
            else:
                subject = f"Court Date Reminder: {court_date.title}"
                urgency = "important"
            
            # Create email content
            body = self._create_court_date_email_body(court_date, client, reminder_type, urgency)
            html_body = self._create_court_date_email_html(court_date, client, reminder_type, urgency)
            
            # Send email
            success = self.send_email(
                to_email=client.email,
                subject=subject,
                body=body,
                html_body=html_body
            )
            
            if success:
                # Mark reminder as sent
                court_date.reminder_sent = True
                db.session.commit()
                
                # Create notification record
                self._create_notification(
                    user_id=client.id,
                    title=subject,
                    message=f"Court date reminder sent for {court_date.title}",
                    notification_type='email_reminder'
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending court date reminder: {e}")
            return False
    
    def send_case_update_notification(self, case_id: int, update_type: str, details: str):
        """Send case update notification email."""
        try:
            case = Case.query.get(case_id)
            if not case:
                return False
            
            client = User.query.get(case.client_id)
            if not client or not client.email:
                return False
            
            subject = f"Case Update: {case.title}"
            body = self._create_case_update_email_body(case, client, update_type, details)
            html_body = self._create_case_update_email_html(case, client, update_type, details)
            
            success = self.send_email(
                to_email=client.email,
                subject=subject,
                body=body,
                html_body=html_body
            )
            
            if success:
                self._create_notification(
                    user_id=client.id,
                    title=subject,
                    message=f"Case update: {update_type}",
                    notification_type='case_update'
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending case update notification: {e}")
            return False
    
    def send_payment_reminder(self, payment_id: int):
        """Send payment reminder email."""
        try:
            from backend.models import Payment
            payment = Payment.query.get(payment_id)
            if not payment:
                return False
            
            client = User.query.get(payment.client_id)
            if not client or not client.email:
                return False
            
            subject = f"Payment Reminder: ${payment.amount}"
            body = self._create_payment_reminder_email_body(payment, client)
            html_body = self._create_payment_reminder_email_html(payment, client)
            
            success = self.send_email(
                to_email=client.email,
                subject=subject,
                body=body,
                html_body=html_body
            )
            
            if success:
                self._create_notification(
                    user_id=client.id,
                    title=subject,
                    message=f"Payment reminder sent for ${payment.amount}",
                    notification_type='payment_reminder'
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending payment reminder: {e}")
            return False
    
    def send_bulk_court_date_reminders(self, days_ahead: int = 1):
        """Send bulk court date reminders for upcoming dates."""
        try:
            target_date = datetime.utcnow() + timedelta(days=days_ahead)
            start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            court_dates = CourtDate.query.filter(
                CourtDate.scheduled_date.between(start_date, end_date),
                CourtDate.reminder_sent == False
            ).all()
            
            success_count = 0
            for court_date in court_dates:
                if self.send_court_date_reminder(court_date.id, 'upcoming'):
                    success_count += 1
            
            logger.info(f"Sent {success_count} court date reminders out of {len(court_dates)}")
            return success_count
            
        except Exception as e:
            logger.error(f"Error sending bulk court date reminders: {e}")
            return 0
    
    def _create_court_date_email_body(self, court_date: CourtDate, client: User, reminder_type: str, urgency: str) -> str:
        """Create plain text email body for court date reminder."""
        scheduled_date = court_date.scheduled_date.strftime('%A, %B %d, %Y at %I:%M %p')
        
        body = f"""
Dear {client.first_name or 'Client'},

This is a {urgency} reminder about your upcoming court date.

COURT DATE DETAILS:
- Event: {court_date.title}
- Date & Time: {scheduled_date}
- Location: {court_date.court_location}
- Room: {court_date.court_room or 'TBD'}
- Case: {court_date.case_id or 'N/A'}

DESCRIPTION:
{court_date.description or 'No additional details provided.'}

IMPORTANT REMINDERS:
- Arrive 15-30 minutes early
- Bring all required documents
- Dress appropriately for court
- Contact your attorney if you have questions

If you need to reschedule or have any questions, please contact us immediately.

Best regards,
SmartProBono Team
        """
        return body.strip()
    
    def _create_court_date_email_html(self, court_date: CourtDate, client: User, reminder_type: str, urgency: str) -> str:
        """Create HTML email body for court date reminder."""
        scheduled_date = court_date.scheduled_date.strftime('%A, %B %d, %Y at %I:%M %p')
        urgency_color = "#dc3545" if urgency == "urgent" else "#ffc107"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0F3D5E; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .urgent {{ background-color: {urgency_color}; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .footer {{ background-color: #6c757d; color: white; padding: 15px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Court Date Reminder</h1>
            </div>
            <div class="content">
                <p>Dear {client.first_name or 'Client'},</p>
                
                <div class="urgent">
                    <h2>⚠️ {urgency.upper()} REMINDER</h2>
                    <p>This is a {urgency} reminder about your upcoming court date.</p>
                </div>
                
                <div class="details">
                    <h3>Court Date Details:</h3>
                    <ul>
                        <li><strong>Event:</strong> {court_date.title}</li>
                        <li><strong>Date & Time:</strong> {scheduled_date}</li>
                        <li><strong>Location:</strong> {court_date.court_location}</li>
                        <li><strong>Room:</strong> {court_date.court_room or 'TBD'}</li>
                        <li><strong>Case:</strong> {court_date.case_id or 'N/A'}</li>
                    </ul>
                </div>
                
                <div class="details">
                    <h3>Description:</h3>
                    <p>{court_date.description or 'No additional details provided.'}</p>
                </div>
                
                <div class="details">
                    <h3>Important Reminders:</h3>
                    <ul>
                        <li>Arrive 15-30 minutes early</li>
                        <li>Bring all required documents</li>
                        <li>Dress appropriately for court</li>
                        <li>Contact your attorney if you have questions</li>
                    </ul>
                </div>
                
                <p>If you need to reschedule or have any questions, please contact us immediately.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>SmartProBono Team</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _create_case_update_email_body(self, case: Case, client: User, update_type: str, details: str) -> str:
        """Create plain text email body for case update."""
        body = f"""
Dear {client.first_name or 'Client'},

We have an update regarding your case: {case.title}

UPDATE TYPE: {update_type.upper()}

DETAILS:
{details}

CASE INFORMATION:
- Case ID: {case.id}
- Status: {case.status}
- Priority: {case.priority}
- Practice Area: {case.practice_area or 'N/A'}

If you have any questions about this update, please don't hesitate to contact us.

Best regards,
SmartProBono Team
        """
        return body.strip()
    
    def _create_case_update_email_html(self, case: Case, client: User, update_type: str, details: str) -> str:
        """Create HTML email body for case update."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0F3D5E; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .update {{ background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .footer {{ background-color: #6c757d; color: white; padding: 15px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Case Update</h1>
            </div>
            <div class="content">
                <p>Dear {client.first_name or 'Client'},</p>
                
                <div class="update">
                    <h2>📋 Case Update: {update_type.upper()}</h2>
                    <p>We have an update regarding your case: <strong>{case.title}</strong></p>
                </div>
                
                <div class="details">
                    <h3>Update Details:</h3>
                    <p>{details}</p>
                </div>
                
                <div class="details">
                    <h3>Case Information:</h3>
                    <ul>
                        <li><strong>Case ID:</strong> {case.id}</li>
                        <li><strong>Status:</strong> {case.status}</li>
                        <li><strong>Priority:</strong> {case.priority}</li>
                        <li><strong>Practice Area:</strong> {case.practice_area or 'N/A'}</li>
                    </ul>
                </div>
                
                <p>If you have any questions about this update, please don't hesitate to contact us.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>SmartProBono Team</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _create_payment_reminder_email_body(self, payment: 'Payment', client: User) -> str:
        """Create plain text email body for payment reminder."""
        due_date = payment.due_date.strftime('%A, %B %d, %Y') if payment.due_date else 'ASAP'
        
        body = f"""
Dear {client.first_name or 'Client'},

This is a reminder about your outstanding payment.

PAYMENT DETAILS:
- Amount: ${payment.amount}
- Due Date: {due_date}
- Payment Type: {payment.payment_type}
- Reference: {payment.reference_number or 'N/A'}

Please make your payment as soon as possible to avoid any late fees or service interruptions.

You can make payments through our online portal or contact us for alternative payment methods.

Best regards,
SmartProBono Team
        """
        return body.strip()
    
    def _create_payment_reminder_email_html(self, payment: 'Payment', client: User) -> str:
        """Create HTML email body for payment reminder."""
        due_date = payment.due_date.strftime('%A, %B %d, %Y') if payment.due_date else 'ASAP'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0F3D5E; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .payment {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .footer {{ background-color: #6c757d; color: white; padding: 15px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Payment Reminder</h1>
            </div>
            <div class="content">
                <p>Dear {client.first_name or 'Client'},</p>
                
                <div class="payment">
                    <h2>💰 Payment Reminder</h2>
                    <p>This is a reminder about your outstanding payment.</p>
                </div>
                
                <div class="details">
                    <h3>Payment Details:</h3>
                    <ul>
                        <li><strong>Amount:</strong> ${payment.amount}</li>
                        <li><strong>Due Date:</strong> {due_date}</li>
                        <li><strong>Payment Type:</strong> {payment.payment_type}</li>
                        <li><strong>Reference:</strong> {payment.reference_number or 'N/A'}</li>
                    </ul>
                </div>
                
                <p>Please make your payment as soon as possible to avoid any late fees or service interruptions.</p>
                <p>You can make payments through our online portal or contact us for alternative payment methods.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>SmartProBono Team</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _create_notification(self, user_id: int, title: str, message: str, notification_type: str):
        """Create a notification record in the database."""
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                priority='medium'
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error creating notification: {e}")

# Create singleton instance
email_notification_service = EmailNotificationService()
