#!/bin/bash
# Run the API with email configuration on an alternative port
source ./load_email_config.sh
export PORT=8081
/Users/baheemferrell/Desktop/Apps/SmartProBono-main/venv/bin/python fix_api.py 