"""
Mock MongoDB module to simulate database functionality
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class MockMongo:
    """
    Mock MongoDB client that simulates MongoDB functionality
    without requiring an actual MongoDB connection
    """
    def __init__(self):
        logger.info("Initializing mock MongoDB client")
        self._collections = {}
        self._db = MockDatabase(self)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        logger.info("Mock MongoDB initialized with Flask app")
        return self
    
    def db(self):
        """Get database reference"""
        return self._db
    
    def get_db(self):
        """Get database reference"""
        return self._db

class MockDatabase:
    """Mock database that simulates MongoDB database functionality"""
    def __init__(self, client):
        self.client = client
        self._collections = {}
    
    def __getattr__(self, name):
        """Get a collection by name"""
        if name not in self._collections:
            self._collections[name] = MockCollection(name)
        return self._collections[name]

class MockCollection:
    """Mock collection that simulates MongoDB collection functionality"""
    def __init__(self, name):
        self.name = name
        self._documents = []
        self._id_counter = 1
    
    def find(self, query=None, projection=None, skip=0, limit=0, sort=None):
        """Find documents in the collection"""
        logger.debug(f"Mock find: {query}, {projection}, {skip}, {limit}, {sort}")
        # Simple implementation that ignores all parameters
        return MockCursor(self._documents)
    
    def find_one(self, query=None, projection=None):
        """Find a single document in the collection"""
        logger.debug(f"Mock find_one: {query}, {projection}")
        for doc in self._documents:
            # Very simple match logic, just for demonstration
            if query is None or all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None
    
    def insert_one(self, document):
        """Insert a document into the collection"""
        logger.debug(f"Mock insert_one: {document}")
        # Add a mock _id if not present
        if '_id' not in document:
            document['_id'] = str(self._id_counter)
            self._id_counter += 1
        self._documents.append(document.copy())
        return MockInsertOneResult(document['_id'])
    
    def insert_many(self, documents):
        """Insert multiple documents into the collection"""
        logger.debug(f"Mock insert_many: {len(documents)} documents")
        ids = []
        for doc in documents:
            result = self.insert_one(doc)
            ids.append(result.inserted_id)
        return MockInsertManyResult(ids)
    
    def update_one(self, filter, update, upsert=False):
        """Update a document in the collection"""
        logger.debug(f"Mock update_one: {filter}, {update}, {upsert}")
        for i, doc in enumerate(self._documents):
            if all(doc.get(k) == v for k, v in filter.items()):
                # Handle $set operation
                if '$set' in update:
                    for k, v in update['$set'].items():
                        self._documents[i][k] = v
                return MockUpdateResult(1, 1)
        
        # If no document found and upsert is True
        if upsert:
            new_doc = {**filter}
            if '$set' in update:
                new_doc.update(update['$set'])
            self.insert_one(new_doc)
            return MockUpdateResult(0, 1)
        
        return MockUpdateResult(0, 0)
    
    def delete_one(self, filter):
        """Delete a document from the collection"""
        logger.debug(f"Mock delete_one: {filter}")
        for i, doc in enumerate(self._documents):
            if all(doc.get(k) == v for k, v in filter.items()):
                del self._documents[i]
                return MockDeleteResult(1)
        return MockDeleteResult(0)
    
    def delete_many(self, filter):
        """Delete multiple documents from the collection"""
        logger.debug(f"Mock delete_many: {filter}")
        original_count = len(self._documents)
        self._documents = [doc for doc in self._documents 
                          if not all(doc.get(k) == v for k, v in filter.items())]
        deleted_count = original_count - len(self._documents)
        return MockDeleteResult(deleted_count)
    
    def count_documents(self, filter):
        """Count documents in the collection"""
        logger.debug(f"Mock count_documents: {filter}")
        count = 0
        for doc in self._documents:
            if all(doc.get(k) == v for k, v in filter.items()):
                count += 1
        return count

class MockCursor:
    """Mock cursor for query results"""
    def __init__(self, documents):
        self._documents = documents
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position >= len(self._documents):
            raise StopIteration
        document = self._documents[self._position]
        self._position += 1
        return document
    
    def limit(self, limit):
        """Limit the number of results"""
        # This is a simplification
        return self
    
    def skip(self, skip):
        """Skip results"""
        # This is a simplification
        return self
    
    def sort(self, key_or_list, direction=None):
        """Sort results"""
        # This is a simplification
        return self

class MockInsertOneResult:
    """Mock result of insert_one operation"""
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id
        self.acknowledged = True

class MockInsertManyResult:
    """Mock result of insert_many operation"""
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids
        self.acknowledged = True

class MockUpdateResult:
    """Mock result of update operations"""
    def __init__(self, matched_count, modified_count):
        self.matched_count = matched_count
        self.modified_count = modified_count
        self.acknowledged = True
        self.upserted_id = None

class MockDeleteResult:
    """Mock result of delete operations"""
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count
        self.acknowledged = True

# Export a mock MongoDB client
mongo = MockMongo() 