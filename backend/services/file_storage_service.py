"""
File storage service for managing document files.

This service provides functionality for storing and retrieving files,
with support for both local filesystem storage and cloud storage.
"""

import os
import uuid
import logging
from typing import BinaryIO, Optional, Tuple
from pathlib import Path
import tempfile
import io

# Import optional cloud storage providers
try:
    import cloudinary
    import cloudinary.uploader
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

class FileStorageService:
    """Service for storing and retrieving files."""
    
    # Storage configuration
    STORAGE_TYPE = os.environ.get('STORAGE_TYPE', 'local')  # 'local' or 'cloud'
    LOCAL_STORAGE_PATH = os.environ.get('LOCAL_STORAGE_PATH', 'uploads')
    
    @classmethod
    def init_storage(cls):
        """Initialize the storage system."""
        if cls.STORAGE_TYPE == 'local':
            # Ensure local storage directory exists
            os.makedirs(cls.LOCAL_STORAGE_PATH, exist_ok=True)
            os.makedirs(os.path.join(cls.LOCAL_STORAGE_PATH, 'documents'), exist_ok=True)
            os.makedirs(os.path.join(cls.LOCAL_STORAGE_PATH, 'templates'), exist_ok=True)
            logger.info(f"Local storage initialized at {cls.LOCAL_STORAGE_PATH}")
        elif cls.STORAGE_TYPE == 'cloud' and CLOUDINARY_AVAILABLE:
            # Initialize Cloudinary
            cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
            api_key = os.environ.get('CLOUDINARY_API_KEY')
            api_secret = os.environ.get('CLOUDINARY_API_SECRET')
            
            if not all([cloud_name, api_key, api_secret]):
                logger.warning("Cloudinary environment variables not set. Falling back to local storage.")
                cls.STORAGE_TYPE = 'local'
                cls.init_storage()  # Reinitialize with local storage
            else:
                cloudinary.config(
                    cloud_name=cloud_name,
                    api_key=api_key,
                    api_secret=api_secret
                )
                logger.info("Cloudinary storage initialized")
        else:
            logger.warning("Cloud storage requested but Cloudinary not available. Falling back to local storage.")
            cls.STORAGE_TYPE = 'local'
            cls.init_storage()  # Reinitialize with local storage
    
    @classmethod
    def save_file(cls, file_data: BinaryIO, file_path: str, content_type: Optional[str] = None) -> Tuple[bool, str]:
        """
        Save a file to storage.
        
        Args:
            file_data: File data as a binary stream
            file_path: Path where the file should be stored
            content_type: MIME type of the file
            
        Returns:
            Tuple of (success, file_url_or_path)
        """
        if cls.STORAGE_TYPE == 'local':
            return cls._save_file_local(file_data, file_path)
        elif cls.STORAGE_TYPE == 'cloud' and CLOUDINARY_AVAILABLE:
            return cls._save_file_cloud(file_data, file_path, content_type)
        else:
            logger.warning("Unsupported storage type. Falling back to local storage.")
            return cls._save_file_local(file_data, file_path)
    
    @classmethod
    def _save_file_local(cls, file_data: BinaryIO, file_path: str) -> Tuple[bool, str]:
        """Save a file to the local filesystem."""
        try:
            # Ensure the directory exists
            full_path = os.path.join(cls.LOCAL_STORAGE_PATH, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write the file
            with open(full_path, 'wb') as f:
                f.write(file_data.read())
            
            logger.info(f"File saved to {full_path}")
            return True, full_path
        except Exception as e:
            logger.error(f"Error saving file to local storage: {str(e)}")
            return False, str(e)
    
    @classmethod
    def _save_file_cloud(cls, file_data: BinaryIO, file_path: str, content_type: Optional[str] = None) -> Tuple[bool, str]:
        """Save a file to cloud storage (Cloudinary)."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(file_data.read())
                temp_path = temp.name
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                temp_path,
                public_id=file_path.replace('/', '_'),
                resource_type="auto"
            )
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            logger.info(f"File uploaded to Cloudinary: {result['url']}")
            return True, result['url']
        except Exception as e:
            logger.error(f"Error uploading file to cloud storage: {str(e)}")
            return False, str(e)
    
    @classmethod
    def get_file(cls, file_path: str) -> Tuple[bool, Optional[BinaryIO]]:
        """
        Get a file from storage.
        
        Args:
            file_path: Path of the file to retrieve
            
        Returns:
            Tuple of (success, file_data)
        """
        if cls.STORAGE_TYPE == 'local':
            return cls._get_file_local(file_path)
        elif cls.STORAGE_TYPE == 'cloud' and CLOUDINARY_AVAILABLE:
            return cls._get_file_cloud(file_path)
        else:
            logger.warning("Unsupported storage type. Falling back to local storage.")
            return cls._get_file_local(file_path)
    
    @classmethod
    def _get_file_local(cls, file_path: str) -> Tuple[bool, Optional[BinaryIO]]:
        """Get a file from the local filesystem."""
        try:
            full_path = os.path.join(cls.LOCAL_STORAGE_PATH, file_path)
            if not os.path.exists(full_path):
                logger.warning(f"File not found: {full_path}")
                return False, None
            
            file_data = open(full_path, 'rb')
            return True, file_data
        except Exception as e:
            logger.error(f"Error retrieving file from local storage: {str(e)}")
            return False, None
    
    @classmethod
    def _get_file_cloud(cls, file_path: str) -> Tuple[bool, Optional[BinaryIO]]:
        """Get a file from cloud storage (Cloudinary)."""
        try:
            # Get file from Cloudinary
            resource = cloudinary.api.resource(file_path.replace('/', '_'))
            if not resource:
                logger.warning(f"File not found in cloud storage: {file_path}")
                return False, None
            
            # Download the file
            import requests
            response = requests.get(resource['url'])
            if response.status_code != 200:
                logger.error(f"Error downloading file from cloud storage: {response.status_code}")
                return False, None
            
            # Return as file-like object
            file_data = io.BytesIO(response.content)
            return True, file_data
        except Exception as e:
            logger.error(f"Error retrieving file from cloud storage: {str(e)}")
            return False, None
    
    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            file_path: Path of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        if cls.STORAGE_TYPE == 'local':
            return cls._delete_file_local(file_path)
        elif cls.STORAGE_TYPE == 'cloud' and CLOUDINARY_AVAILABLE:
            return cls._delete_file_cloud(file_path)
        else:
            logger.warning("Unsupported storage type. Falling back to local storage.")
            return cls._delete_file_local(file_path)
    
    @classmethod
    def _delete_file_local(cls, file_path: str) -> bool:
        """Delete a file from the local filesystem."""
        try:
            full_path = os.path.join(cls.LOCAL_STORAGE_PATH, file_path)
            if not os.path.exists(full_path):
                logger.warning(f"File not found: {full_path}")
                return False
            
            os.remove(full_path)
            logger.info(f"File deleted: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file from local storage: {str(e)}")
            return False
    
    @classmethod
    def _delete_file_cloud(cls, file_path: str) -> bool:
        """Delete a file from cloud storage (Cloudinary)."""
        try:
            result = cloudinary.uploader.destroy(file_path.replace('/', '_'))
            if result.get('result') == 'ok':
                logger.info(f"File deleted from cloud storage: {file_path}")
                return True
            else:
                logger.warning(f"File not deleted from cloud storage: {result}")
                return False
        except Exception as e:
            logger.error(f"Error deleting file from cloud storage: {str(e)}")
            return False
    
    @classmethod
    def save_text_file(cls, content: str, file_path: str, encoding: str = 'utf-8') -> Tuple[bool, str]:
        """
        Save a text file to storage.
        
        Args:
            content: Text content to save
            file_path: Path where the file should be stored
            encoding: Text encoding to use
            
        Returns:
            Tuple of (success, file_url_or_path)
        """
        try:
            # Convert text to binary
            binary_data = io.BytesIO(content.encode(encoding))
            
            # Save the file
            return cls.save_file(binary_data, file_path, content_type='text/plain')
        except Exception as e:
            logger.error(f"Error saving text file: {str(e)}")
            return False, str(e)
    
    @classmethod
    def generate_unique_filename(cls, prefix: str, extension: str) -> str:
        """
        Generate a unique filename.
        
        Args:
            prefix: Prefix for the filename
            extension: File extension (without dot)
            
        Returns:
            Unique filename
        """
        filename = f"{prefix}_{uuid.uuid4().hex}.{extension}"
        return filename 