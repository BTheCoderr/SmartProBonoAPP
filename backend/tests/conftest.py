import os
import sys
import pytest
from flask import Flask
import json
from datetime import datetime, timedelta

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from app import create_app
from models.user import User
from models.case import Case
from models.document import Document
from services.case_service import CaseService
from services.user_service import UserService
from services.document_template_engine import DocumentTemplateEngine
from ai.document_analyzer import DocumentAnalyzer
from ai.vector_db_manager import VectorDatabaseManager
from services.legal_assistant_service import LegalAssistantService

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app(testing=True)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test_secret_key',
        'TEMPLATES_DIR': os.path.join(os.path.dirname(__file__), '..', 'templates'),
    })
    
    # Create tables in the in-memory database
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up / reset resources
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    """Create a fresh database session for tests."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Create a session bound to the connection
        session = db.create_scoped_session(
            options={"bind": connection, "binds": {}}
        )
        
        db.session = session
        
        yield session
        
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing."""
    return {'Authorization': 'Bearer test_token'}

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        id='test-user-id',
        email='test@example.com',
        password='hashed_password',
        role='client',
        first_name='Test',
        last_name='User'
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def sample_lawyer(db_session):
    """Create a sample lawyer for testing."""
    lawyer = User(
        id='test-lawyer-id',
        email='lawyer@example.com',
        password='hashed_password',
        role='volunteer_attorney',
        first_name='Test',
        last_name='Lawyer',
        practice_areas='Immigration,Family Law',
        years_of_experience=5,
        languages='English,Spanish',
        state='CA',
        availability='Weekdays 9-5'
    )
    db_session.add(lawyer)
    db_session.commit()
    return lawyer

@pytest.fixture
def sample_case(db_session, sample_user, sample_lawyer):
    """Create a sample case for testing."""
    case = Case(
        id='test-case-id',
        title='Test Case',
        description='This is a test case',
        case_type='IMMIGRATION',
        status='NEW',
        priority='MEDIUM',
        client_id=sample_user.id,
        lawyer_id=sample_lawyer.id
    )
    db_session.add(case)
    db_session.commit()
    return case

@pytest.fixture
def sample_document(db_session, sample_case, sample_user):
    """Create a sample document for testing."""
    document = Document(
        id='test-document-id',
        title='Test Document',
        description='This is a test document',
        document_type='LEGAL_FORM',
        status='DRAFT',
        case_id=sample_case.id,
        created_by=sample_user.id,
        file_path='/path/to/test/document.pdf',
        file_size=12345,
        file_type='pdf'
    )
    db_session.add(document)
    db_session.commit()
    return document

@pytest.fixture
def case_service(db_session):
    """Create a case service for testing."""
    return CaseService(session=db_session)

@pytest.fixture
def user_service(db_session):
    """Create a user service for testing."""
    return UserService(session=db_session)

@pytest.fixture
def document_template_engine():
    """Create a document template engine for testing."""
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return DocumentTemplateEngine(templates_dir=templates_dir)

@pytest.fixture
def document_analyzer():
    """Create a document analyzer for testing."""
    return DocumentAnalyzer(model_name="test-model")

@pytest.fixture
def mock_legal_data():
    """Mock legal data for testing."""
    return {
        "statutes": [
            {"id": "12345", "title": "Test Statute", "content": "This is a test statute"},
            {"id": "67890", "title": "Another Statute", "content": "This is another test statute"}
        ],
        "cases": [
            {"id": "case123", "title": "Test Case", "content": "This is a test case decision"},
            {"id": "case456", "title": "Another Case", "content": "This is another test case decision"}
        ]
    } 