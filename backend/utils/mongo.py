"""MongoDB utility functions for Flask applications."""

from typing import Any, cast
from flask import current_app
from flask_pymongo import PyMongo
from pymongo.database import Database
from pymongo.collection import Collection

def get_mongo_db() -> Database:
    """
    Get the MongoDB database instance from the current Flask application.
    
    Returns:
        Database: The MongoDB database instance
        
    Raises:
        RuntimeError: If MongoDB is not initialized or database is not available
    """
    app: Any = current_app
    if not hasattr(app, 'mongo'):
        raise RuntimeError("MongoDB is not initialized")
    
    try:
        mongo = cast(PyMongo, app.mongo)
        if not hasattr(mongo, 'db'):
            raise RuntimeError("MongoDB database is not available")
        return cast(Database, mongo.db)
    except Exception as e:
        raise RuntimeError(f"Failed to get MongoDB database: {str(e)}")

def get_mongo_collection(collection_name: str) -> Collection:
    """
    Get a MongoDB collection by name.
    
    Args:
        collection_name: Name of the collection to get
        
    Returns:
        Collection: The MongoDB collection
        
    Raises:
        RuntimeError: If MongoDB is not initialized or collection is not available
    """
    db = get_mongo_db()
    
    try:
        collection = cast(Collection, db[collection_name])
        if not isinstance(collection, Collection):
            raise RuntimeError(f"Collection '{collection_name}' is not available")
        return collection
    except Exception as e:
        raise RuntimeError(f"Failed to get collection '{collection_name}': {str(e)}")
 