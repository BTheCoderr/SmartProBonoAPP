#!/usr/bin/env python3
"""
Fix all models to add extend_existing=True
"""
import os
import re

def fix_model_file(file_path):
    """Add extend_existing=True to all model classes in a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match class definitions with __tablename__
    pattern = r'(class \w+\(db\.Model\):.*?__tablename__ = [\'"][^\'"]+[\'"])(\n)'
    
    def replace_func(match):
        class_def = match.group(1)
        newline = match.group(2)
        # Check if __table_args__ already exists
        if '__table_args__' not in class_def:
            return class_def + newline + "    __table_args__ = {'extend_existing': True}" + newline
        return match.group(0)
    
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"✅ Fixed {file_path}")
        return True
    else:
        print(f"ℹ️  No changes needed for {file_path}")
        return False

def main():
    """Fix all model files"""
    models_dir = "backend/models"
    model_files = [
        "audit.py",
        "case.py", 
        "client_intake.py",
        "document.py",
        "notification.py",
        "payment.py",
        "user.py"
    ]
    
    print("🔧 Fixing all model files...")
    print("=" * 50)
    
    fixed_count = 0
    for model_file in model_files:
        file_path = os.path.join(models_dir, model_file)
        if os.path.exists(file_path):
            if fix_model_file(file_path):
                fixed_count += 1
        else:
            print(f"❌ File not found: {file_path}")
    
    print("=" * 50)
    print(f"🎯 Fixed {fixed_count} model files")

if __name__ == "__main__":
    main()
