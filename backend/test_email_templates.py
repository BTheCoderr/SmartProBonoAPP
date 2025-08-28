#!/usr/bin/env python3
"""
Email template testing script for SmartProBono.
Renders email templates and saves them as HTML files for preview.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

try:
    from utils.email_templates import (
        render_welcome_email, 
        render_password_reset_email, 
        render_document_share_email,
        render_form_submission_email
    )
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.email_templates import (
        render_welcome_email, 
        render_password_reset_email, 
        render_document_share_email,
        render_form_submission_email
    )

def save_html_template(html_content, filename):
    """Save HTML content to file."""
    output_dir = Path("./email_templates")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / filename
    with open(output_file, "w") as f:
        f.write(html_content)
    
    return output_file.absolute()

def test_welcome_email():
    """Test welcome email template."""
    print("Testing welcome email template...")
    html_content = render_welcome_email(
        name="John Doe",
        login_url="https://smartprobono.org/login"
    )
    
    filename = f"welcome_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_file = save_html_template(html_content, filename)
    
    print(f"Welcome email template saved to {output_file}")
    return output_file

def test_password_reset_email():
    """Test password reset email template."""
    print("Testing password reset email template...")
    html_content = render_password_reset_email(
        name="John Doe",
        reset_url="https://smartprobono.org/reset-password?token=abc123"
    )
    
    filename = f"password_reset_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_file = save_html_template(html_content, filename)
    
    print(f"Password reset email template saved to {output_file}")
    return output_file

def test_document_share_email():
    """Test document share email template."""
    print("Testing document share email template...")
    html_content = render_document_share_email(
        sender_name="Jane Smith",
        document_title="Contract Agreement",
        document_description="Legal contract for client review",
        document_url="https://smartprobono.org/documents/123",
        message="Please review this document at your earliest convenience."
    )
    
    filename = f"document_share_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_file = save_html_template(html_content, filename)
    
    print(f"Document share email template saved to {output_file}")
    return output_file

def test_form_submission_email():
    """Test form submission email template."""
    print("Testing form submission email template...")
    html_content = render_form_submission_email(
        name="John Doe",
        form_type="Client Intake Form",
        reference_id="FORM-12345",
        submission_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status="Submitted",
        status_url="https://smartprobono.org/forms/12345/status"
    )
    
    filename = f"form_submission_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_file = save_html_template(html_content, filename)
    
    print(f"Form submission email template saved to {output_file}")
    return output_file

def main():
    """Main function to run the email template tests."""
    parser = argparse.ArgumentParser(description="Test email templates for SmartProBono.")
    parser.add_argument("--all", action="store_true", help="Test all email templates")
    parser.add_argument("--welcome", action="store_true", help="Test welcome email template")
    parser.add_argument("--reset", action="store_true", help="Test password reset email template")
    parser.add_argument("--share", action="store_true", help="Test document share email template")
    parser.add_argument("--form", action="store_true", help="Test form submission email template")
    args = parser.parse_args()

    # If no specific template is selected, test all
    if not (args.welcome or args.reset or args.share or args.form):
        args.all = True
    
    generated_files = []
    
    print("\n=== SmartProBono Email Template Test ===")
    
    if args.all or args.welcome:
        generated_files.append(test_welcome_email())
    
    if args.all or args.reset:
        generated_files.append(test_password_reset_email())
    
    if args.all or args.share:
        generated_files.append(test_document_share_email())
    
    if args.all or args.form:
        generated_files.append(test_form_submission_email())
    
    print("\n=== Email Template Test Summary ===")
    print(f"Generated {len(generated_files)} template files:")
    for file in generated_files:
        print(f"- {file}")
    print("\nOpen these files in a web browser to preview the email templates.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 