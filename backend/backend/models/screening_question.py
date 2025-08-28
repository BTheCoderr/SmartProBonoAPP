from bson import ObjectId
from database import db

class ScreeningQuestion:
    @staticmethod
    def create(question_data):
        """Create a new screening question in the database"""
        result = db.screening_questions.insert_one(question_data)
        return result.inserted_id
    
    @staticmethod
    def find(query=None):
        """Find screening questions matching the query"""
        query = query or {}
        cursor = db.screening_questions.find(query)
        # Convert ObjectId to string for JSON serialization
        questions = []
        for question in cursor:
            question['_id'] = str(question['_id'])
            questions.append(question)
        return questions
    
    @staticmethod
    def find_one(query):
        """Find a single screening question matching the query"""
        question = db.screening_questions.find_one(query)
        if question:
            question['_id'] = str(question['_id'])
        return question
    
    @staticmethod
    def update_one(query, update_data):
        """Update a screening question in the database"""
        result = db.screening_questions.update_one(query, update_data)
        return result.modified_count
    
    @staticmethod
    def delete_one(query):
        """Delete a screening question from the database"""
        result = db.screening_questions.delete_one(query)
        return result.deleted_count 