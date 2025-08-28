#!/usr/bin/env python3
"""
Test script for Zoho email configuration with DKIM authentication
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid

def test_zoho_email(recipient_email=None):
    """
    Test sending an email via Zoho with proper DKIM headers
    """
    if not recipient_email:
        print("Error: Please provide a recipient email address")
        print("Usage: python test_zoho_email.py recipient@example.com")
        return False
    
    # Get environment variables
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    # Check if variables are set
    missing_vars = []
    if not smtp_server:
        missing_vars.append("SMTP_SERVER")
    if not smtp_port:
        missing_vars.append("SMTP_PORT")
    if not smtp_username:
        missing_vars.append("SMTP_USERNAME")
    if not smtp_password:
        missing_vars.append("SMTP_PASSWORD")
    
    if missing_vars:
        print("Error: Missing environment variables:", ", ".join(missing_vars))
        print("Please run source ./load_email_config.sh first")
        return False
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = "SmartProBono Email Test with DKIM"
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain='smartprobono.org')
    
    # Email content
    html_content = """
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #0078d4; color: white; padding: 10px 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>SmartProBono Email Test</h2>
                </div>
                <div style="padding: 20px;">
                    <p>This is a test email sent from SmartProBono using Zoho with DKIM authentication.</p>
                    <p>If you're receiving this, your email configuration is working correctly!</p>
                    <p>This email should pass DKIM verification checks.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    # Send the email
    try:
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            print(f"Logging in as {smtp_username}...")
            server.login(smtp_username, smtp_password)
            
            print(f"Sending test email to {recipient_email}...")
            server.send_message(msg)
            
        print("Email sent successfully!")
        print("Please check your inbox and verify that:")
        print("1. The email arrived (not in spam)")
        print("2. It displays with proper formatting")
        print("3. Checking email headers shows DKIM=pass")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    # Get recipient email from command line argument
    recipient = sys.argv[1] if len(sys.argv) > 1 else None
    test_zoho_email(recipient) 