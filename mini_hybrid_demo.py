#!/usr/bin/env python3
"""
Mini Hybrid Storage Demo for SmartProBono
This minimal script demonstrates fetching templates from GitHub Releases
and uploading/retrieving content from Cloudinary.
"""
import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for resource types
RESOURCE_TYPE_TEMPLATE = "template"         # GitHub Releases
RESOURCE_TYPE_USER_DOCUMENT = "user_document"  # Cloudinary
RESOURCE_TYPE_MEDIA = "media"               # Cloudinary

# GitHub configuration
GITHUB_REPO = os.environ.get("GITHUB_REPO", "SmartProBonoProject/SmartProBono")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Create cache directory
CACHE_DIR = Path(os.path.expanduser("~/.smartprobono/cache"))
CACHE_DIR.mkdir(exist_ok=True, parents=True)

def github_headers():
    """Return headers for GitHub API requests."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def get_latest_github_release():
    """Get the latest GitHub release."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, headers=github_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching latest GitHub release: {e}")
        return None

def list_template_assets():
    """List template assets from the latest GitHub release."""
    release = get_latest_github_release()
    if not release:
        print("No GitHub release found. Check your GITHUB_REPO setting.")
        return []
    
    print(f"Found release: {release['name']} ({release['tag_name']})")
    
    assets = release.get("assets", [])
    templates = []
    
    for asset in assets:
        name = asset["name"]
        if name.endswith(('.txt', '.md', '.pdf', '.docx')):
            templates.append({
                "name": name,
                "size": asset["size"],
                "download_url": asset["browser_download_url"],
                "download_count": asset["download_count"]
            })
    
    return templates

def download_template(template_name, version="latest"):
    """Download a template file from GitHub releases."""
    # Check cache first
    cache_key = f"{version}_{template_name}".replace("/", "_")
    cache_path = CACHE_DIR / cache_key
    
    if cache_path.exists():
        print(f"Using cached template: {cache_path}")
        return str(cache_path)
    
    # Get the release
    release = get_latest_github_release()
    if not release:
        print("Latest release not found")
        return None
    
    version = release["tag_name"]
    
    # Download the template
    download_url = f"https://github.com/{GITHUB_REPO}/releases/download/{version}/{template_name}"
    try:
        print(f"Downloading template from: {download_url}")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(cache_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Template downloaded to: {cache_path}")
        return str(cache_path)
    except Exception as e:
        print(f"Error downloading template {template_name}: {e}")
        return None

def check_cloudinary_config():
    """Check if Cloudinary is properly configured."""
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    
    if not (cloud_name and api_key and api_secret):
        print("Cloudinary not configured. Please set CLOUDINARY_* environment variables.")
        return False
    
    print(f"Cloudinary configured with cloud name: {cloud_name}")
    return True

def show_help():
    """Show usage help."""
    print(f"""
SmartProBono Hybrid Storage Demo

Usage: {sys.argv[0]} <command>

Commands:
  list-templates         List templates from the latest GitHub release
  download <template>    Download a specific template
  check-config           Check Cloudinary and GitHub configuration
  help                   Show this help message
    """)

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        show_help()
        sys.exit(0)
    
    # Process commands
    command = sys.argv[1]
    
    if command == "list-templates":
        templates = list_template_assets()
        if templates:
            print("\nAvailable templates:")
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template['name']} ({template['size']} bytes)")
            print(f"\nTotal: {len(templates)} templates")
        else:
            print("No templates found in the latest release.")
    
    elif command == "download":
        if len(sys.argv) < 3:
            print("Error: Template name required.")
            print("Usage: download <template_name>")
            sys.exit(1)
        
        template_name = sys.argv[2]
        template_path = download_template(template_name)
        
        if template_path:
            print(f"Success! Template downloaded to: {template_path}")
            # Show the first few lines if it's a text file
            if template_path.endswith(('.txt', '.md')):
                print("\nPreview:")
                with open(template_path, 'r') as f:
                    for i, line in enumerate(f):
                        if i >= 10:
                            break
                        print(f"  {line.rstrip()}")
        else:
            print(f"Failed to download template: {template_name}")
    
    elif command == "check-config":
        print("\nChecking configuration:")
        print("-----------------------")
        
        # Check GitHub
        if not GITHUB_REPO:
            print("❌ GitHub repository not configured.")
        else:
            print(f"✓ GitHub repository: {GITHUB_REPO}")
            release = get_latest_github_release()
            if release:
                print(f"✓ Latest release: {release['tag_name']} - {release['name']}")
            else:
                print("❌ Could not fetch latest release.")
        
        # Check Cloudinary
        if check_cloudinary_config():
            print("✓ Cloudinary configuration looks good.")
        else:
            print("❌ Cloudinary not properly configured.")
        
        print("\nFor a full demonstration of Cloudinary uploads and transformations,")
        print("please use the full Flask application in simple_resource_demo.py")
    
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1) 