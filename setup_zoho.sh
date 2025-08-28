#!/bin/bash

# SmartProBono Zoho Email Configuration Script
echo "=========================================================="
echo "SmartProBono Zoho Email Configuration"
echo "=========================================================="
echo "This script will help you set up your Zoho email account."
echo ""

# Get the password
read -s -p "Enter the password for info@smartprobono.org: " EMAIL_PASSWORD
echo ""

if [[ -z "$EMAIL_PASSWORD" ]]; then
  echo "Password is required. Please run the script again."
  exit 1
fi

# Create or update config file
CONFIG_FILE=".env.email"
echo "Writing configuration to $CONFIG_FILE..."

cat > "$CONFIG_FILE" << EOL
# SmartProBono Email Configuration
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=587
SMTP_USERNAME=info@smartprobono.org
SMTP_PASSWORD=$EMAIL_PASSWORD
EOL

# Make file only readable by the owner for security
chmod 600 "$CONFIG_FILE"

# Update the load_email_config.sh script
cat > "load_email_config.sh" << EOL
#!/bin/bash
# Load SmartProBono email configuration
export SMTP_SERVER=smtp.zoho.com
export SMTP_PORT=587
export SMTP_USERNAME=info@smartprobono.org
export SMTP_PASSWORD='$EMAIL_PASSWORD'
EOL

chmod +x "load_email_config.sh"

echo ""
echo "Configuration saved successfully!"
echo ""
echo "To test the email configuration, run:"
echo "  ./run_email_test.sh your-test-email@example.com"
echo ""
echo "To run the API with email enabled:"
echo "  ./run_with_email.sh"
echo "" 