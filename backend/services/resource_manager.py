"""
Unified Resource Manager for SmartProBono.

This service provides a unified interface for managing different types of resources:
- Official templates: Stored in GitHub Releases
- User-generated content: Stored in Cloudinary
"""
import os
import logging
from pathlib import Path
from .github_resource_service import GitHubResourceService
from .cloudinary_service import CloudinaryService

logger = logging.getLogger(__name__)

# Resource type constants
RESOURCE_TYPE_TEMPLATE = "template"         # Official templates in GitHub Releases
RESOURCE_TYPE_USER_DOCUMENT = "user_document" # User-uploaded documents in Cloudinary
RESOURCE_TYPE_MEDIA = "media"               # Media files (images, videos) in Cloudinary

class ResourceManager:
    """
    Unified service for managing all SmartProBono resources.
    
    This class provides a facade over different storage backends,
    selecting the appropriate one based on the resource type.
    """
    
    def __init__(self):
        """Initialize the resource manager with its underlying services."""
        self.github_service = GitHubResourceService()
        self.cloudinary_service = CloudinaryService()
        
        # Create a local temporary upload directory
        self.upload_dir = Path(os.environ.get("UPLOAD_FOLDER", "/tmp/smartprobono_uploads"))
        self.upload_dir.mkdir(exist_ok=True, parents=True)
    
    def get_resource(self, resource_id, resource_type=RESOURCE_TYPE_TEMPLATE, version="latest", **kwargs):
        """
        Get a resource by ID, using the appropriate backend based on resource type.
        
        Args:
            resource_id: Resource identifier
            resource_type: Type of resource (template, user_document, media)
            version: Version for versioned resources
            **kwargs: Additional parameters for the backend
            
        Returns:
            Path to file or URL, depending on resource type
        """
        try:
            # Official templates are stored in GitHub Releases
            if resource_type == RESOURCE_TYPE_TEMPLATE:
                return self.github_service.get_template(resource_id, version)
            
            # User-uploaded content is in Cloudinary
            elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
                cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
                format_type = kwargs.get("format")
                transformations = kwargs.get("transformations")
                
                return self.cloudinary_service.get_file_url(
                    resource_id, 
                    resource_type=cloudinary_type,
                    format=format_type,
                    transformations=transformations
                )
            
            else:
                logger.error(f"Unsupported resource type: {resource_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting resource {resource_id} of type {resource_type}: {str(e)}")
            return None
            
    def upload_resource(self, file_path, resource_type=RESOURCE_TYPE_USER_DOCUMENT, **kwargs):
        """
        Upload a resource to the appropriate backend.
        
        Args:
            file_path: Path to the file
            resource_type: Type of resource
            **kwargs: Additional parameters for the uploader
            
        Returns:
            Resource ID or information
        """
        try:
            # Templates are managed through GitHub Releases
            if resource_type == RESOURCE_TYPE_TEMPLATE:
                logger.error("Templates should be added to GitHub Releases, not uploaded through this API")
                return None
            
            # User-generated content goes to Cloudinary
            elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
                cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "auto"
                folder = kwargs.get("folder", resource_type + "s")
                
                result = self.cloudinary_service.upload_file(
                    file_path,
                    resource_type=cloudinary_type,
                    folder=folder,
                    tags=kwargs.get("tags"),
                    public_id=kwargs.get("public_id"),
                    metadata=kwargs.get("metadata")
                )
                
                if not result:
                    return None
                    
                return {
                    "id": result["public_id"],
                    "url": result["secure_url"],
                    "resource_type": result["resource_type"],
                    "format": result.get("format"),
                    "version": result.get("version"),
                    "created_at": result.get("created_at")
                }
                
            else:
                logger.error(f"Unsupported resource type for upload: {resource_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading resource of type {resource_type}: {str(e)}")
            return None
            
    def list_resources(self, resource_type=RESOURCE_TYPE_TEMPLATE, **kwargs):
        """
        List resources of a specific type.
        
        Args:
            resource_type: Type of resource to list
            **kwargs: Additional parameters for the listing service
            
        Returns:
            List of resources
        """
        try:
            # Official templates from GitHub Releases
            if resource_type == RESOURCE_TYPE_TEMPLATE:
                version = kwargs.get("version", "latest")
                category = kwargs.get("category")
                search = kwargs.get("search")
                
                if search:
                    return self.github_service.search_templates(search, version)
                else:
                    return self.github_service.list_templates(version, category)
            
            # User content from Cloudinary
            elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
                cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
                folder = kwargs.get("folder")
                tags = kwargs.get("tags")
                prefix = kwargs.get("prefix")
                max_results = kwargs.get("max_results", 100)
                
                return self.cloudinary_service.list_files(
                    folder=folder,
                    resource_type=cloudinary_type,
                    max_results=max_results,
                    prefix=prefix,
                    tags=tags,
                    context=True
                )
                
            else:
                logger.error(f"Unsupported resource type for listing: {resource_type}")
                return []
                
        except Exception as e:
            logger.error(f"Error listing resources of type {resource_type}: {str(e)}")
            return []
            
    def delete_resource(self, resource_id, resource_type=RESOURCE_TYPE_USER_DOCUMENT):
        """
        Delete a resource.
        
        Args:
            resource_id: Resource identifier
            resource_type: Type of resource
            
        Returns:
            Boolean indicating success
        """
        try:
            # Cannot delete official templates
            if resource_type == RESOURCE_TYPE_TEMPLATE:
                logger.error("Cannot delete official templates through API")
                return False
            
            # Delete user content from Cloudinary
            elif resource_type in [RESOURCE_TYPE_USER_DOCUMENT, RESOURCE_TYPE_MEDIA]:
                cloudinary_type = "raw" if resource_type == RESOURCE_TYPE_USER_DOCUMENT else "image"
                return self.cloudinary_service.delete_file(resource_id, cloudinary_type)
                
            else:
                logger.error(f"Unsupported resource type for deletion: {resource_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting resource {resource_id} of type {resource_type}: {str(e)}")
            return False
            
    def get_temp_upload_path(self, filename):
        """
        Get a temporary file path for uploading.
        
        Args:
            filename: Name of the file
            
        Returns:
            Path to save the uploaded file
        """
        safe_filename = "".join([c for c in filename if c.isalnum() or c in "._- "])
        return str(self.upload_dir / safe_filename)
        
    def clear_temp_files(self, max_age_hours=24):
        """
        Clear temporary files older than the specified age.
        
        Args:
            max_age_hours: Maximum age in hours
            
        Returns:
            Number of files deleted
        """
        import time
        from datetime import datetime, timedelta
        
        count = 0
        max_age = datetime.now() - timedelta(hours=max_age_hours)
        max_age_timestamp = max_age.timestamp()
        
        for path in self.upload_dir.glob("*"):
            if path.is_file():
                file_age = path.stat().st_mtime
                if file_age < max_age_timestamp:
                    path.unlink()
                    count += 1
                    
        return count 