#!/usr/bin/env python3
"""
Simple email test using Resend with a verified domain.
"""

import requests
import os

def test_resend_simple():
    """Test Resend with a simple approach."""
    print("🧪 Testing Resend API with verified domain...")
    
    api_key = os.getenv('RESEND_API_KEY')
    if not api_key:
        print("❌ RESEND_API_KEY not set")
        return False
    
    # Use Resend's default verified domain
    url = 'https://api.resend.com/emails'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'from': 'SmartProBono <onboarding@resend.dev>',
        'to': ['bferrell514@gmail.com'],
        'subject': 'SmartProBono Contact Form Test',
        'html': '''
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #0F3D5E;">SmartProBono Contact Form Test</h2>
            <p>This is a test email from your SmartProBono contact form system.</p>
            <p>If you receive this email, your Resend configuration is working correctly!</p>
            <div style="background: #f0f0f0; padding: 15px; margin: 20px 0;">
                <h3>Test Details:</h3>
                <ul>
                    <li><strong>From:</strong> SmartProBono (via Resend)</li>
                    <li><strong>To:</strong> bferrell514@gmail.com</li>
                    <li><strong>Sent via:</strong> Resend API</li>
                    <li><strong>Status:</strong> Working!</li>
                </ul>
            </div>
            <p>Best regards,<br>SmartProBono System</p>
        </body>
        </html>
        ''',
        'text': '''
SmartProBono Contact Form Test

This is a test email from your SmartProBono contact form system.

If you receive this email, your Resend configuration is working correctly!

Test Details:
- From: SmartProBono (via Resend)
- To: bferrell514@gmail.com
- Sent via: Resend API
- Status: Working!

Best regards,
SmartProBono System
        '''
    }
    
    try:
        print("📧 Sending test email via Resend API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Resend API test successful! Check your Gmail inbox.")
            print("📧 Email sent to: bferrell514@gmail.com")
            return True
        else:
            print(f"❌ Resend API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Resend API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Resend Email Test")
    print("=" * 30)
    
    success = test_resend_simple()
    
    if success:
        print("\n🎉 Email system is working!")
        print("📝 Next steps:")
        print("1. Test your contact form on the website")
        print("2. Check your Gmail inbox")
        print("3. Forward important emails to bferrell@smartprobono.org")
    else:
        print("\n⚠️ Email system needs configuration")
        print("📝 Check your Resend API key and try again")
