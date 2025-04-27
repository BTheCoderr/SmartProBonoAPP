"""MongoDB database manager"""
import os
import pymongo
from urllib.parse import urlparse
import logging
from pymongo.server_api import ServerApi
import threading
from typing import Optional, Dict, Any, cast, Union
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

logger = logging.getLogger(__name__)

class MongoManager:
    """Singleton class to manage MongoDB connection"""
    _instance = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    _collections: Dict[str, Collection] = {}
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize MongoManager without connecting immediately"""
        self.logger = logging.getLogger(__name__)
        self._initialized = False

    @property
    def db(self) -> Optional[Database]:
        """Get the MongoDB database instance"""
        return self._db

    def is_connected(self) -> bool:
        """Check if MongoDB connection is active"""
        return self._db is not None

    def init_app(self, app) -> None:
        """Initialize with Flask app"""
        if not self._initialized:
            uri = app.config['MONGO_URI']
            self.init_client(uri)
            self._initialized = True

    def init_client(self, uri: str) -> None:
        """Initialize MongoDB client with the given URI"""
        try:
            self._client = MongoClient(uri)
            db_name = urlparse(uri).path.lstrip('/')
            self._db = cast(Database, self._client[db_name])
            logger.info(f"Connected to MongoDB database: {db_name}")
            
            # Initialize collections
            if self._db is not None:
                self._collections = {
                    'users': self._db.users,
                    'cases': self._db.cases,
                    'documents': self._db.documents,
                    'notifications': self._db.notifications,
                    'intakes': self._db.intakes,
                    'form_templates': self._db.form_templates
                }
            
                # Ensure indexes
                self._ensure_indexes()
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {str(e)}")
            raise

    def _ensure_indexes(self) -> None:
        """Create necessary indexes on collections"""
        if self._db is None:
            raise RuntimeError("MongoDB client not initialized")
            
        try:
            # Users collection indexes
            users_collection = self.get_collection('users')
            if users_collection is not None:
                users_collection.create_index('email', unique=True)
            
            # Cases collection indexes
            cases_collection = self.get_collection('cases')
            if cases_collection is not None:
                cases_collection.create_index('client_id')
                cases_collection.create_index('lawyer_id')
            
            # Documents collection indexes
            docs_collection = self.get_collection('documents')
            if docs_collection is not None:
                docs_collection.create_index('case_id')
            
            # Notifications collection indexes
            notifs_collection = self.get_collection('notifications')
            if notifs_collection is not None:
                notifs_collection.create_index('user_id')
            
            # Intakes collection indexes
            intakes_collection = self.get_collection('intakes')
            if intakes_collection is not None:
                intakes_collection.create_index('client_id')
            
            # Form templates collection indexes
            templates_collection = self.get_collection('form_templates')
            if templates_collection is not None:
                templates_collection.create_index('name', unique=True)
            
        except Exception as e:
            logger.warning(f"Failed to create some indexes: {str(e)}")

    def get_collection(self, name: str) -> Optional[Collection]:
        """Get a MongoDB collection by name"""
        return self._collections.get(name)

    def close(self) -> None:
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self._collections = {}
            self._initialized = False

    def ensure_indexes(self) -> None:
        """Create indexes for collections"""
        if not self._initialized:
            raise RuntimeError("MongoDB client not initialized. Call init_client() first.")
        
        try:
            # Create indexes for cases collection
            cases_collection = self.get_collection('cases')
            if cases_collection is not None:
                cases_collection.create_index([('created_at', pymongo.DESCENDING)])
                cases_collection.create_index([('client_name', pymongo.ASCENDING)])
                cases_collection.create_index([('status', pymongo.ASCENDING)])
            
            self.logger.info("Successfully created MongoDB indexes")
        except Exception as e:
            self.logger.error(f"Failed to create indexes: {str(e)}")
            raise

# Create a singleton instance
mongo = MongoManager() 