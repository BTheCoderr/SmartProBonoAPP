#!/usr/bin/env python
"""
Test script for email functionality in SmartProBono
"""
import os
import sys
import argparse
from datetime import datetime
from services.email_service import EmailService, send_confirmation_email_flask, send_welcome_email_flask, send_subscription_confirmation

def setup_test_env():
    """Set up test environment variables if not already set"""
    # Only set these if they're not already set
    if not os.environ.get('EMAIL_HOST'):
        print("Setting up test environment variables...")
        os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
        os.environ['EMAIL_PORT'] = '587'
        os.environ['EMAIL_FROM'] = 'test@smartprobono.org'
        os.environ['EMAIL_FROM_NAME'] = 'SmartProBono Test'
        os.environ['APP_URL'] = 'http://localhost:3000'
        
        # Note: We don't set username/password to use the logging fallback
        # This prevents accidentally sending real emails during testing
        print("Email credentials NOT set - emails will be logged but not sent")

def test_basic_email(to_email):
    """Test basic email sending"""
    print(f"Testing basic email to {to_email}...")
    result = EmailService.send_email(
        to_email=to_email,
        subject="SmartProBono Test Email",
        html_content=f"""
        <html>
            <body>
                <h1>Test Email</h1>
                <p>This is a test email from SmartProBono sent at {datetime.now()}.</p>
            </body>
        </html>
        """,
        text_content=f"Test email from SmartProBono sent at {datetime.now()}."
    )
    print(f"Result: {'Success' if result else 'Failed'}")
    return result

def test_confirmation_email(to_email):
    """Test beta confirmation email"""
    print(f"Testing confirmation email to {to_email}...")
    mock_token = "test_token_12345"
    result = send_confirmation_email_flask(to_email, mock_token)
    print(f"Result: {'Success' if result else 'Failed'}")
    return result

def test_welcome_email(to_email):
    """Test beta welcome email"""
    print(f"Testing welcome email to {to_email}...")
    result = send_welcome_email_flask(to_email)
    print(f"Result: {'Success' if result else 'Failed'}")
    return result

def test_subscription_email(to_email):
    """Test subscription confirmation email"""
    print(f"Testing subscription email to {to_email}...")
    preferences = {
        'productUpdates': True,
        'legalNews': False,
        'tips': True
    }
    result = send_subscription_confirmation(to_email, preferences)
    print(f"Result: {'Success' if result else 'Failed'}")
    return result

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test SmartProBono email functionality')
    parser.add_argument('email', help='Email address to send test emails to')
    parser.add_argument('--all', action='store_true', help='Run all email tests')
    parser.add_argument('--basic', action='store_true', help='Test basic email')
    parser.add_argument('--confirmation', action='store_true', help='Test confirmation email')
    parser.add_argument('--welcome', action='store_true', help='Test welcome email')
    parser.add_argument('--subscription', action='store_true', help='Test subscription email')
    
    args = parser.parse_args()
    
    if not args.email:
        print("Email address is required")
        sys.exit(1)
        
    setup_test_env()
    
    # If no specific test is selected or --all is used, run all tests
    run_all = args.all or not any([args.basic, args.confirmation, args.welcome, args.subscription])
    
    if run_all or args.basic:
        test_basic_email(args.email)
        
    if run_all or args.confirmation:
        test_confirmation_email(args.email)
        
    if run_all or args.welcome:
        test_welcome_email(args.email)
        
    if run_all or args.subscription:
        test_subscription_email(args.email)
        
    print("Testing complete!")

if __name__ == "__main__":
    main() 