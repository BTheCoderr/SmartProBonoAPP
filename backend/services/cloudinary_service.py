import os
import logging
from dotenv import load_dotenv
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    from cloudinary.utils import cloudinary_url
except ImportError:
    print("Warning: Cloudinary packages not found. Install with 'pip install cloudinary'")

# Load environment variables
load_dotenv()

# Configure Cloudinary
try:
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )
except (NameError, AttributeError):
    print("Warning: Could not configure Cloudinary - package not properly imported")

# Initialize logger
logger = logging.getLogger(__name__)

# Constants for Cloudinary folders and presets
CASE_FOLDER = 'smartprobono/case_documents'
TEMPLATE_FOLDER = 'smartprobono/document_templates'
USER_FOLDER = 'smartprobono/user_uploads'

DOCUMENT_UPLOAD_PRESET = 'document_uploads'
TEMPLATE_UPLOAD_PRESET = 'template_uploads'
USER_UPLOAD_PRESET = 'user_uploads'


class CloudinaryService:
    """Service for handling Cloudinary operations"""

    @staticmethod
    def get_upload_signature(preset_name=USER_UPLOAD_PRESET):
        """Get a signature for direct upload from frontend"""
        try:
            timestamp = cloudinary.utils.now()
            signature = cloudinary.utils.api_sign_request({
                'timestamp': timestamp,
                'upload_preset': preset_name
            }, cloudinary.config().api_secret)
            
            return {
                'signature': signature,
                'timestamp': timestamp,
                'cloudName': cloudinary.config().cloud_name,
                'apiKey': cloudinary.config().api_key,
                'uploadPreset': preset_name
            }
        except Exception as e:
            logger.error(f"Error generating upload signature: {e}")
            raise

    @staticmethod
    def upload_file(file_path, public_id=None, folder=USER_FOLDER, resource_type='auto', **options):
        """Upload a file to Cloudinary from the server"""
        try:
            upload_options = {
                'folder': folder,
                'resource_type': resource_type,
                **options
            }
            
            if public_id:
                upload_options['public_id'] = public_id
            
            result = cloudinary.uploader.upload(file_path, **upload_options)
            return result
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise

    @staticmethod
    def generate_url(public_id, **options):
        """Generate a URL for a Cloudinary resource"""
        try:
            url, options = cloudinary_url(public_id, **options)
            return url
        except Exception as e:
            logger.error(f"Error generating URL: {e}")
            raise

    @staticmethod
    def delete_file(public_id, resource_type='auto'):
        """Delete a file from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            return result
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise
    
    @staticmethod
    def list_files(folder, resource_type='auto', max_results=100):
        """List files in a folder"""
        try:
            result = cloudinary.api.resources(
                type='upload',
                prefix=folder,
                resource_type=resource_type,
                max_results=max_results
            )
            return result.get('resources', [])
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise
    
    @staticmethod
    def create_folder(folder):
        """Create a new folder in Cloudinary"""
        try:
            result = cloudinary.api.create_folder(folder)
            return result
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            raise


# Create singleton instance
cloudinary_service = CloudinaryService() 