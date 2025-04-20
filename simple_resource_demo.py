#!/usr/bin/env python3
"""
Simple Resource Demo for SmartProBono
Demonstrates the hybrid storage approach using GitHub Releases and Cloudinary
"""
from flask import Flask, jsonify, request, send_file
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import requests
import json
from pathlib import Path
import tempfile
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Constants for resource types
RESOURCE_TYPE_TEMPLATE = "template"        # GitHub Releases
RESOURCE_TYPE_USER_DOCUMENT = "user_document"  # Cloudinary
RESOURCE_TYPE_MEDIA = "media"              # Cloudinary

# GitHub configuration
GITHUB_REPO = os.environ.get("GITHUB_REPO", "SmartProBonoProject/SmartProBono")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

# Create temp directory for file uploads
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/tmp/smartprobono_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create a cache directory
CACHE_DIR = Path(os.path.expanduser("~/.smartprobono/cache"))
CACHE_DIR.mkdir(exist_ok=True, parents=True)

# GitHub API client
def github_headers():
    """Return headers for GitHub API requests."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def get_github_releases():
    """Get all GitHub releases."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
        response = requests.get(url, headers=github_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching GitHub releases: {e}")
        return []

def get_github_release_by_tag(tag):
    """Get a specific GitHub release by tag."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/tags/{tag}"
        response = requests.get(url, headers=github_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching GitHub release {tag}: {e}")
        return None

def get_latest_github_release():
    """Get the latest GitHub release."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, headers=github_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching latest GitHub release: {e}")
        return None

def get_template_from_github(template_name, version="latest"):
    """Download a template file from GitHub releases."""
    # Check cache first
    cache_key = f"{version}_{template_name}".replace("/", "_")
    cache_path = CACHE_DIR / cache_key
    
    if cache_path.exists():
        logger.info(f"Using cached template: {cache_path}")
        return str(cache_path)
    
    # Get the release
    if version == "latest":
        release = get_latest_github_release()
        if not release:
            logger.error("Latest release not found")
            return None
        version = release["tag_name"]
    else:
        release = get_github_release_by_tag(version)
        if not release:
            logger.error(f"Release {version} not found")
            return None
    
    # Download the template
    download_url = f"https://github.com/{GITHUB_REPO}/releases/download/{version}/{template_name}"
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(cache_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Template downloaded to: {cache_path}")
        return str(cache_path)
    except Exception as e:
        logger.error(f"Error downloading template {template_name}: {e}")
        return None

# Routes

@app.route('/')
def index():
    """Home page."""
    return jsonify({
        "message": "SmartProBono Hybrid Storage Demo",
        "github_status": "Ready" if GITHUB_REPO else "Not configured",
        "cloudinary_status": "Ready" if cloudinary.config().cloud_name else "Not configured",
        "endpoints": [
            "/api/resources",
            "/api/resources/<resource_id>"
        ]
    })

@app.route('/api/resources', methods=['GET'])
def list_resources():
    """List resources with filtering."""
    resource_type = request.args.get('type', RESOURCE_TYPE_TEMPLATE)
    
    # GitHub Templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        version = request.args.get('version', 'latest')
        category = request.args.get('category')
        search_term = request.args.get('search')
        
        # Get the release
        if version == "latest":
            release = get_latest_github_release()
        else:
            release = get_github_release_by_tag(version)
            
        if not release:
            return jsonify([])
            
        # Process the assets
        assets = release.get("assets", [])
        templates = []
        
        for asset in assets:
            name = asset["name"]
            
            # Skip non-template files
            if not (name.endswith('.txt') or name.endswith('.md') or 
                    name.endswith('.pdf') or name.endswith('.docx')):
                continue
                
            # Apply category filter
            if category and not name.startswith(f"{category}/"):
                continue
                
            # Apply search filter
            if search_term and search_term.lower() not in name.lower():
                continue
                
            templates.append({
                "name": name,
                "size": asset["size"],
                "download_url": asset["browser_download_url"],
                "created_at": asset["created_at"],
                "updated_at": asset.get("updated_at", asset["created_at"]),
                "download_count": asset["download_count"]
            })
        
        return jsonify(templates)
    
    # Cloudinary resources
    elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        folder = request.args.get('folder')
        tags_str = request.args.get('tags')
        max_results = int(request.args.get('max_results', 100))
        
        # Convert tags string to list
        tags = tags_str.split(',') if tags_str else None
        
        try:
            # Set resource type for Cloudinary
            cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
            
            # Build parameters for Cloudinary
            params = {
                "max_results": max_results,
                "resource_type": cloudinary_type,
                "type": "upload"
            }
            
            if folder:
                params["prefix"] = folder
                
            if tags:
                params["tags"] = True
                params["tag"] = ",".join(tags)
            
            # Get resources from Cloudinary
            result = cloudinary.api.resources(**params)
            return jsonify(result.get("resources", []))
            
        except Exception as e:
            logger.error(f"Error listing Cloudinary resources: {e}")
            return jsonify({"error": str(e)}), 500
    
    else:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400

@app.route('/api/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get a resource by ID."""
    resource_type = request.args.get('type', RESOURCE_TYPE_TEMPLATE)
    
    # GitHub Templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        version = request.args.get('version', 'latest')
        
        # Download the template
        template_path = get_template_from_github(resource_id, version)
        
        if not template_path:
            return jsonify({"error": "Template not found"}), 404
            
        return send_file(template_path, download_name=os.path.basename(resource_id))
    
    # Cloudinary resources
    elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        try:
            # Set resource type for Cloudinary
            cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
            
            # Handle format conversion
            format_type = request.args.get('format')
            
            # Handle transformations (e.g., resize, crop)
            transformations = {}
            for key in request.args:
                if key.startswith('t_'):
                    transformations[key[2:]] = request.args[key]
            
            # Build the URL
            options = {
                "resource_type": cloudinary_type,
                "secure": True,
                "sign_url": True
            }
            
            if format_type:
                options["format"] = format_type
                
            if transformations:
                options.update(transformations)
            
            url = cloudinary.CloudinaryImage(resource_id).build_url(**options)
            return jsonify({"url": url})
            
        except Exception as e:
            logger.error(f"Error getting Cloudinary resource {resource_id}: {e}")
            return jsonify({"error": str(e)}), 500
    
    else:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400

@app.route('/api/resources', methods=['POST'])
def upload_resource():
    """Upload a resource to Cloudinary."""
    resource_type = request.form.get('type', RESOURCE_TYPE_USER_DOCUMENT)
    
    # Ensure not trying to upload templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        return jsonify({
            "error": "Templates must be added to GitHub Releases, not uploaded through this API"
        }), 400
    
    # Ensure resource type is valid
    if resource_type not in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400
    
    # Get file from request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Get options from form
    folder = request.form.get('folder', resource_type + 's')
    tags_str = request.form.get('tags')
    tags = tags_str.split(',') if tags_str else None
    
    # Get metadata from form
    metadata = {}
    for key in request.form:
        if key.startswith('meta_'):
            metadata[key[5:]] = request.form[key]
    
    # Save file temporarily
    filename = secure_filename(file.filename or "uploaded_file")
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(temp_path)
    
    try:
        # Set resource type for Cloudinary
        cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "auto"
        
        # Generate a unique ID
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(filename))[0]
        public_id = f"{base_name}_{timestamp}"
        
        # Upload to Cloudinary
        upload_params = {
            "public_id": public_id,
            "folder": folder,
            "resource_type": cloudinary_type,
            "overwrite": True,
            "use_filename": True,
            "unique_filename": True,
        }
        
        if tags:
            upload_params["tags"] = tags
            
        if metadata:
            upload_params["context"] = metadata
            
        result = cloudinary.uploader.upload(temp_path, **upload_params)
        
        # Return the result
        return jsonify({
            "id": result["public_id"],
            "url": result["secure_url"],
            "resource_type": result["resource_type"],
            "format": result.get("format"),
            "version": result.get("version"),
            "created_at": result.get("created_at")
        }), 201
            
    except Exception as e:
        logger.error(f"Error uploading to Cloudinary: {e}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/resources/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """Delete a resource from Cloudinary."""
    resource_type = request.args.get('type', RESOURCE_TYPE_USER_DOCUMENT)
    
    # Ensure not trying to delete templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        return jsonify({
            "error": "Templates cannot be deleted through this API"
        }), 400
    
    # Ensure resource type is valid
    if resource_type not in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400
    
    try:
        # Set resource type for Cloudinary
        cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
        
        # Delete from Cloudinary
        result = cloudinary.uploader.destroy(resource_id, resource_type=cloudinary_type)
        
        if result.get("result") == "ok":
            return jsonify({"message": f"Resource {resource_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete resource"}), 500
            
    except Exception as e:
        logger.error(f"Error deleting from Cloudinary: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check for missing configuration
    if not cloudinary.config().cloud_name:
        logger.warning("Cloudinary not configured properly. User uploads and media will not work.")
    
    # Run the application
    app.run(debug=True, port=5005) 