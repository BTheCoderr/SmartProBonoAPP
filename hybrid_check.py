#!/usr/bin/env python3
"""
Hybrid Storage System Check for SmartProBono
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create cache directory
CACHE_DIR = Path(os.path.expanduser("~/.smartprobono/cache"))
CACHE_DIR.mkdir(exist_ok=True, parents=True)

def check_github_config():
    """Check GitHub configuration and connection."""
    github_repo = os.environ.get("GITHUB_REPO", "SmartProBonoProject/SmartProBono")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    if not github_repo:
        print("❌ GitHub repository not configured.")
        return False
        
    print(f"✓ GitHub Repository: {github_repo}")
    
    # Test API connection
    try:
        import requests
        headers = {"Accept": "application/vnd.github.v3+json"}
        if github_token:
            headers["Authorization"] = f"token {github_token}"
            
        url = f"https://api.github.com/repos/{github_repo}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        repo_info = response.json()
        print(f"✓ Connected to GitHub repository: {repo_info['full_name']}")
        print(f"✓ Description: {repo_info.get('description', 'None')}")
        return True
    except Exception as e:
        print(f"❌ Error connecting to GitHub: {str(e)}")
        return False

def check_cloudinary_config():
    """Check if Cloudinary is properly configured."""
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    
    if not cloud_name:
        print("❌ Cloudinary cloud name not configured")
        return False
        
    if not api_key:
        print("❌ Cloudinary API key not configured")
        return False
        
    if not api_secret:
        print("❌ Cloudinary API secret not configured")
        return False
    
    print(f"✓ Cloudinary configured with cloud name: {cloud_name}")
    
    # We would test the connection here, but don't want to import cloudinary
    # just for a configuration check
    return True

def check_flask_demo():
    """Check if the Flask demo file exists."""
    flask_demo = os.path.join(os.getcwd(), "simple_resource_demo.py")
    if os.path.exists(flask_demo):
        print(f"✓ Found Flask demo at: {flask_demo}")
        return True
    else:
        print(f"❌ Flask demo not found at: {flask_demo}")
        return False

if __name__ == "__main__":
    print("SmartProBono Hybrid Storage System Check\n")
    
    # Check environment variables
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        print(f"✓ Found .env file at: {env_path}")
    else:
        print(f"❌ No .env file found at: {env_path}")
    
    print("\nChecking GitHub Configuration:")
    print("-" * 30)
    check_github_config()
    
    print("\nChecking Cloudinary Configuration:")
    print("-" * 30)
    check_cloudinary_config()
    
    print("\nChecking Flask Demo App:")
    print("-" * 30)
    check_flask_demo()
    
    print("\nTo run the full hybrid storage system:")
    print("1. Make sure your .env file has proper GitHub and Cloudinary credentials")
    print("2. Run 'python simple_resource_demo.py' to start the Flask server")
    print("3. Access the API endpoints as described in HYBRID_STORAGE_README.md") 