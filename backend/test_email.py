#!/usr/bin/env python3
"""
Test script for email configuration.
Run this to test your email setup before using the contact form.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_smtp():
    """Test Gmail SMTP configuration."""
    print("🧪 Testing Gmail SMTP Configuration...")
    
    # Get configuration from environment or use defaults
    smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('MAIL_PORT', 587))
    username = os.getenv('MAIL_USERNAME', 'bferrell514@gmail.com')
    password = os.getenv('MAIL_PASSWORD')
    from_email = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@smartprobono.org')
    to_email = 'bferrell514@gmail.com'
    
    if not password:
        print("❌ MAIL_PASSWORD not set. Please set your Gmail app password.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "SmartProBono Email Test"
        
        body = """
This is a test email from your SmartProBono contact form system.

If you receive this email, your Zoho SMTP configuration is working correctly!

Test Details:
- From: noreply@smartprobono.org
- To: bferrell@smartprobono.org
- Sent via: Zoho SMTP
- Timestamp: """ + str(os.popen('date').read().strip()) + """

Best regards,
SmartProBono System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        print(f"📧 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print(f"🔐 Logging in as {username}...")
        server.login(username, password)
        
        print(f"📤 Sending test email to {to_email}...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Gmail SMTP test successful! Check your Gmail inbox.")
        return True
        
    except Exception as e:
        print(f"❌ Gmail SMTP test failed: {str(e)}")
        return False

def test_resend_api():
    """Test Resend API configuration."""
    print("\n🧪 Testing Resend API Configuration...")
    
    import requests
    
    api_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('RESEND_FROM_EMAIL', 'SmartProBono <onboarding@resend.dev>')
    to_email = 'bferrell514@gmail.com'
    
    if not api_key:
        print("❌ RESEND_API_KEY not set. Please set your Resend API key.")
        return False
    
    try:
        url = 'https://api.resend.com/emails'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'from': from_email,
            'to': [to_email],
            'subject': 'SmartProBono Email Test (Resend)',
            'html': f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>SmartProBono Email Test</h2>
                <p>This is a test email from your SmartProBono contact form system.</p>
                <p>If you receive this email, your Resend API configuration is working correctly!</p>
                <div style="background: #f0f0f0; padding: 15px; margin: 20px 0;">
                    <h3>Test Details:</h3>
                    <ul>
                        <li><strong>From:</strong> {from_email}</li>
                        <li><strong>To:</strong> {to_email}</li>
                        <li><strong>Sent via:</strong> Resend API</li>
                        <li><strong>Timestamp:</strong> {os.popen('date').read().strip()}</li>
                    </ul>
                </div>
                <p>Best regards,<br>SmartProBono System</p>
            </body>
            </html>
            """,
            'text': f"""
SmartProBono Email Test

This is a test email from your SmartProBono contact form system.

If you receive this email, your Resend API configuration is working correctly!

Test Details:
- From: {from_email}
- To: {to_email}
- Sent via: Resend API
- Timestamp: {os.popen('date').read().strip()}

Best regards,
SmartProBono System
            """
        }
        
        print(f"📧 Sending test email via Resend API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Resend API test successful! Check your Gmail inbox.")
            return True
        else:
            print(f"❌ Resend API test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Resend API test failed: {str(e)}")
        return False

def main():
    """Main test function."""
    print("🚀 SmartProBono Email Configuration Test")
    print("=" * 50)
    
    # Test both configurations
    gmail_success = test_gmail_smtp()
    resend_success = test_resend_api()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Gmail SMTP: {'✅ Working' if gmail_success else '❌ Failed'}")
    print(f"Resend API: {'✅ Working' if resend_success else '❌ Failed'}")
    
    if gmail_success or resend_success:
        print("\n🎉 At least one email method is working!")
        print("Your contact form should work correctly.")
    else:
        print("\n⚠️  No email methods are working.")
        print("Please check your configuration and try again.")
    
    print("\n📝 Next Steps:")
    if gmail_success:
        print("1. Use Gmail SMTP configuration for your contact form")
        print("2. Forward important emails to bferrell@smartprobono.org")
    elif resend_success:
        print("1. Use Resend API configuration for your contact form")
        print("2. Forward important emails to bferrell@smartprobono.org")
    else:
        print("1. Fix your email configuration")
        print("2. Check the ZOHO_EMAIL_SETUP.md guide")
    
    print("3. Test your contact form on the website")
    print("4. Check your Gmail inbox for test emails")
    print("5. Forward important emails to bferrell@smartprobono.org")

if __name__ == "__main__":
    main()
