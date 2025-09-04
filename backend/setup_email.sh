#!/bin/bash

# SmartProBono Email Setup Script
# This script helps you set up email configuration securely

echo "🔒 SmartProBono Email Setup"
echo "=========================="
echo ""

# Check if we're in the right directory
if [ ! -f "test_email.py" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

echo "📧 Email Configuration Options:"
echo "1. Gmail SMTP (Recommended)"
echo "2. Resend API (Alternative)"
echo ""
read -p "Choose option (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🔐 Gmail SMTP Setup"
        echo "=================="
        echo ""
        echo "You need to:"
        echo "1. Go to https://myaccount.google.com/security"
        echo "2. Enable 2-Step Verification if not already enabled"
        echo "3. Go to 'App passwords' section"
        echo "4. Generate a new app password for 'Mail'"
        echo "5. Name it 'SmartProBono'"
        echo ""
        read -p "Enter your Gmail app password (16 characters): " -s gmail_password
        echo ""
        
        if [ ${#gmail_password} -eq 16 ]; then
            export MAIL_PASSWORD="$gmail_password"
            echo "✅ Gmail password set successfully"
            echo "🧪 Testing Gmail configuration..."
            python test_email.py
        else
            echo "❌ Invalid password length. Gmail app passwords are 16 characters."
        fi
        ;;
    2)
        echo ""
        echo "🔑 Resend API Setup"
        echo "=================="
        echo ""
        echo "You need to:"
        echo "1. Go to https://resend.com/api-keys"
        echo "2. Copy your API key"
        echo ""
        read -p "Enter your Resend API key: " -s resend_key
        echo ""
        
        if [ ${#resend_key} -gt 10 ]; then
            export RESEND_API_KEY="$resend_key"
            echo "✅ Resend API key set successfully"
            echo "🧪 Testing Resend configuration..."
            python test_email.py
        else
            echo "❌ Invalid API key length."
        fi
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Test your contact form on the website"
echo "2. Check your Gmail inbox for test emails"
echo "3. Forward important emails to bferrell@smartprobono.org"
echo ""
echo "🔒 Security reminder:"
echo "- Never share your app passwords or API keys"
echo "- These credentials are only stored in your current session"
echo "- For production, use environment variables or secure key management"
