#!/bin/bash

# SmartProBono Email Configuration Script
echo "=========================================================="
echo "SmartProBono Email Configuration"
echo "=========================================================="
echo "This script helps you set up email notifications for"
echo "your SmartProBono instance."
echo ""

# Define the config file
CONFIG_FILE=".env.email"

# Welcome message
echo "We need to configure your email settings to send confirmation"
echo "emails to users and notifications to yourself."
echo ""

# Ask about email server
read -p "SMTP Server [smtp.zoho.com]: " SMTP_SERVER
SMTP_SERVER=${SMTP_SERVER:-smtp.zoho.com}

read -p "SMTP Port [587]: " SMTP_PORT
SMTP_PORT=${SMTP_PORT:-587}

read -p "Email address to use (recommended: info@smartprobono.org): " SMTP_USERNAME
if [[ -z "$SMTP_USERNAME" ]]; then
  echo "Email address is required."
  exit 1
fi

# Get password securely
read -s -p "Email password (hidden for security): " SMTP_PASSWORD
echo ""
if [[ -z "$SMTP_PASSWORD" ]]; then
  echo "Password is required for sending emails."
  exit 1
fi

# Verify if using Zoho
if [[ "$SMTP_SERVER" == "smtp.zoho.com" ]]; then
  echo ""
  echo "IMPORTANT: For Zoho Mail accounts, ensure you have:"
  echo "1. Verified your domain ownership in Zoho"
  echo "2. Set up the appropriate MX records for your domain"
  echo "3. Configured and verified DKIM in Zoho Mail Admin Panel"
  echo "   (This improves email deliverability and prevents emails from being marked as spam)"
  echo ""
  read -p "Have you completed the domain verification and DKIM setup in Zoho? (y/n): " zoho_verified
  if [[ "$zoho_verified" != "y" && "$zoho_verified" != "Y" ]]; then
    echo "It's recommended to complete domain verification and DKIM setup first."
    echo "You can continue, but email deliverability may be impacted."
    read -p "Continue anyway? (y/n): " continue_anyway
    if [[ "$continue_anyway" != "y" && "$continue_anyway" != "Y" ]]; then
      exit 1
    fi
  fi
fi

# Gmail option remains as fallback
if [[ "$SMTP_SERVER" == "smtp.gmail.com" ]]; then
  echo ""
  echo "IMPORTANT: For Gmail accounts, you need to:"
  echo "1. Enable 2-Step Verification on your Google account"
  echo "2. Create an App Password for this application"
  echo "   (Go to your Google Account > Security > App passwords)"
  echo ""
  read -p "Have you set up an App Password for this Gmail account? (y/n): " gmail_verified
  if [[ "$gmail_verified" != "y" && "$gmail_verified" != "Y" ]]; then
    echo "Please set up an App Password first, then run this script again."
    exit 1
  fi
fi

# Create or update config file
echo "Writing configuration to $CONFIG_FILE..."
cat > "$CONFIG_FILE" << EOL
# SmartProBono Email Configuration
SMTP_SERVER=$SMTP_SERVER
SMTP_PORT=$SMTP_PORT
SMTP_USERNAME=$SMTP_USERNAME
SMTP_PASSWORD=$SMTP_PASSWORD
EOL

# Make file only readable by the owner for security
chmod 600 "$CONFIG_FILE"

# Create a script to export these variables
cat > "load_email_config.sh" << EOL
#!/bin/bash
# Load SmartProBono email configuration
export SMTP_SERVER=$SMTP_SERVER
export SMTP_PORT=$SMTP_PORT
export SMTP_USERNAME=$SMTP_USERNAME
export SMTP_PASSWORD=$SMTP_PASSWORD
EOL

chmod +x "load_email_config.sh"

echo ""
echo "Configuration saved successfully!"
echo ""
echo "To use your email configuration when running the API:"
echo ""
echo "Option 1: Source the configuration file:"
echo "  source ./load_email_config.sh"
echo "  python fix_api.py"
echo ""
echo "Option 2: Run with configuration in one command:"
echo "  ./run_with_email.sh"
echo ""

# Create the run_with_email.sh script
cat > "run_with_email.sh" << EOL
#!/bin/bash
# Run the API with email configuration
source ./load_email_config.sh
python fix_api.py
EOL

chmod +x "run_with_email.sh"

echo "Done! Your email configuration is ready to use." 