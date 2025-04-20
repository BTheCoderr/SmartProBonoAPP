"""
API routes for resource management.

These routes handle:
1. Listing resources from both GitHub and Cloudinary
2. Downloading official templates from GitHub Releases
3. Uploading user-generated content to Cloudinary
4. Deleting user-generated content
"""
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
import logging
from ..services.resource_manager import ResourceManager, RESOURCE_TYPE_TEMPLATE, RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA

logger = logging.getLogger(__name__)
resource_routes = Blueprint('resources', __name__)
resource_manager = ResourceManager()

#
# Resource Listing Routes
#

@resource_routes.route('/api/resources', methods=['GET'])
def list_resources():
    """
    List resources with filtering.
    
    Query parameters:
    - type: Resource type (template, user_document, media)
    - version: Version for templates (latest, v1.0.0, etc.)
    - category: Category for templates (legal, housing, etc.)
    - search: Search term for filtering
    - folder: Folder for Cloudinary resources
    - tags: Comma-separated tags for Cloudinary resources
    """
    resource_type = request.args.get('type', RESOURCE_TYPE_TEMPLATE)
    
    # Build parameters for the resource manager
    params = {}
    
    # Template-specific parameters (GitHub)
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        params['version'] = request.args.get('version', 'latest')
        params['category'] = request.args.get('category')
        params['search'] = request.args.get('search')
    
    # Cloudinary-specific parameters
    elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        params['folder'] = request.args.get('folder')
        tags = request.args.get('tags')
        if tags:
            params['tags'] = tags.split(',')
        params['prefix'] = request.args.get('prefix')
        max_results = request.args.get('max_results')
        if max_results and max_results.isdigit():
            params['max_results'] = int(max_results)
    
    # Get resources from the appropriate backend
    try:
        resources = resource_manager.list_resources(resource_type=resource_type, **params)
        return jsonify(resources)
    except Exception as e:
        logger.error(f"Error listing resources: {str(e)}")
        return jsonify({"error": f"Failed to list resources: {str(e)}"}), 500

#
# Resource Retrieval Routes
#

@resource_routes.route('/api/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """
    Get a resource by ID.
    
    For templates, this will download the file.
    For user documents and media, this will redirect to the Cloudinary URL.
    
    Query parameters:
    - type: Resource type (template, user_document, media)
    - version: Version for templates (latest, v1.0.0, etc.)
    - format: Format for Cloudinary resources (jpg, png, pdf, etc.)
    """
    resource_type = request.args.get('type', RESOURCE_TYPE_TEMPLATE)
    
    # Build parameters for the resource manager
    params = {}
    
    # Template-specific parameters
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        params['version'] = request.args.get('version', 'latest')
    
    # Cloudinary-specific parameters
    elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        if request.args.get('format'):
            params['format'] = request.args.get('format')
            
        # Handle transformations (e.g., resize, crop)
        transformations = {}
        for key in request.args:
            if key.startswith('t_'):
                transformations[key[2:]] = request.args[key]
        
        if transformations:
            params['transformations'] = transformations
    
    # Get the resource from the appropriate backend
    try:
        result = resource_manager.get_resource(resource_id, resource_type=resource_type, **params)
        
        if not result:
            return jsonify({"error": "Resource not found"}), 404
            
        # For templates, return the file
        if resource_type == RESOURCE_TYPE_TEMPLATE:
            return send_file(result, as_attachment=True, download_name=os.path.basename(resource_id))
        
        # For Cloudinary resources, return the URL
        else:
            return jsonify({"url": result})
            
    except Exception as e:
        logger.error(f"Error retrieving resource {resource_id}: {str(e)}")
        return jsonify({"error": f"Failed to retrieve resource: {str(e)}"}), 500
        
#
# Resource Upload Routes
#

@resource_routes.route('/api/resources', methods=['POST'])
def upload_resource():
    """
    Upload a resource.
    
    This only works for user-generated content (user_document, media).
    Templates must be added through GitHub Releases.
    
    Form parameters:
    - type: Resource type (user_document, media)
    - folder: Folder in Cloudinary
    - tags: Comma-separated tags
    - file: The file to upload
    """
    # Get form data
    resource_type = request.form.get('type', RESOURCE_TYPE_USER_DOCUMENT)
    
    # Ensure we're not trying to upload templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        return jsonify({
            "error": "Templates cannot be uploaded through this API. Add them to GitHub Releases."
        }), 400
    
    # Ensure the resource type is valid
    if resource_type not in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400
    
    # Get file from request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Build parameters for the resource manager
    params = {}
    
    # Add folder if specified
    if request.form.get('folder'):
        params['folder'] = request.form.get('folder')
    
    # Add tags if specified
    tags = request.form.get('tags')
    if tags:
        params['tags'] = tags.split(',')
    
    # Add metadata if specified
    metadata = {}
    for key in request.form:
        if key.startswith('meta_'):
            metadata[key[5:]] = request.form[key]
    
    if metadata:
        params['metadata'] = metadata
    
    # Save file temporarily
    filename = secure_filename(file.filename or "uploaded_file")
    temp_path = resource_manager.get_temp_upload_path(filename)
    file.save(temp_path)
    
    try:
        # Upload the file
        result = resource_manager.upload_resource(
            temp_path,
            resource_type=resource_type,
            **params
        )
        
        if not result:
            return jsonify({"error": "Failed to upload resource"}), 500
            
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error uploading resource: {str(e)}")
        return jsonify({"error": f"Failed to upload resource: {str(e)}"}), 500
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
#
# Resource Deletion Route
#

@resource_routes.route('/api/resources/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Delete a resource.
    
    This only works for user-generated content (user_document, media).
    Templates cannot be deleted through the API.
    
    Query parameters:
    - type: Resource type (user_document, media)
    """
    resource_type = request.args.get('type', RESOURCE_TYPE_USER_DOCUMENT)
    
    # Ensure we're not trying to delete templates
    if resource_type == RESOURCE_TYPE_TEMPLATE:
        return jsonify({
            "error": "Templates cannot be deleted through this API."
        }), 400
    
    # Ensure the resource type is valid
    if resource_type not in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
        return jsonify({"error": f"Invalid resource type: {resource_type}"}), 400
    
    try:
        success = resource_manager.delete_resource(resource_id, resource_type=resource_type)
        
        if not success:
            return jsonify({"error": "Failed to delete resource"}), 500
            
        return jsonify({"message": f"Resource {resource_id} deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error deleting resource {resource_id}: {str(e)}")
        return jsonify({"error": f"Failed to delete resource: {str(e)}"}), 500 