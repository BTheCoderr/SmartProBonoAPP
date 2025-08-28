#!/bin/bash
# Run the email test script with the correct Python
source ./load_email_config.sh

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 your-test-email@example.com"
    exit 1
fi

/Users/baheemferrell/Desktop/Apps/SmartProBono-main/venv/bin/python test_zoho_email.py "$1" 