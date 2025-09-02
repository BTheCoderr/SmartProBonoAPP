#!/usr/bin/env python3
"""
Script to check for invalid Material-UI icon imports across the frontend
"""

import os
import re
import subprocess
import json
from pathlib import Path

def get_available_mui_icons():
    """Get list of available Material-UI icons by checking the package"""
    try:
        # Try to get icons from node_modules
        result = subprocess.run([
            'node', '-e', 
            'console.log(JSON.stringify(Object.keys(require("@mui/icons-material"))))'
        ], capture_output=True, text=True, cwd='frontend')
        
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            print(f"Error getting MUI icons: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def find_icon_imports(file_path):
    """Find all Material-UI icon imports in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find import statements from @mui/icons-material
        import_pattern = r"import\s*\{([^}]+)\}\s*from\s*['\"]@mui/icons-material['\"]"
        matches = re.findall(import_pattern, content, re.MULTILINE)
        
        icons = []
        for match in matches:
            # Split by comma and clean up
            icon_list = [icon.strip().split(' as ')[0].strip() for icon in match.split(',')]
            icons.extend(icon_list)
        
        return icons
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def check_all_files():
    """Check all frontend files for invalid icon imports"""
    frontend_path = Path('frontend/src')
    if not frontend_path.exists():
        print("Frontend directory not found!")
        return
    
    print("🔍 Checking for invalid Material-UI icon imports...")
    print("=" * 60)
    
    # Get available icons
    available_icons = get_available_mui_icons()
    if not available_icons:
        print("❌ Could not get list of available icons. Make sure @mui/icons-material is installed.")
        return
    
    print(f"✅ Found {len(available_icons)} available Material-UI icons")
    print()
    
    # Find all JS/JSX/TS/TSX files
    files_to_check = []
    for ext in ['**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx']:
        files_to_check.extend(frontend_path.glob(ext))
    
    invalid_imports = []
    
    for file_path in files_to_check:
        icons = find_icon_imports(file_path)
        if icons:
            invalid_in_file = []
            for icon in icons:
                if icon not in available_icons:
                    invalid_in_file.append(icon)
            
            if invalid_in_file:
                invalid_imports.append({
                    'file': str(file_path),
                    'invalid_icons': invalid_in_file
                })
    
    # Report results
    if invalid_imports:
        print("❌ Found invalid icon imports:")
        print()
        for item in invalid_imports:
            print(f"📁 {item['file']}")
            for icon in item['invalid_icons']:
                print(f"   ❌ {icon}")
                
                # Suggest similar icons
                similar = [available for available in available_icons 
                          if icon.lower() in available.lower() or available.lower() in icon.lower()]
                if similar:
                    print(f"   💡 Similar: {', '.join(similar[:3])}")
            print()
    else:
        print("✅ No invalid icon imports found!")
    
    return invalid_imports

if __name__ == "__main__":
    check_all_files()
