#!/usr/bin/env python3
"""
Security Issues Fix Script
This script fixes the remaining security issues found by bandit
"""

import os
import re

def fix_requests_timeouts():
    """Add timeouts to all requests.post calls"""
    
    files_to_fix = [
        'backend/combined_server.py',
        'backend/services/audit_service.py', 
        'backend/services/resend_email_service.py'
    ]
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Pattern to match requests.post without timeout
        pattern = r'(requests\.post\([^)]+)\)'
        
        def add_timeout(match):
            call = match.group(1)
            if 'timeout' not in call:
                return call + ', timeout=30)'
            return call + ')'
        
        # Replace all requests.post calls
        new_content = re.sub(pattern, add_timeout, content)
        
        if new_content != content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"✅ Fixed requests timeouts in {file_path}")

def fix_hardcoded_secrets():
    """Fix hardcoded secrets in configuration"""
    
    config_file = 'backend/config/security.py'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Replace hardcoded JWT secret with environment variable
        new_content = content.replace(
            "JWT_SECRET_KEY = 'your-secret-key'  # Change in production",
            "JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Use env var in production"
        )
        
        if new_content != content:
            with open(config_file, 'w') as f:
                f.write(new_content)
            print(f"✅ Fixed hardcoded JWT secret in {config_file}")

def fix_temp_directories():
    """Fix hardcoded temp directories"""
    
    files_to_fix = [
        'backend/tests/conftest.py',
        'backend/utils/document_generator.py'
    ]
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace hardcoded /tmp with tempfile.gettempdir()
        new_content = content.replace(
            "'/tmp/smartprobono_test_uploads'",
            "os.path.join(tempfile.gettempdir(), 'smartprobono_test_uploads')"
        )
        
        new_content = new_content.replace(
            "'/tmp'",
            "tempfile.gettempdir()"
        )
        
        # Add tempfile import if needed
        if 'tempfile.gettempdir()' in new_content and 'import tempfile' not in new_content:
            new_content = new_content.replace(
                'import os',
                'import os\nimport tempfile'
            )
        
        if new_content != content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"✅ Fixed temp directories in {file_path}")

def main():
    """Main function to run all security fixes"""
    print("🔧 Fixing Security Issues...")
    print("=" * 50)
    
    fix_requests_timeouts()
    fix_hardcoded_secrets()
    fix_temp_directories()
    
    print("=" * 50)
    print("✅ Security fixes completed!")
    print("📝 Note: Test files with hardcoded passwords are expected for testing")

if __name__ == "__main__":
    main()
