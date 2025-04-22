from flask import Blueprint, request, jsonify, current_app
import os
import uuid
import tempfile
from werkzeug.utils import secure_filename
from services.cloudinary_service import cloudinary_service, DOCUMENT_UPLOAD_PRESET, TEMPLATE_UPLOAD_PRESET, USER_UPLOAD_PRESET

# Create blueprint
uploads = Blueprint('uploads', __name__, url_prefix='/api/uploads')

@uploads.route('/signature', methods=['GET'])
def get_upload_signature():
    """Get a signature for direct uploads from frontend"""
    preset_type = request.args.get('type', 'user')
    
    # Determine which preset to use
    if preset_type == 'document':
        preset_name = DOCUMENT_UPLOAD_PRESET
    elif preset_type == 'template':
        preset_name = TEMPLATE_UPLOAD_PRESET
    else:
        preset_name = USER_UPLOAD_PRESET
    
    try:
        # Get signature from service
        result = cloudinary_service.get_upload_signature(preset_name)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting upload signature: {str(e)}")
        return jsonify({"error": "Could not generate upload signature"}), 500

@uploads.route('/server', methods=['POST'])
def upload_file():
    """Upload a file from the server to Cloudinary"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Get parameters from request
    folder = request.form.get('folder')
    resource_type = request.form.get('resource_type', 'auto')
    public_id = request.form.get('public_id')
    
    # Save the file temporarily
    try:
        filename = secure_filename(file.filename)
        temp_file_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{filename}")
        file.save(temp_file_path)
        
        # Upload to Cloudinary
        result = cloudinary_service.upload_file(
            temp_file_path, 
            public_id=public_id,
            folder=folder,
            resource_type=resource_type
        )
        
        # Clean up the temp file
        os.remove(temp_file_path)
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error uploading file: {str(e)}")
        # Clean up the temp file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return jsonify({"error": "Failed to upload file"}), 500

@uploads.route('/<public_id>', methods=['DELETE'])
def delete_file(public_id):
    """Delete a file from Cloudinary"""
    resource_type = request.args.get('resource_type', 'auto')
    
    try:
        result = cloudinary_service.delete_file(public_id, resource_type)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return jsonify({"error": "Failed to delete file"}), 500

@uploads.route('/list', methods=['GET'])
def list_files():
    """List files in a folder"""
    folder = request.args.get('folder', '')
    resource_type = request.args.get('resource_type', 'auto')
    max_results = request.args.get('max_results', 100, type=int)
    
    try:
        result = cloudinary_service.list_files(folder, resource_type, max_results)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error listing files: {str(e)}")
        return jsonify({"error": "Failed to list files"}), 500 