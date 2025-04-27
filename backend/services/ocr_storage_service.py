import os
import uuid
import logging
from datetime import datetime
from pathlib import Path

# For Cloudinary support
try:
    from services.cloudinary_service import cloudinary_service
    HAS_CLOUDINARY = True
except ImportError:
    HAS_CLOUDINARY = False
    logging.warning("Cloudinary service not available. Using local storage for OCR documents.")

logger = logging.getLogger(__name__)

class OCRStorageService:
    """Service for storing and retrieving OCR document images and results"""
    
    def __init__(self):
        """Initialize the OCR storage service"""
        self.local_storage_dir = os.path.join(os.getcwd(), 'data', 'ocr_documents')
        
        # Create local directory if not exists
        Path(self.local_storage_dir).mkdir(parents=True, exist_ok=True)
    
    def store_document(self, file_obj, user_id=None, document_type='general'):
        """
        Store document image using the available storage backend (Cloudinary or local)
        
        Args:
            file_obj: The file object to store
            user_id: Optional user ID to associate with the document
            document_type: Type of document being stored
            
        Returns:
            dict: Storage information including URLs
        """
        try:
            # Generate a unique file ID
            file_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            
            # Get original filename and extension
            original_filename = file_obj.filename
            ext = original_filename.split('.')[-1].lower() if original_filename else 'jpg'
            
            # Try to use Cloudinary if available
            if HAS_CLOUDINARY:
                return self._store_in_cloudinary(file_obj, file_id, document_type, user_id)
            else:
                return self._store_locally(file_obj, file_id, ext, document_type, user_id)
                
        except Exception as e:
            logger.error(f"Error storing document: {str(e)}")
            raise
    
    def _store_in_cloudinary(self, file_obj, file_id, document_type, user_id=None):
        """Store document in Cloudinary"""
        try:
            # Create a folder structure based on document type
            folder = f"ocr/{document_type}"
            
            # Create a public ID for the file
            public_id = f"{folder}/{file_id}"
            
            # Save the file to a temporary location
            temp_path = os.path.join(self.local_storage_dir, f"temp_{file_id}.{file_obj.filename.split('.')[-1]}")
            file_obj.save(temp_path)
            
            # Upload to Cloudinary
            upload_result = cloudinary_service.upload_file(
                temp_path,
                public_id=public_id,
                folder="",  # Empty string instead of None
                resource_type="image",
                tags=[document_type, "ocr", "scan"]
            )
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return {
                "storage_backend": "cloudinary",
                "file_id": file_id,
                "public_id": upload_result.get("public_id"),
                "secure_url": upload_result.get("secure_url"),
                "url": upload_result.get("url"),
                "original_filename": file_obj.filename,
                "document_type": document_type,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error storing in Cloudinary: {str(e)}")
            raise
    
    def _store_locally(self, file_obj, file_id, ext, document_type, user_id=None):
        """Store document locally when Cloudinary is not available"""
        try:
            # Create directory structure
            user_dir = os.path.join(self.local_storage_dir, str(user_id) if user_id else "anonymous")
            Path(user_dir).mkdir(exist_ok=True)
            
            document_type_dir = os.path.join(user_dir, document_type)
            Path(document_type_dir).mkdir(exist_ok=True)
            
            # Save file
            filename = f"{file_id}.{ext}"
            file_path = os.path.join(document_type_dir, filename)
            file_obj.save(file_path)
            
            # Create URL (relative path)
            relative_path = os.path.join("data", "ocr_documents", 
                                       str(user_id) if user_id else "anonymous", 
                                       document_type, 
                                       filename)
            
            base_url = os.environ.get("BASE_URL", "http://localhost:5000")
            
            return {
                "storage_backend": "local",
                "file_id": file_id,
                "file_path": file_path,
                "url": f"{base_url}/{relative_path.replace(os.sep, '/')}",
                "original_filename": file_obj.filename,
                "document_type": document_type,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error storing locally: {str(e)}")
            raise

# Initialize service
ocr_storage_service = OCRStorageService() 