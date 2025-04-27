from bson import ObjectId
from database import db

class DocumentTemplate:
    @staticmethod
    def create(template_data):
        """Create a new document template in the database"""
        result = db.document_templates.insert_one(template_data)
        return result.inserted_id
    
    @staticmethod
    def find(query=None):
        """Find document templates matching the query"""
        query = query or {}
        cursor = db.document_templates.find(query)
        # Convert ObjectId to string for JSON serialization
        templates = []
        for template in cursor:
            template['_id'] = str(template['_id'])
            templates.append(template)
        return templates
    
    @staticmethod
    def find_one(query):
        """Find a single document template matching the query"""
        template = db.document_templates.find_one(query)
        if template:
            template['_id'] = str(template['_id'])
        return template
    
    @staticmethod
    def update_one(query, update_data):
        """Update a document template in the database"""
        result = db.document_templates.update_one(query, update_data)
        return result.modified_count
    
    @staticmethod
    def delete_one(query):
        """Delete a document template from the database"""
        result = db.document_templates.delete_one(query)
        return result.deleted_count 