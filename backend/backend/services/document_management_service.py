"""
Document Management Service for handling document lifecycle.
"""
import os
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from flask import current_app
from werkzeug.utils import secure_filename
from bson import ObjectId
from services.mongodb_service import mongodb_service
from services.error_logging_service import error_logging_service
from utils.encryption import encrypt_document, decrypt_document

class DocumentManagementService:
    """Service for managing documents throughout their lifecycle."""
    
    def __init__(self):
        """Initialize the document management service."""
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        
        # Ensure upload directory exists
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
        
        # Define sensitive fields for encryption
        self.sensitive_fields = [
            'client_ssn', 
            'client_dob', 
            'client_address',
            'client_phone', 
            'bank_info',
            'confidential_notes'
        ]
        
        # Document access levels
        self.access_levels = {
            'public': 1,     # Visible to anyone
            'internal': 2,   # Visible to organization members
            'confidential': 3, # Visible to specific users only
            'restricted': 4  # Visible only to owner and admins
        }
    
    async def create_document(self, file, metadata: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Create a new document from a file upload.
        
        Args:
            file: The uploaded file object
            metadata: Document metadata
            user_id: ID of the user creating the document
            
        Returns:
            Dict: The created document record
        """
        try:
            # Secure the filename
            original_filename = secure_filename(file.filename)
            
            # Generate a unique filename
            filename = f"{uuid.uuid4().hex}_{original_filename}"
            
            # Save the file
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            
            # Get file size and mime type
            file_size = os.path.getsize(file_path)
            file_type = file.content_type
            
            # Create document record
            document = {
                'filename': filename,
                'original_filename': original_filename,
                'file_path': file_path,
                'file_type': file_type,
                'file_size': file_size,
                'metadata': metadata,
                'owner_id': user_id,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'version': 1,
                'is_latest': True,
                'status': 'active',
                'access_level': metadata.get('access_level', 'internal'),
                'shared_with': metadata.get('shared_with', []),
                'tags': metadata.get('tags', [])
            }
            
            # Encrypt sensitive fields if present
            document = encrypt_document(document, self.sensitive_fields)
            
            # Store in MongoDB
            document_id = await mongodb_service.store_document(document)
            
            # Add document ID to the record
            document['_id'] = document_id
            
            return self._sanitize_document(document)
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def get_document(self, document_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by ID.
        
        Args:
            document_id: The document ID
            user_id: ID of the user requesting the document
            
        Returns:
            Optional[Dict]: The document record if found and accessible
        """
        try:
            # Get document from MongoDB
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return None
            
            # Check access permissions
            if not self._can_access(document, user_id):
                return None
                
            # Decrypt sensitive fields
            document = decrypt_document(document, self.sensitive_fields)
            
            return self._sanitize_document(document)
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def update_document(self, document_id: str, updates: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Update a document's metadata.
        
        Args:
            document_id: The document ID
            updates: The updates to apply
            user_id: ID of the user updating the document
            
        Returns:
            Optional[Dict]: The updated document if successful
        """
        try:
            # Get current document
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return None
            
            # Check permissions
            if not self._can_modify(document, user_id):
                raise PermissionError("You don't have permission to modify this document")
            
            # Prepare updates
            update_data = {
                'metadata': {**document.get('metadata', {}), **updates.get('metadata', {})},
                'updated_at': datetime.utcnow()
            }
            
            # Update other fields if provided
            for field in ['access_level', 'shared_with', 'tags', 'status']:
                if field in updates:
                    update_data[field] = updates[field]
            
            # Encrypt sensitive fields if present
            update_data = encrypt_document(update_data, self.sensitive_fields)
            
            # Apply updates
            success = await mongodb_service.update_document(document_id, update_data)
            
            if not success:
                return None
                
            # Get updated document
            updated_document = await mongodb_service.get_document(document_id)
            
            # Decrypt sensitive fields
            updated_document = decrypt_document(updated_document, self.sensitive_fields)
            
            return self._sanitize_document(updated_document)
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def replace_document_file(self, document_id: str, file, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Replace a document's file, creating a new version.
        
        Args:
            document_id: The document ID
            file: The new file
            user_id: ID of the user replacing the file
            
        Returns:
            Optional[Dict]: The updated document record
        """
        try:
            # Get current document
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return None
            
            # Check permissions
            if not self._can_modify(document, user_id):
                raise PermissionError("You don't have permission to modify this document")
            
            # Mark current version as not latest
            await mongodb_service.update_document(document_id, {
                'is_latest': False
            })
            
            # Secure the filename
            original_filename = secure_filename(file.filename)
            
            # Generate a unique filename
            filename = f"{uuid.uuid4().hex}_{original_filename}"
            
            # Save the file
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            
            # Get file info
            file_size = os.path.getsize(file_path)
            file_type = file.content_type
            
            # Create new version
            new_version = {
                'filename': filename,
                'original_filename': original_filename,
                'file_path': file_path,
                'file_type': file_type,
                'file_size': file_size,
                'metadata': document.get('metadata', {}),
                'owner_id': document.get('owner_id'),
                'created_at': document.get('created_at'),
                'updated_at': datetime.utcnow(),
                'version': document.get('version', 1) + 1,
                'is_latest': True,
                'status': document.get('status', 'active'),
                'access_level': document.get('access_level', 'internal'),
                'shared_with': document.get('shared_with', []),
                'tags': document.get('tags', []),
                'previous_version_id': document_id
            }
            
            # Encrypt sensitive fields
            new_version = encrypt_document(new_version, self.sensitive_fields)
            
            # Store in MongoDB
            new_document_id = await mongodb_service.store_document(new_version)
            
            # Add document ID to the record
            new_version['_id'] = new_document_id
            
            return self._sanitize_document(new_version)
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def delete_document(self, document_id: str, user_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            document_id: The document ID
            user_id: ID of the user deleting the document
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            # Get document
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return False
            
            # Check permissions (only owner or admin can delete)
            if not self._can_delete(document, user_id):
                raise PermissionError("You don't have permission to delete this document")
            
            # Soft delete - update status to deleted
            success = await mongodb_service.update_document(document_id, {
                'status': 'deleted',
                'updated_at': datetime.utcnow()
            })
            
            if success and document.get('file_path') and os.path.exists(document.get('file_path')):
                # Move file to trash folder instead of deleting
                trash_folder = os.path.join(self.upload_folder, 'trash')
                
                if not os.path.exists(trash_folder):
                    os.makedirs(trash_folder)
                
                # Move file to trash
                trash_path = os.path.join(trash_folder, document.get('filename'))
                os.rename(document.get('file_path'), trash_path)
            
            return success
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def list_documents(self, 
                           user_id: str, 
                           filters: Optional[Dict[str, Any]] = None, 
                           skip: int = 0, 
                           limit: int = 20) -> List[Dict[str, Any]]:
        """
        List documents with filtering and pagination.
        
        Args:
            user_id: ID of the user requesting documents
            filters: Filter criteria
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            List[Dict]: List of document records
        """
        try:
            # Prepare base query
            query = filters or {}
            
            # Only active documents
            query['status'] = {'$ne': 'deleted'}
            
            # Only latest versions
            query['is_latest'] = True
            
            # Access control
            # 1. Documents owned by the user
            # 2. Documents shared with the user
            # 3. Public documents
            # 4. Internal documents if the user has internal access
            access_query = {
                '$or': [
                    {'owner_id': user_id},
                    {'shared_with': user_id},
                    {'access_level': 'public'}
                ]
            }
            
            # Add internal access if applicable
            # This would be based on user roles/groups
            user_has_internal_access = True  # This should be determined from user roles
            if user_has_internal_access:
                access_query['$or'].append({'access_level': 'internal'})
            
            # Combine with existing query
            if '$or' in query:
                query = {
                    '$and': [query, access_query]
                }
            else:
                query.update(access_query)
            
            # Get documents
            documents = await mongodb_service.list_documents(query, skip, limit)
            
            # Process documents
            result = []
            for doc in documents:
                # Decrypt sensitive fields
                doc = decrypt_document(doc, self.sensitive_fields)
                
                # Sanitize document
                sanitized = self._sanitize_document(doc)
                result.append(sanitized)
            
            return result
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def search_documents(self, 
                             query: str, 
                             user_id: str, 
                             skip: int = 0, 
                             limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search documents based on text query.
        
        Args:
            query: Search query
            user_id: ID of the user searching
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            List[Dict]: List of matching document records
        """
        try:
            # Get documents matching the query
            documents = await mongodb_service.search_documents(query, skip, limit)
            
            # Filter for access control
            result = []
            for doc in documents:
                # Skip deleted documents
                if doc.get('status') == 'deleted':
                    continue
                    
                # Check access permissions
                if not self._can_access(doc, user_id):
                    continue
                
                # Decrypt sensitive fields
                doc = decrypt_document(doc, self.sensitive_fields)
                
                # Sanitize document
                sanitized = self._sanitize_document(doc)
                result.append(sanitized)
            
            return result
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def share_document(self, 
                           document_id: str, 
                           user_id: str,
                           share_with_ids: List[str]) -> Optional[Dict[str, Any]]:
        """
        Share a document with users.
        
        Args:
            document_id: The document ID
            user_id: ID of the user sharing the document
            share_with_ids: List of user IDs to share with
            
        Returns:
            Optional[Dict]: The updated document if successful
        """
        try:
            # Get document
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return None
            
            # Check permissions
            if not self._can_modify(document, user_id):
                raise PermissionError("You don't have permission to share this document")
            
            # Get current shared_with list
            shared_with = document.get('shared_with', [])
            
            # Add new users
            for share_id in share_with_ids:
                if share_id not in shared_with:
                    shared_with.append(share_id)
            
            # Update document
            success = await mongodb_service.update_document(document_id, {
                'shared_with': shared_with,
                'updated_at': datetime.utcnow()
            })
            
            if not success:
                return None
                
            # Get updated document
            updated_document = await mongodb_service.get_document(document_id)
            
            # Decrypt sensitive fields
            updated_document = decrypt_document(updated_document, self.sensitive_fields)
            
            return self._sanitize_document(updated_document)
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    async def get_document_versions(self, 
                                  document_id: str, 
                                  user_id: str) -> List[Dict[str, Any]]:
        """
        Get all versions of a document.
        
        Args:
            document_id: The document ID
            user_id: ID of the user requesting versions
            
        Returns:
            List[Dict]: List of document versions
        """
        try:
            # Get document
            document = await mongodb_service.get_document(document_id)
            
            if not document:
                return []
            
            # Check access permissions
            if not self._can_access(document, user_id):
                return []
            
            # Get all versions
            versions = []
            
            # Add current document
            versions.append(document)
            
            # Get previous versions
            current = document
            while 'previous_version_id' in current:
                prev_id = current['previous_version_id']
                prev_version = await mongodb_service.get_document(prev_id)
                
                if prev_version:
                    versions.append(prev_version)
                    current = prev_version
                else:
                    break
            
            # Process versions
            result = []
            for version in versions:
                # Decrypt sensitive fields
                version = decrypt_document(version, self.sensitive_fields)
                
                # Sanitize document
                sanitized = self._sanitize_document(version)
                result.append(sanitized)
            
            # Sort by version number
            result.sort(key=lambda x: x.get('version', 1), reverse=True)
            
            return result
            
        except Exception as e:
            error_logging_service.log_exception(e)
            raise
    
    def _can_access(self, document: Dict[str, Any], user_id: str) -> bool:
        """Check if a user can access a document."""
        # Document owner can always access
        if document.get('owner_id') == user_id:
            return True
        
        # Shared with user
        if user_id in document.get('shared_with', []):
            return True
        
        # Public documents are accessible to all
        if document.get('access_level') == 'public':
            return True
        
        # Internal documents are accessible to organization members
        # This would be based on user roles/groups
        if document.get('access_level') == 'internal':
            # Check if user has internal access
            user_has_internal_access = True  # This should be determined from user roles
            return user_has_internal_access
        
        # Confidential/restricted documents are not accessible unless owned or explicitly shared
        return False
    
    def _can_modify(self, document: Dict[str, Any], user_id: str) -> bool:
        """Check if a user can modify a document."""
        # Document owner can always modify
        if document.get('owner_id') == user_id:
            return True
        
        # Admin users can modify any document
        # This should be determined from user roles
        user_is_admin = False  # This should be determined from user roles
        
        return user_is_admin
    
    def _can_delete(self, document: Dict[str, Any], user_id: str) -> bool:
        """Check if a user can delete a document."""
        # Only owner and admins can delete
        if document.get('owner_id') == user_id:
            return True
        
        # Admin users can delete any document
        # This should be determined from user roles
        user_is_admin = False  # This should be determined from user roles
        
        return user_is_admin
    
    def _sanitize_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive internal fields from document record."""
        # Create a copy to avoid modifying the original
        sanitized = document.copy()
        
        # Remove internal fields
        if 'file_path' in sanitized:
            del sanitized['file_path']
        
        # Convert ObjectId to string
        if '_id' in sanitized and isinstance(sanitized['_id'], ObjectId):
            sanitized['_id'] = str(sanitized['_id'])
        
        # Format dates
        for date_field in ['created_at', 'updated_at']:
            if date_field in sanitized and isinstance(sanitized[date_field], datetime):
                sanitized[date_field] = sanitized[date_field].isoformat()
        
        return sanitized

# Create a singleton instance
document_management_service = DocumentManagementService() 