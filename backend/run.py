#!/usr/bin/env python3
"""
SmartProBono Application Runner
-------------------------------
This script starts the SmartProBono backend application with proper configuration.
"""
import os
import sys
import argparse
from app import create_app
from flask_migrate import Migrate
from config.database import db

def setup_template_directories():
    """Ensure template directories exist"""
    needed_dirs = [
        'backend/templates/definitions',
        'backend/templates/fonts',
        'backend/templates/output',
    ]
    
    for directory in needed_dirs:
        os.makedirs(directory, exist_ok=True)
    
    print(f"Template directories verified.")

def create_migration_directories():
    """Ensure migration directories exist"""
    if not os.path.exists('backend/migrations'):
        print("Creating migrations directory...")
        os.makedirs('backend/migrations/versions', exist_ok=True)
    
    print("Migration directories verified.")

def setup_parser():
    """Setup command-line argument parser"""
    parser = argparse.ArgumentParser(description='Run the SmartProBono application')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the application on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--setup-db', action='store_true', help='Setup the database before running')
    parser.add_argument('--migrate', action='store_true', help='Run migrations before starting')
    
    return parser

def main():
    """Main entry point for running the application"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Create Flask application
    app = create_app()
    
    # Setup Flask-Migrate
    migrate = Migrate(app, db)
    
    # Ensure template directories exist
    setup_template_directories()
    
    # Create migration directories if needed
    create_migration_directories()
    
    # Setup database if requested
    if args.setup_db:
        with app.app_context():
            from scripts.setup_postgres import setup_postgres
            setup_postgres()
    
    # Run migrations if requested
    if args.migrate:
        with app.app_context():
            from flask_migrate import upgrade
            upgrade()
    
    # Check for template and font installation
    if not os.path.exists('backend/templates/fonts/NotoSans-Regular.ttf'):
        print("Note: Font files are not installed. Run scripts/setup_fonts.py to install required fonts.")
    
    if not os.listdir('backend/templates/definitions'):
        print("Note: No document templates are installed. Check templates/definitions directory.")
    
    # Run the application
    print(f"Starting SmartProBono on {args.host}:{args.port}...")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main() 