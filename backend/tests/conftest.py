"""
Pytest configuration and fixtures
"""
import pytest
from flask import Flask
from backend import create_app
from backend.extensions import db
from backend.models.user import User
from datetime import datetime, timedelta
import jwt
import os
from pymongo.errors import ConnectionFailure, OperationFailure
import time
import socket
from contextlib import closing
from flask_jwt_extended import create_access_token
from backend.models.template import Template
import threading
from typing import Dict, Any, Generator, Optional
from backend.database.mongo import mongo
from pymongo.database import Database
from pymongo.collection import Collection
from backend.websocket import socketio
import shutil
from pathlib import Path

def find_free_port():
    """Find a free port to use for testing"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port

@pytest.fixture(scope='session')
def websocket_port():
    """Get a free port for WebSocket testing"""
    return find_free_port()

@pytest.fixture(scope='session')
def websocket_url(websocket_port):
    """Get WebSocket URL for testing"""
    return f'http://localhost:{websocket_port}'

@pytest.fixture(scope='session')
def socketio_server(app, websocket_port):
    """Start a SocketIO server for testing"""
    server_thread = threading.Thread(
        target=socketio.run,
        args=(app,),
        kwargs={'port': websocket_port, 'use_reloader': False}
    )
    server_thread.daemon = True
    server_thread.start()
    # Wait for server to start
    time.sleep(1)
    yield socketio
    socketio.stop()

@pytest.fixture
def socketio_client(websocket_url, auth_headers):
    """Create a SocketIO client for testing"""
    from socketio import Client
    client = Client()
    client.connect(
        websocket_url,
        headers=auth_headers,
        wait_timeout=1
    )
    yield client
    client.disconnect()

def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line(
        "markers",
        "websocket: mark test as requiring websocket server"
    )

def pytest_collection_modifyitems(config, items):
    """Skip websocket tests if server is not available"""
    skip_websocket = pytest.mark.skip(reason="WebSocket server not available")
    
    for item in items:
        if "websocket" in item.keywords:
            item.add_marker(skip_websocket)

def get_test_config() -> Dict[str, Any]:
    """Get test configuration"""
    return {
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key',
        'JWT_SECRET_KEY': 'test_jwt_secret',
        'SQLALCHEMY_DATABASE_URI': os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/smartprobono_test'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'MONGO_URI': 'mongodb://localhost:27017/smartprobono_test',
        'MAIL_SUPPRESS_SEND': True,
        'WTF_CSRF_ENABLED': False
    }

@pytest.fixture(scope='session')
def app() -> Generator[Flask, None, None]:
    """Create test Flask application"""
    app = create_app(get_test_config())
    
    with app.app_context():
        # Initialize SQL tables
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {str(e)}")
            pytest.skip("Could not create database tables. Make sure PostgreSQL is running and the user has the correct permissions.")
        
        # Initialize MongoDB and wait for connection
        retries = 5
        while retries > 0:
            try:
                mongo.init_client(app.config['MONGO_URI'])
                if mongo.is_connected():
                    # Clear all collections
                    for collection in mongo.db.list_collection_names():
                        mongo.db[collection].delete_many({})
                    break
            except ConnectionFailure:
                retries -= 1
                if retries == 0:
                    pytest.skip("MongoDB server is not available")
                time.sleep(1)
    
    yield app
    
    with app.app_context():
        # Cleanup
        db.session.remove()
        try:
            db.drop_all()
        except Exception as e:
            app.logger.warning(f"Failed to drop database tables: {str(e)}")
        
        if mongo.db is not None:
            for collection in mongo.db.list_collection_names():
                mongo.db[collection].delete_many({})
            mongo.close()

@pytest.fixture
def client(app: Flask):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(app: Flask, test_user) -> Dict[str, str]:
    """Create authentication headers for test user"""
    with app.app_context():
        access_token = create_access_token(identity=test_user.id)
    return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture(autouse=True)
def cleanup_databases(app: Flask) -> Generator[None, None, None]:
    """Clean up both SQL and MongoDB databases after each test"""
    with app.app_context():
        # Create all tables
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {str(e)}")
            pytest.skip("Could not create database tables. Make sure PostgreSQL is running and the user has the correct permissions.")
        
        # Initialize MongoDB connection
        try:
            if not mongo.is_connected():
                mongo.init_client(app.config['MONGO_URI'])
        except Exception as e:
            app.logger.error(f"Failed to initialize MongoDB: {str(e)}")
            pytest.skip("Could not initialize MongoDB connection")
        
        yield
        
        # Clean up SQL tables
        db.session.remove()
        try:
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
        except Exception as e:
            app.logger.warning(f"Failed to clean up database tables: {str(e)}")
        
        # Clean up MongoDB collections
        if mongo.is_connected():
            try:
                for collection in mongo.db.list_collection_names():
                    try:
                        mongo.db.drop_collection(collection)
                    except Exception as e:
                        app.logger.warning(f"Failed to drop MongoDB collection {collection}: {str(e)}")
            except Exception as e:
                app.logger.warning(f"Failed to list MongoDB collections: {str(e)}")

@pytest.fixture
def test_user(app: Flask) -> User:
    """Create a test user."""
    with app.app_context():
        user = User(
            email="test@example.com",
            role="user",
            first_name="Test",
            last_name="User",
            active=True
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_admin(app: Flask) -> User:
    """Create a test admin user."""
    with app.app_context():
        admin = User(
            email="admin@example.com",
            role="admin",
            first_name="Admin",
            last_name="User",
            active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def template(app: Flask, test_user) -> Template:
    """Create a test template."""
    with app.app_context():
        template = Template(
            template_id="test_template_1",
            name="Test Template",
            title="Test Form Template",
            fields={"field1": "text", "field2": "number"},
            version="1.0",
            is_active=True
        )
        db.session.add(template)
        db.session.commit()
        return template

@pytest.fixture(scope="session")
def upload_dir(app):
    """Create and manage the upload directory for document scanner tests."""
    test_upload_dir = Path(app.instance_path) / 'test_uploads' / 'scans'
    test_upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Override the upload folder in the scanner config
    from backend.routes.document_scanner import config
    config.upload_folder = test_upload_dir
    
    yield test_upload_dir
    
    # Clean up after all tests
    if test_upload_dir.exists():
        shutil.rmtree(test_upload_dir) 