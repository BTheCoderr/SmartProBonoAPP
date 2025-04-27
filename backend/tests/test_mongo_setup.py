import logging
import sys
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_direct_mongo_connection() -> bool:
    """Test direct MongoDB connection without Flask."""
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ Direct MongoDB connection successful")
        client.close()
        return True
    except ConnectionFailure as e:
        logger.error(f"❌ Direct MongoDB connection failed: {e}")
        return False

def test_case_operations(client: MongoClient) -> bool:
    """Test CRUD operations for cases collection."""
    try:
        db = client['probono']
        cases = db['cases']
        
        # Test document
        test_case = {
            "title": "Test Case",
            "description": "Test case for MongoDB operations",
            "status": "test"
        }
        
        # Insert
        result = cases.insert_one(test_case)
        case_id = result.inserted_id
        logger.info(f"✅ Successfully inserted test case with ID: {case_id}")
        
        # Find
        found_case = cases.find_one({"_id": case_id})
        if not found_case:
            raise Exception("Could not find inserted case")
        logger.info("✅ Successfully found test case")
        
        # Update
        update_result = cases.update_one(
            {"_id": case_id},
            {"$set": {"status": "updated"}}
        )
        if update_result.modified_count != 1:
            raise Exception("Failed to update case")
        logger.info("✅ Successfully updated test case")
        
        # Delete
        delete_result = cases.delete_one({"_id": case_id})
        if delete_result.deleted_count != 1:
            raise Exception("Failed to delete case")
        logger.info("✅ Successfully deleted test case")
        
        return True
    except Exception as e:
        logger.error(f"❌ Case operations test failed: {e}")
        return False

def main():
    """Run all MongoDB tests."""
    logger.info("Starting MongoDB setup tests...")
    
    # Test direct connection first
    if not test_direct_mongo_connection():
        logger.error("Direct MongoDB connection test failed. Stopping tests.")
        sys.exit(1)
    
    # Test case operations
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    try:
        if not test_case_operations(client):
            logger.error("Case operations test failed.")
            sys.exit(1)
        logger.info("✅ All MongoDB tests passed successfully!")
    finally:
        client.close()

if __name__ == "__main__":
    main() 