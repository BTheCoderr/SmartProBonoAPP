"""Document service for handling document operations."""
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from database import db, mongo
from models.document import Document
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    """Service class for document operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_document(self, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Create a new document."""
        try:
            document = {
                'title': data['title'],
                'content': data.get('content', ''),
                'file_url': data.get('file_url'),
                'file_type': data.get('file_type'),
                'document_type': data.get('document_type', 'general'),
                'description': data.get('description', ''),
                'tags': data.get('tags', []),
                'created_by': ObjectId(user_id),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'status': 'active'
            }
            
            result = mongo.db.documents.insert_one(document)
            document['_id'] = str(result.inserted_id)
            return document
        except Exception as e:
            self.logger.error(f"Error creating document: {str(e)}")
            return None
    
    def get_document(self, document_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID."""
        try:
            document = mongo.db.documents.find_one({
                '_id': ObjectId(document_id),
                'created_by': ObjectId(user_id)
            })
            
            if document:
                document['_id'] = str(document['_id'])
                document['created_by'] = str(document['created_by'])
            return document
        except Exception as e:
            self.logger.error(f"Error getting document: {str(e)}")
            return None
    
    def update_document(self, document_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Update a document."""
        try:
            update_data = {
                'updated_at': datetime.utcnow(),
                **{k: v for k, v in data.items() if k not in ['_id', 'created_by', 'created_at']}
            }
            
            result = mongo.db.documents.update_one(
                {'_id': ObjectId(document_id), 'created_by': ObjectId(user_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                return self.get_document(document_id, user_id)
            return None
        except Exception as e:
            self.logger.error(f"Error updating document: {str(e)}")
            return None
    
    def delete_document(self, document_id: str, user_id: str) -> bool:
        """Delete a document."""
        try:
            result = mongo.db.documents.delete_one({
                '_id': ObjectId(document_id),
                'created_by': ObjectId(user_id)
            })
            return result.deleted_count > 0
        except Exception as e:
            self.logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def list_documents(self, user_id: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """List documents for a user."""
        try:
            query = {'created_by': ObjectId(user_id)}
            if filters:
                query.update(filters)
                
            documents = list(mongo.db.documents.find(query).sort('created_at', -1))
            
            # Convert ObjectIds to strings
            for doc in documents:
                doc['_id'] = str(doc['_id'])
                doc['created_by'] = str(doc['created_by'])
            
            return documents
        except Exception as e:
            self.logger.error(f"Error listing documents: {str(e)}")
            return []
    
    def search_documents(self, query: str, user_id: str) -> List[Dict[str, Any]]:
        """Search documents by text."""
        try:
            documents = list(mongo.db.documents.find({
                'created_by': ObjectId(user_id),
                '$text': {'$search': query}
            }).sort('created_at', -1))
            
            # Convert ObjectIds to strings
            for doc in documents:
                doc['_id'] = str(doc['_id'])
                doc['created_by'] = str(doc['created_by'])
            
            return documents
        except Exception as e:
            self.logger.error(f"Error searching documents: {str(e)}")
            return [] 