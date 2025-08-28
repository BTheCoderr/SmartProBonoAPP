"""MongoDB database module."""
from flask_pymongo import PyMongo
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional
import logging

# Initialize MongoDB
mongo = PyMongo()

def get_db() -> Optional[Database]:
    """Get MongoDB database instance."""
    try:
        return mongo.db
    except Exception as e:
        logging.error(f"Error getting MongoDB database: {str(e)}")
        return None

def get_collection(collection_name: str) -> Optional[Collection]:
    """Get MongoDB collection by name."""
    db = get_db()
    if db is None:
        return None
    try:
        return db[collection_name]
    except Exception as e:
        logging.error(f"Error getting collection {collection_name}: {str(e)}")
        return None 