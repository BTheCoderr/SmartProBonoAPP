#!/usr/bin/env python
"""
Setup script for Cloudinary resources.

This script initializes the required Cloudinary folders and upload presets
for the SmartProBono application.
"""
import os
import sys
import argparse
import cloudinary
import cloudinary.api
import cloudinary.uploader

# Add parent directory to path so we can import from backend package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config.cloudinary_config import validate_config, get_cloudinary_config, DEFAULT_FOLDERS

def initialize_cloudinary():
    """Initialize Cloudinary with configuration."""
    config = get_cloudinary_config()
    cloudinary.config(
        cloud_name=config['cloud_name'],
        api_key=config['api_key'],
        api_secret=config['api_secret']
    )

def test_cloudinary_connection():
    """Test the Cloudinary connection by getting account info."""
    try:
        info = cloudinary.api.account_info()
        print(f"✅ Successfully connected to Cloudinary account: {info.get('account', {}).get('cloud_name')}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Cloudinary: {str(e)}")
        return False

def create_folders(folders):
    """Create folder structure in Cloudinary."""
    created = []
    for folder in folders:
        try:
            result = cloudinary.api.create_folder(folder)
            if result.get('success', False):
                created.append(folder)
                print(f"✅ Created folder: {folder}")
            else:
                print(f"⚠️ Failed to create folder: {folder}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"ℹ️ Folder already exists: {folder}")
            else:
                print(f"❌ Error creating folder {folder}: {str(e)}")
    
    return created

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Setup Cloudinary resources for SmartProBono")
    parser.add_argument('--test-only', action='store_true', help='Only test connectivity, don\'t set up resources')
    args = parser.parse_args()
    
    try:
        # Validate configuration
        validate_config()
        
        # Initialize Cloudinary
        initialize_cloudinary()
        
        # Test connection
        if not test_cloudinary_connection():
            print("Failed to connect to Cloudinary. Check your credentials and try again.")
            return 1
        
        if args.test_only:
            print("Test only mode - Cloudinary connection successful")
            return 0
            
        # Set up folder structure
        print("\nSetting up folder structure...")
        folder_paths = []
        for folder_name in DEFAULT_FOLDERS.keys():
            folder_paths.append(folder_name)
                
        create_folders(folder_paths)
        
        print("\n✅ Cloudinary setup completed successfully")
        return 0
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 