#!/usr/bin/env python3
"""
SmartProBono Email Test Script
This script helps test email sending functionality to ensure notifications work.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_test_email(recipient_email, subject="SmartProBono Email Test", message="This is a test email from SmartProBono."):
    """Send a test email to verify email functionality."""
    
    # Get email configuration from environment variables
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_username = os.environ.get('SMTP_USERNAME', 'info@smartprobono.org')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    if not smtp_password:
        print("Error: SMTP_PASSWORD environment variable is not set.")
        print("Please run 'source load_email_config.sh' before running this script.")
        return False
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Add body to email
    body = f"""
    {message}
    
    This email was sent from {smtp_username} via {smtp_server}:{smtp_port}.
    If you received this email, your email configuration is working correctly.
    
    Timestamp: {os.popen('date').read().strip()}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
    try:
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        
        print(f"Logging in as {smtp_username}...")
        server.login(smtp_username, smtp_password)
        
        print(f"Sending email to {recipient_email}...")
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {recipient_email}!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


if __name__ == "__main__":
    # Check if recipient email was provided as argument
    if len(sys.argv) > 1:
        recipient = sys.argv[1]
    else:
        # Prompt for recipient email
        recipient = input("Enter recipient email address: ")
    
    # Optional custom subject and message
    if len(sys.argv) > 2:
        custom_subject = sys.argv[2]
    else:
        custom_subject = "SmartProBono Email Test"
    
    if len(sys.argv) > 3:
        custom_message = sys.argv[3]
    else:
        custom_message = "This is a test email from SmartProBono. If you received this, the email system is working correctly."
    
    # Send the test email
    success = send_test_email(recipient, custom_subject, custom_message)
    
    if success:
        print("\nEmail settings are configured correctly.")
    else:
        print("\nThere was a problem with your email configuration.")
        print("Please check your settings in .env.email and try again.") 