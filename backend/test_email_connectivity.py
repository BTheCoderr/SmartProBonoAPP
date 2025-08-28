#!/usr/bin/env python3
"""
Email connectivity test script for SmartProBono.
Tests the email configuration and sends a test email.
"""

import os
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import getpass
import argparse

def create_test_email(recipient):
    """Create a test email message."""
    message = MIMEMultipart("alternative")
    message["Subject"] = f"SmartProBono Email Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    message["From"] = "bferrell@smartprobono.org"
    message["To"] = recipient
    
    # Create the plain-text version of the message
    text = """
    Hello,
    
    This is a test email from the SmartProBono platform.
    
    If you're receiving this, the email configuration is working correctly.
    
    Time of test: {}
    
    Regards,
    SmartProBono System
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Create the HTML version of the message
    html = """
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #1976d2; color: white; padding: 20px; text-align: center;">
                <h1>SmartProBono Email Test</h1>
            </div>
            <div style="padding: 20px;">
                <p>Hello,</p>
                <p>This is a test email from the <strong>SmartProBono</strong> platform.</p>
                <p>If you're receiving this, the email configuration is working correctly.</p>
                <p><em>Time of test: {}</em></p>
                <p>Regards,<br>SmartProBono System</p>
            </div>
            <div style="background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 12px; color: #666;">
                <p>© 2025 SmartProBono. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Attach both plain-text and HTML versions
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))
    
    return message

def test_email_connection(smtp_server, smtp_port, username, password, use_tls=True, recipient=None):
    """Test email server connection and send a test email if recipient is provided."""
    try:
        # Create a secure SSL/TLS context
        context = ssl.create_default_context() if use_tls else None
        
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        
        if use_tls:
            # For TLS connections
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        else:
            # For SSL connections
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        
        print("Connection established.")
        
        # Login to the SMTP server
        print(f"Logging in as {username}...")
        server.login(username, password)
        print("Login successful.")
        
        # If a recipient is provided, send a test email
        if recipient:
            print(f"Creating test email to send to {recipient}...")
            message = create_test_email(recipient)
            
            print("Sending test email...")
            server.sendmail(
                from_addr="bferrell@smartprobono.org",
                to_addrs=recipient,
                msg=message.as_string()
            )
            print(f"Test email sent successfully to {recipient}!")
        
        # Close the connection
        server.quit()
        print("SMTP server connection closed.")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """Main function to run the email test."""
    parser = argparse.ArgumentParser(description="Test email connectivity for SmartProBono.")
    parser.add_argument("--recipient", help="Email address to send test email to")
    parser.add_argument("--server", help="SMTP server address")
    parser.add_argument("--port", type=int, help="SMTP server port")
    parser.add_argument("--username", help="SMTP username")
    parser.add_argument("--no-tls", action="store_true", help="Disable TLS encryption")
    args = parser.parse_args()
    
    # Get SMTP configuration from environment variables or command line
    smtp_server = args.server or os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    smtp_port = args.port or int(os.environ.get("MAIL_PORT", 587))
    username = args.username or os.environ.get("MAIL_USERNAME", "bferrell@smartprobono.org")
    use_tls = not args.no_tls
    
    # Get password
    password = os.environ.get("MAIL_PASSWORD")
    if not password:
        password = getpass.getpass(f"Enter password for {username}: ")
    
    # Get recipient email
    recipient = args.recipient or os.environ.get("TEST_EMAIL_RECIPIENT")
    if not recipient:
        recipient = input("Enter recipient email for test (leave empty to skip sending): ")
        if not recipient.strip():
            recipient = None
    
    print("\n=== SmartProBono Email Connectivity Test ===")
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Username: {username}")
    print(f"Use TLS: {use_tls}")
    if recipient:
        print(f"Recipient: {recipient}")
    print("=" * 45 + "\n")
    
    success = test_email_connection(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password,
        use_tls=use_tls,
        recipient=recipient
    )
    
    if success:
        print("\n✅ Email test completed successfully!")
        return 0
    else:
        print("\n❌ Email test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 