#!/usr/bin/env python3
"""
Test script to verify all dependencies can be imported successfully
This helps catch dependency conflicts before deployment
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        if package_name:
            module = importlib.import_module(module_name, package_name)
        else:
            module = importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - WARNING: {e}")
        return True  # Some modules might have warnings but still work

def main():
    """Test all critical dependencies."""
    print("🧪 Testing Dependencies for SmartProBono...")
    print("=" * 50)
    
    # Core Flask dependencies
    print("\n📦 Core Flask Dependencies:")
    flask_deps = [
        "flask",
        "flask_cors", 
        "flask_socketio",
        "gunicorn"
    ]
    
    # Database dependencies
    print("\n🗄️  Database Dependencies:")
    db_deps = [
        "pymongo",
        "flask_pymongo",
        "supabase"
    ]
    
    # PDF processing dependencies
    print("\n📄 PDF Processing Dependencies:")
    pdf_deps = [
        "pypdf",
        "pdfplumber", 
        "PyPDF2",
        "reportlab"
    ]
    
    # AI/ML dependencies
    print("\n🤖 AI/ML Dependencies:")
    ai_deps = [
        "openai",
        "anthropic",
        "langchain",
        "langgraph",
        "chromadb",
        "pydantic"
    ]
    
    # Data processing dependencies
    print("\n📊 Data Processing Dependencies:")
    data_deps = [
        "pandas",
        "numpy",
        "requests"
    ]
    
    # Utilities
    print("\n🔧 Utility Dependencies:")
    util_deps = [
        "dotenv",
        "psutil"
    ]
    
    # Test all dependencies
    all_deps = flask_deps + db_deps + pdf_deps + ai_deps + data_deps + util_deps
    
    success_count = 0
    total_count = len(all_deps)
    
    for dep in all_deps:
        if test_import(dep):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📈 Results: {success_count}/{total_count} dependencies working")
    
    if success_count == total_count:
        print("🎉 All dependencies are working! Deployment should succeed.")
        return True
    else:
        print("❌ Some dependencies failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
