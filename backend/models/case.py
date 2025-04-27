from datetime import datetime
from bson import ObjectId
from backend.database.mongo import mongo
from backend.models.user import User
import logging
from typing import Optional, List, Dict, Any, cast
from pymongo.database import Database
from pymongo.collection import Collection

logger = logging.getLogger(__name__)

class Case:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.data['created_at'] = datetime.utcnow()
        self.data['updated_at'] = datetime.utcnow()

    def save(self) -> Optional[str]:
        """Save case to MongoDB if available"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - case will not be persisted")
                return None
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            result = db.cases.insert_one(self.data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save case to MongoDB: {str(e)}")
            return None

    @staticmethod
    def find_by_id(case_id: str) -> Optional[Dict[str, Any]]:
        """Find case by ID if MongoDB is available"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - cannot retrieve case")
                return None
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            return db.cases.find_one({'_id': ObjectId(case_id)})
        except Exception as e:
            logger.error(f"Failed to find case in MongoDB: {str(e)}")
            return None

    @staticmethod
    def find_all() -> List[Dict[str, Any]]:
        """Find all cases if MongoDB is available"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - cannot retrieve cases")
                return []
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            return list(db.cases.find())
        except Exception as e:
            logger.error(f"Failed to retrieve cases from MongoDB: {str(e)}")
            return []

    def update(self) -> bool:
        """Update case if MongoDB is available"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - case will not be updated")
                return False
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            result = db.cases.update_one(
                {'_id': ObjectId(self.data.get('_id'))},
                {'$set': {**self.data, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update case in MongoDB: {str(e)}")
            return False

    def delete(self) -> bool:
        """Delete case if MongoDB is available"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - case will not be deleted")
                return False
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            result = db.cases.delete_one({'_id': ObjectId(self.data.get('_id'))})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete case from MongoDB: {str(e)}")
            return False

class CaseStore:
    @staticmethod
    def create(case_data):
        """Create a new case in MongoDB"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - case will not be created")
                return None
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            case_data['created_at'] = datetime.utcnow()
            case_data['updated_at'] = datetime.utcnow()
            result = db.cases.insert_one(case_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create case in MongoDB: {str(e)}")
            return None
    
    @staticmethod
    def find(query=None):
        """Find cases matching the query"""
        query = query or {}
        db = mongo.db
        if db is None:
            logger.warning("MongoDB not available - cannot find cases")
            return []
            
        # After None check, we can safely assert the type
        db = cast(Database, db)
        cursor = db.cases.find(query)
        return [{**case, '_id': str(case['_id'])} for case in cursor]
    
    @staticmethod
    def find_one(query):
        """Find a single case matching the query"""
        try:
            db = mongo.db
            if db is None:
                logger.warning("MongoDB not available - cannot find case")
                return None
            
            # After None check, we can safely assert the type
            db = cast(Database, db)
            
            if '_id' in query and isinstance(query['_id'], str):
                query['_id'] = ObjectId(query['_id'])
            case = db.cases.find_one(query)
            if case:
                case['_id'] = str(case['_id'])
            return case
        except Exception as e:
            logger.error(f"Failed to find case in MongoDB: {str(e)}")
            return None
    @staticmethod
    def update_one(query, update_data):
        """Update a case in MongoDB"""
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        db = mongo.db
        if db is None:
            logger.warning("MongoDB not available - cannot update case")
            return 0
            
        # After None check, we can safely assert the type
        db = cast(Database, db)
        update_data['$set']['updated_at'] = datetime.utcnow()
        result = db.cases.update_one(query, update_data)
        return result.modified_count
    
    @staticmethod
    def delete_one(query):
        """Delete a case from MongoDB"""
        if '_id' in query and isinstance(query['_id'], str):
            query['_id'] = ObjectId(query['_id'])
        db = mongo.db
        if db is None:
            logger.warning("MongoDB not available - cannot delete case")
            return 0
            
        # After None check, we can safely assert the type
        db = cast(Database, db)
        result = db.cases.delete_one(query)
        return result.deleted_count