#!/bin/bash

echo "SmartProBono PostgreSQL Setup Script"
echo "==================================="
echo

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL first:"
    echo "For MacOS: brew install postgresql"
    echo "For Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    echo "For other systems, visit: https://www.postgresql.org/download/"
    exit 1
fi

echo "PostgreSQL is installed."
echo

# Check if PostgreSQL service is running
if ! pg_isready &> /dev/null; then
    echo "PostgreSQL service is not running. Please start it:"
    echo "For MacOS: brew services start postgresql"
    echo "For Ubuntu: sudo service postgresql start"
    exit 1
fi

echo "PostgreSQL service is running."
echo

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Initialize PostgreSQL database
echo "Initializing PostgreSQL database..."
python scripts/init_postgres.py

# Create database tables
echo "Creating database tables..."
export FLASK_APP=app.py
flask db upgrade

# Seed initial data
echo "Seeding initial data..."
python init_db.py

echo
echo "Setup complete! Make sure to:"
echo "1. Update your .env file with the correct DATABASE_URL"
echo "2. Update your production environment variables"
echo "3. Restart your application" 