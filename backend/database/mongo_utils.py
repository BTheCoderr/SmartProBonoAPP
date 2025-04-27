from typing import Optional, TypeVar, Dict, Any, List, Union, Sequence, cast
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from bson import ObjectId
import logging
from flask import current_app

logger = logging.getLogger(__name__)

T = TypeVar('T')
Document = Dict[str, Any]
QueryFilter = Dict[str, Any]
UpdateOperations = Dict[str, Any]
SortOption = List[tuple[str, int]]

class MongoDBError(Exception):
    """Custom exception for MongoDB operations."""
    pass

def get_mongo_db() -> Database:
    """Get MongoDB database instance."""
    if not hasattr(current_app, 'mongo') or not current_app.mongo:
        raise MongoDBError("MongoDB not initialized")
    db = current_app.mongo.db
    if not db:
        raise MongoDBError("MongoDB database not available")
    return cast(Database, db)

def get_collection(name: str) -> Collection:
    """Get MongoDB collection by name."""
    db = get_mongo_db()
    collection = db.get_collection(name)
    if not collection:
        raise MongoDBError(f"Collection {name} not found")
    return collection

def safe_insert_one(collection_name: str, document: Document) -> InsertOneResult:
    """Safely insert one document into a collection."""
    try:
        collection = get_collection(collection_name)
        result = collection.insert_one(document)
        return result
    except Exception as e:
        logger.error(f"Error inserting document into {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to insert document: {str(e)}")

def safe_insert_many(collection_name: str, documents: List[Document]) -> List[ObjectId]:
    """Safely insert multiple documents with type checking."""
    try:
        collection = get_collection(collection_name)
        result = collection.insert_many(documents)
        return cast(List[ObjectId], result.inserted_ids)
    except Exception as e:
        logger.error(f"Error inserting documents into {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to insert documents: {str(e)}")

def safe_find_one(collection_name: str, query: Document) -> Optional[Document]:
    """Safely find one document in a collection."""
    try:
        collection = get_collection(collection_name)
        result = collection.find_one(query)
        return result if result else None
    except Exception as e:
        logger.error(f"Error finding document in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to find document: {str(e)}")

def safe_find(
    collection_name: str,
    query: QueryFilter,
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[SortOption] = None,
    projection: Optional[Dict[str, Union[int, bool]]] = None
) -> List[Document]:
    """
    Safely find documents with type checking.
    
    Args:
        collection_name: Name of the collection
        query: Query filter
        skip: Number of documents to skip
        limit: Maximum number of documents to return
        sort: List of (field, direction) pairs for sorting
        projection: Projection for the query
        
    Returns:
        List of found documents
    """
    try:
        collection = get_collection(collection_name)
        cursor = collection.find(query, projection) if projection else collection.find(query)
        
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
            
        return list(cursor)
    except Exception as e:
        logger.error(f"Error finding documents in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to find documents: {str(e)}")

def safe_update_one(collection_name: str, filter_query: Document, update: Document) -> UpdateResult:
    """Safely update one document in a collection."""
    try:
        collection = get_collection(collection_name)
        result = collection.update_one(filter_query, update)
        return result
    except Exception as e:
        logger.error(f"Error updating document in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to update document: {str(e)}")

def safe_update_many(
    collection_name: str,
    query: QueryFilter,
    update: UpdateOperations,
    upsert: bool = False
) -> int:
    """Safely update multiple documents with type checking."""
    try:
        collection = get_collection(collection_name)
        result: UpdateResult = collection.update_many(query, update, upsert=upsert)
        return result.modified_count
    except Exception as e:
        logger.error(f"Error updating documents in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to update documents: {str(e)}")

def safe_delete_one(collection_name: str, query: QueryFilter) -> bool:
    """Safely delete one document with type checking."""
    try:
        collection = get_collection(collection_name)
        result: DeleteResult = collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error deleting document from {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to delete document: {str(e)}")

def safe_delete_many(collection_name: str, query: QueryFilter) -> int:
    """Safely delete multiple documents with type checking."""
    try:
        collection = get_collection(collection_name)
        result: DeleteResult = collection.delete_many(query)
        return result.deleted_count
    except Exception as e:
        logger.error(f"Error deleting documents from {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to delete documents: {str(e)}")

def safe_count_documents(collection_name: str, query: QueryFilter) -> int:
    """
    Safely count documents with type checking.
    
    Args:
        collection_name: Name of the collection
        query: Query filter
        
    Returns:
        Number of matching documents
    """
    try:
        collection = get_collection(collection_name)
        return collection.count_documents(query)
    except Exception as e:
        logger.error(f"Error counting documents in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to count documents: {str(e)}")

def safe_aggregate(collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Document]:
    """Safely perform an aggregation pipeline on a collection."""
    try:
        collection = get_collection(collection_name)
        return list(collection.aggregate(pipeline))
    except Exception as e:
        logger.error(f"Error performing aggregation on {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to perform aggregation: {str(e)}")

def safe_distinct(
    collection_name: str,
    field: str,
    query: Optional[QueryFilter] = None
) -> List[Any]:
    """Safely get distinct values with type checking."""
    try:
        collection = get_collection(collection_name)
        return collection.distinct(field, query)
    except Exception as e:
        logger.error(f"Error getting distinct values in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to get distinct values: {str(e)}")

def safe_bulk_write(
    collection_name: str,
    operations: List[Dict[str, Any]],
    ordered: bool = True
) -> Dict[str, int]:
    """Safely perform bulk write operations with type checking."""
    try:
        collection = get_collection(collection_name)
        result = collection.bulk_write(operations, ordered=ordered)
        return {
            'inserted': result.inserted_count,
            'updated': result.modified_count,
            'deleted': result.deleted_count
        }
    except Exception as e:
        logger.error(f"Error performing bulk write in {collection_name}: {str(e)}")
        raise MongoDBError(f"Failed to perform bulk write: {str(e)}")

def object_id_to_str(obj: Union[Document, List[Document]]) -> Union[Document, List[Document]]:
    """Convert ObjectId to string in a document or list of documents."""
    if isinstance(obj, list):
        return [object_id_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            k: str(v) if isinstance(v, ObjectId) else object_id_to_str(v) if isinstance(v, (dict, list)) else v
            for k, v in obj.items()
        }
    return obj 