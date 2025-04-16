#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install
npm run build
cd ..

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    # Generate secure keys
    echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
    echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env
fi

# Initialize database
echo "Initializing database..."
cd backend
python3 -c "from models.database import db, init_db; from app import create_app; app = create_app(); init_db(app)"

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:5002 \
         --workers 4 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --capture-output \
         --enable-stdio-inheritance \
         "app:create_app()"

echo "Deployment complete!" 