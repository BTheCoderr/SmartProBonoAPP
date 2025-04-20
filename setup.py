#!/usr/bin/env python
"""
Setup script for SmartProBono.

This script initializes the database, sets up required services, and loads initial data.
"""

import os
import sys
import logging
import argparse
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("setup")

def run_script(script_path, description, args=None):
    """Run a script and log the result."""
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    logger.info(f"Running {description}...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} failed with exit code {e.returncode}")
        logger.error(f"Stdout: {e.stdout}")
        logger.error(f"Stderr: {e.stderr}")
        return False

def setup_database():
    """Set up the database."""
    logger.info("Setting up database...")
    
    # Run database initialization script
    if not run_script("backend/scripts/init_db.py", "Database initialization"):
        return False
    
    # Run data migration script if it exists
    if os.path.exists("backend/scripts/migrate_data.py"):
        if not run_script("backend/scripts/migrate_data.py", "Data migration"):
            return False
    
    # Load seed data
    if not run_script("backend/scripts/seed_data.py", "Seed data loading"):
        return False
    
    logger.info("Database setup completed successfully")
    return True

def setup_file_storage():
    """Set up file storage."""
    logger.info("Setting up file storage...")
    
    if not run_script("backend/scripts/init_storage.py", "File storage initialization"):
        return False
    
    logger.info("File storage setup completed successfully")
    return True

def setup_document_templates():
    """Set up document templates."""
    logger.info("Setting up document templates...")
    
    if not run_script("backend/scripts/init_document_templates.py", "Document template initialization"):
        return False
    
    logger.info("Document templates setup completed successfully")
    return True

def setup_vector_database():
    """Set up vector database for AI services."""
    logger.info("Setting up vector database...")
    
    if not os.path.exists("backend/scripts/init_vector_db.py"):
        logger.warning("Vector database initialization script not found, skipping...")
        return True
    
    if not run_script("backend/scripts/init_vector_db.py", "Vector database initialization"):
        return False
    
    logger.info("Vector database setup completed successfully")
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Set up SmartProBono application")
    parser.add_argument("--skip-db", action="store_true", help="Skip database setup")
    parser.add_argument("--skip-storage", action="store_true", help="Skip file storage setup")
    parser.add_argument("--skip-templates", action="store_true", help="Skip document templates setup")
    parser.add_argument("--skip-vector-db", action="store_true", help="Skip vector database setup")
    args = parser.parse_args()
    
    success = True
    
    if not args.skip_db:
        if not setup_database():
            logger.error("Database setup failed")
            success = False
    
    if not args.skip_storage and success:
        if not setup_file_storage():
            logger.error("File storage setup failed")
            success = False
    
    if not args.skip_templates and success:
        if not setup_document_templates():
            logger.error("Document templates setup failed")
            success = False
    
    if not args.skip_vector_db and success:
        if not setup_vector_database():
            logger.error("Vector database setup failed")
            success = False
    
    if success:
        logger.info("Setup completed successfully")
        return 0
    else:
        logger.error("Setup failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 