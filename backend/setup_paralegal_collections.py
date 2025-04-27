import os
import json
import sys
import pymongo
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/smartprobono')

def setup_paralegal_collections():
    """Initialize collections for the paralegal feature"""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        db = client.get_database()
        
        print(f"Connected to MongoDB: {MONGO_URI}")
        
        # Create collections if they don't exist
        if 'cases' not in db.list_collection_names():
            db.create_collection('cases')
            print("Created 'cases' collection")
        
        if 'document_templates' not in db.list_collection_names():
            db.create_collection('document_templates')
            print("Created 'document_templates' collection")
            
            # Insert sample document templates
            templates = [
                {
                    'name': 'Client Intake Form',
                    'category': 'General',
                    'format': 'PDF',
                    'template_content': 'Sample client intake form template',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'name': 'Fee Waiver Request',
                    'category': 'Court',
                    'format': 'DOCX',
                    'template_content': 'Sample fee waiver request template',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'name': 'Client Representation Agreement',
                    'category': 'Contracts',
                    'format': 'PDF',
                    'template_content': 'Sample client representation agreement template',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'name': 'Tenant Complaint Letter',
                    'category': 'Housing',
                    'format': 'DOCX',
                    'template_content': 'Sample tenant complaint letter template',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'name': 'Employment Discrimination Complaint',
                    'category': 'Employment',
                    'format': 'PDF',
                    'template_content': 'Sample employment discrimination complaint template',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            ]
            db.document_templates.insert_many(templates)
            print(f"Added {len(templates)} sample document templates")
        
        if 'screening_questions' not in db.list_collection_names():
            db.create_collection('screening_questions')
            print("Created 'screening_questions' collection")
            
            # Insert sample screening questions
            questions = [
                {
                    'question': 'Have you sought legal help for this issue before?',
                    'type': 'boolean',
                    'category': 'general',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'question': 'When did this issue first occur?',
                    'type': 'date',
                    'category': 'general',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'question': 'Please describe your current financial situation',
                    'type': 'text',
                    'category': 'eligibility',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'question': 'Do you have any deadlines or court dates approaching?',
                    'type': 'boolean',
                    'category': 'urgency',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                },
                {
                    'question': 'What is your preferred language for communication?',
                    'type': 'select',
                    'options': ['English', 'Spanish', 'Mandarin', 'Vietnamese', 'Other'],
                    'category': 'communication',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            ]
            db.screening_questions.insert_many(questions)
            print(f"Added {len(questions)} sample screening questions")
        
        print("Paralegal collections setup completed successfully")
        
    except Exception as e:
        print(f"Error setting up paralegal collections: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_paralegal_collections() 