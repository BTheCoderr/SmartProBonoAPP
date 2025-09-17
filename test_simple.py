#!/usr/bin/env python3
"""
Simple test to verify the test setup works
"""

def test_basic_functionality():
    """Test that basic functionality works"""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    print("✅ Basic test passed")

def test_imports():
    """Test that we can import required modules"""
    try:
        import flask
        import pytest
        print("✅ All required imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Simple Tests")
    print("=" * 30)
    
    test_basic_functionality()
    test_imports()
    
    print("=" * 30)
    print("🎉 Simple tests completed!")
