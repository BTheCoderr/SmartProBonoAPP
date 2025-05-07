"""
Pytest configuration for production testing
"""
import pytest
from flask import Flask
from backend.app import create_app
from backend.extensions import db
from backend.models.user import User
from backend.models.template import Template
from datetime import datetime
import os
from pathlib import Path
import shutil

def get_prod_test_config():
    """Get production-like test configuration"""
    return {
        'TESTING': True,
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'production-secret-key'),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'production-jwt-secret'),
        'SQLALCHEMY_DATABASE_URI': os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/smartprobono_test'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'MONGO_URI': os.environ.get('MONGO_TEST_URI', 'mongodb://localhost:27017/smartprobono_test'),
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': os.environ.get('MAIL_PORT'),
        'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS', True),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
        'UPLOAD_FOLDER': os.environ.get('UPLOAD_FOLDER', '/tmp/smartprobono_test_uploads'),
        'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB max file size
    }

@pytest.fixture(scope='session')
def app():
    """Create test Flask application with production-like settings"""
    app = create_app(get_prod_test_config())
    
    with app.app_context():
            db.create_all()
        
        # Set up upload directory
        upload_dir = Path(app.config['UPLOAD_FOLDER'])
        upload_dir.mkdir(parents=True, exist_ok=True)
    
    yield app
    
        # Cleanup
        db.session.remove()
            db.drop_all()
        
        # Clean up upload directory
        if upload_dir.exists():
            shutil.rmtree(upload_dir)

@pytest.fixture(scope='function')
def session(app):
    """Create a new database session for each test"""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        
        db.session = session
        
        yield session
        
        transaction.rollback()
        connection.close()
        session.remove()

@pytest.fixture(scope='function')
def test_user(session):
    """Create a real test user"""
        user = User(
            email="test@example.com",
            role="user",
            first_name="Test",
            last_name="User",
            active=True
        )
    user.set_password("test_password")
    session.add(user)
    session.commit()
        return user

@pytest.fixture(scope='function')
def test_admin(session):
    """Create a real admin user"""
        admin = User(
            email="admin@example.com",
            role="admin",
            first_name="Admin",
            last_name="User",
            active=True
        )
    admin.set_password("admin_password")
    session.add(admin)
    session.commit()
        return admin

@pytest.fixture(scope='function')
def template(session):
    """Create a real template for testing"""
        template = Template(
            template_id="test_template_1",
            name="Test Template",
            title="Test Form Template",
            fields={"field1": "text", "field2": "number"},
            version="1.0",
            is_active=True
        )
    session.add(template)
    session.commit()
        return template

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    ) 