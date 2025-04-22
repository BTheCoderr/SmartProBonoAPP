#!/usr/bin/env python
"""
Script to setup Cloudinary folders and presets needed for SmartProBono
"""
import argparse
import os
import sys
import cloudinary
import cloudinary.api
from dotenv import load_dotenv

# Add necessary directories to the path so we can import from backend
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(backend_dir)

# Constants for Cloudinary setup
CASE_FOLDER = 'smartprobono/case_documents'
TEMPLATE_FOLDER = 'smartprobono/document_templates'
USER_FOLDER = 'smartprobono/user_uploads'
FOLDERS = [CASE_FOLDER, TEMPLATE_FOLDER, USER_FOLDER]

DOCUMENT_UPLOAD_PRESET = 'document_uploads'
TEMPLATE_UPLOAD_PRESET = 'template_uploads'
USER_UPLOAD_PRESET = 'user_uploads'

PRESETS = {
    DOCUMENT_UPLOAD_PRESET: {
        'folder': CASE_FOLDER,
        'allowed_formats': ['pdf', 'doc', 'docx'],
        'resource_type': 'raw'
    },
    TEMPLATE_UPLOAD_PRESET: {
        'folder': TEMPLATE_FOLDER,
        'allowed_formats': ['doc', 'docx', 'txt', 'html'],
        'resource_type': 'raw'
    },
    USER_UPLOAD_PRESET: {
        'folder': USER_FOLDER,
        'allowed_formats': ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'],
        'resource_type': 'auto'
    }
}

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Check for required environment variables
    required_vars = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

def validate_configuration():
    """Validate Cloudinary credentials and connection"""
    try:
        # Try to ping Cloudinary
        result = cloudinary.api.ping()
        print(f"Cloudinary connection successful: {result}")
        return True
    except Exception as e:
        print(f"Error connecting to Cloudinary: {e}")
        return False

def ensure_folder_exists(folder_path):
    """Ensure a folder exists in Cloudinary"""
    try:
        print(f"Checking if folder exists: {folder_path}")
        # Try to get folder info
        cloudinary.api.root_folders()
        
        # Create folder if it doesn't exist
        folder_parts = folder_path.split('/')
        current_path = ''
        
        for part in folder_parts:
            if current_path:
                current_path = f"{current_path}/{part}"
            else:
                current_path = part
                
            try:
                # Check if this folder level exists
                cloudinary.api.sub_folders(current_path)
            except Exception:
                # Create the folder if it doesn't exist
                print(f"Creating folder: {current_path}")
                cloudinary.api.create_folder(current_path)
        
        return True
    except Exception as e:
        print(f"Error ensuring folder exists: {e}")
        return False

def setup_upload_preset(name, config):
    """Set up an upload preset in Cloudinary"""
    try:
        print(f"Setting up upload preset: {name}")
        # Check if preset already exists
        presets = cloudinary.api.upload_presets()
        preset_exists = any(preset['name'] == name for preset in presets['presets'])
        
        preset_config = {
            'name': name,
            'folder': config['folder'],
            'allowed_formats': config['allowed_formats'],
            'resource_type': config['resource_type'],
            'unsigned': True
        }
        
        if preset_exists:
            print(f"Updating existing preset: {name}")
            cloudinary.api.update_upload_preset(**preset_config)
        else:
            print(f"Creating new preset: {name}")
            cloudinary.api.create_upload_preset(**preset_config)
            
        return True
    except Exception as e:
        print(f"Error setting up upload preset {name}: {e}")
        return False

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Setup Cloudinary for SmartProBono')
    parser.add_argument('--test-only', action='store_true', help='Only test the connection, don\'t set up resources')
    args = parser.parse_args()
    
    # Load environment variables
    load_environment()
    
    # Validate configuration
    if not validate_configuration():
        print("Failed to validate Cloudinary configuration")
        sys.exit(1)
        
    if args.test_only:
        print("Configuration tested successfully")
        sys.exit(0)
    
    # Setup folders
    for folder in FOLDERS:
        if not ensure_folder_exists(folder):
            print(f"Failed to create folder: {folder}")
            sys.exit(1)
    
    # Setup upload presets
    for preset_name, preset_config in PRESETS.items():
        if not setup_upload_preset(preset_name, preset_config):
            print(f"Failed to setup upload preset: {preset_name}")
            sys.exit(1)
    
    print("Cloudinary setup completed successfully")

if __name__ == "__main__":
    main() 