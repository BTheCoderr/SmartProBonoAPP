#!/usr/bin/env python3
"""
Migration script to transition from the old websocket_service.py file to the new modular structure
"""
import os
import sys
import shutil
from datetime import datetime

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def backup_file(file_path):
    """Create a backup of a file with timestamp"""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = f"{file_path}.bak.{timestamp}"
        shutil.copy2(file_path, backup_path)
        print(f"Created backup of {file_path} at {backup_path}")
        return True
    return False

def main():
    """Main migration function"""
    # Get the backend directory (parent of this script's directory)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Set paths
    old_file = os.path.join(backend_dir, 'websocket_service.py')
    websocket_dir = os.path.join(backend_dir, 'websocket')
    
    # Check if the old file exists
    if not os.path.exists(old_file):
        print(f"Error: {old_file} not found!")
        return 1
    
    # Create backup of the old file
    if not backup_file(old_file):
        print("Could not create backup, aborting.")
        return 1
    
    # Ensure the new directories exist
    ensure_directory_exists(websocket_dir)
    ensure_directory_exists(os.path.join(websocket_dir, 'handlers'))
    ensure_directory_exists(os.path.join(websocket_dir, 'services'))
    ensure_directory_exists(os.path.join(websocket_dir, 'utils'))
    
    # Create empty __init__.py files in the directories
    for directory in [
        websocket_dir,
        os.path.join(websocket_dir, 'handlers'),
        os.path.join(websocket_dir, 'services'),
        os.path.join(websocket_dir, 'utils')
    ]:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('"""WebSocket module"""')
            print(f"Created {init_file}")
    
    # Move the old file to the new structure (this is just for reference)
    reference_file = os.path.join(websocket_dir, 'old_websocket_service.py.reference')
    shutil.copy2(old_file, reference_file)
    print(f"Copied old file to {reference_file} for reference")
    
    print("\nMigration complete!")
    print("\nNext steps:")
    print("1. Update your imports from 'websocket_service' to 'websocket'")
    print("2. Modify app.py to use the new WebSocket module")
    print("3. Run tests to ensure everything is working")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 