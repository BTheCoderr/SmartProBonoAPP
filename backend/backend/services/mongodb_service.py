from typing import Dict, List, Optional
from bson import ObjectId
from datetime import datetime
from flask import current_app
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

class MongoDBService:
    def __init__(self, db_name: str = "smartprobono"):
        self.db_name = db_name
        self._db = None

    @property
    def db(self):
        if not self._db:
            self._db = current_app.mongo.db
        return self._db

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    async def store_document(self, document_data: Dict) -> str:
        """Store a new document in MongoDB."""
        document_data["created_at"] = datetime.utcnow()
        document_data["updated_at"] = datetime.utcnow()
        
        result: InsertOneResult = await self.get_collection("documents").insert_one(document_data)
        return str(result.inserted_id)

    async def update_document(self, document_id: str, update_data: Dict) -> bool:
        """Update an existing document."""
        update_data["updated_at"] = datetime.utcnow()
        
        result: UpdateResult = await self.get_collection("documents").update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def get_document(self, document_id: str) -> Optional[Dict]:
        """Retrieve a document by ID."""
        return await self.get_collection("documents").find_one({"_id": ObjectId(document_id)})

    async def list_documents(self, filters: Dict = None, skip: int = 0, limit: int = 20) -> List[Dict]:
        """List documents with optional filtering and pagination."""
        cursor = self.get_collection("documents").find(filters or {})
        cursor = cursor.skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID."""
        result: DeleteResult = await self.get_collection("documents").delete_one(
            {"_id": ObjectId(document_id)}
        )
        return result.deleted_count > 0

    async def search_documents(self, query: str, skip: int = 0, limit: int = 20) -> List[Dict]:
        """Search documents using text search."""
        cursor = self.get_collection("documents").find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})])
        
        cursor = cursor.skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

# Create a singleton instance
mongodb_service = MongoDBService() 