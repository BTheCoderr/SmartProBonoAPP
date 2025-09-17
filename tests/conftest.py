"""
Test Configuration and Fixtures
Shared configuration for all tests
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

@pytest.fixture(scope="session")
def test_config():
    """Test configuration settings"""
    return {
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'CORS_ORIGINS': ['http://localhost:3000'],
        'DEBUG': True
    }

@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_requests():
    """Mock requests library for external API calls"""
    with patch('requests.post') as mock_post, \
         patch('requests.get') as mock_get:
        yield {
            'post': mock_post,
            'get': mock_get
        }

@pytest.fixture
def mock_email_service():
    """Mock email service for testing"""
    with patch('services.email_service.send_email') as mock_send:
        mock_send.return_value = True
        yield mock_send

@pytest.fixture
def mock_slack_service():
    """Mock Slack service for testing"""
    with patch('services.slack_service.send_message') as mock_send:
        mock_send.return_value = True
        yield mock_send

@pytest.fixture
def mock_websocket():
    """Mock WebSocket service for testing"""
    with patch('services.websocket_service.send_message') as mock_send:
        mock_send.return_value = True
        yield mock_send

@pytest.fixture
def sample_immigration_case():
    """Sample immigration case data for testing"""
    return {
        'id': 'TEST-CASE-001',
        'clientName': 'John Doe',
        'caseType': 'Asylum',
        'status': 'New',
        'priority': 'High',
        'description': 'Test asylum case',
        'dueDate': '2024-12-31',
        'documents': [],
        'createdAt': '2024-01-01T00:00:00Z',
        'updatedAt': '2024-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_court_filing():
    """Sample court filing data for testing"""
    return {
        'id': 'TEST-FILING-001',
        'case_id': 'CASE-001',
        'document_type': 'complaint',
        'title': 'Test Complaint',
        'description': 'Test court filing',
        'status': 'draft',
        'court': 'Superior Court',
        'jurisdiction': 'Rhode Island',
        'filed_by': 'Test Attorney',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_voice_command():
    """Sample voice command data for testing"""
    return {
        'text': 'What are my legal options for immigration?',
        'user_id': 'test_user',
        'language': 'en-US',
        'confidence': 0.95
    }

@pytest.fixture
def sample_analytics_data():
    """Sample analytics data for testing"""
    return {
        'user': {
            'total_users': 100,
            'active_users': 50,
            'new_users_today': 5
        },
        'performance': {
            'response_time': 200,
            'uptime': 99.9,
            'error_rate': 0.1
        },
        'business': {
            'total_cases': 500,
            'revenue': 10000,
            'conversion_rate': 15.5
        },
        'security': {
            'threats_blocked': 10,
            'vulnerabilities': 2,
            'last_scan': '2024-01-01T00:00:00Z'
        }
    }

@pytest.fixture
def mock_ai_response():
    """Mock AI analysis response for testing"""
    return {
        'success': True,
        'analysis': {
            'case_summary': 'This is a test case summary',
            'key_facts': [
                'Fact 1: Client is seeking asylum',
                'Fact 2: Client has been in the US for 2 years'
            ],
            'practical_advice': [
                'Advice 1: Gather supporting documentation',
                'Advice 2: Consult with immigration attorney'
            ]
        },
        'disclaimers': [
            'This is not legal advice',
            'Consult with a qualified attorney'
        ],
        'warnings': [],
        'recommendations': [
            'File Form I-589',
            'Prepare supporting evidence'
        ]
    }

@pytest.fixture
def mock_legal_forms():
    """Mock legal forms data for testing"""
    return {
        'success': True,
        'forms': [
            {
                'id': 'form_589',
                'name': 'Application for Asylum and for Withholding of Removal',
                'description': 'Form I-589 for asylum applications',
                'jurisdiction': 'Federal',
                'category': 'Immigration',
                'url': 'https://www.uscis.gov/i-589'
            },
            {
                'id': 'form_485',
                'name': 'Application to Register Permanent Residence',
                'description': 'Form I-485 for green card applications',
                'jurisdiction': 'Federal',
                'category': 'Immigration',
                'url': 'https://www.uscis.gov/i-485'
            }
        ]
    }

@pytest.fixture
def mock_court_rules():
    """Mock court rules data for testing"""
    return {
        'success': True,
        'rules': [
            {
                'jurisdiction': 'Rhode Island',
                'court': 'Superior Court',
                'rule_number': 'Civ. R. 5',
                'title': 'Service and Filing of Pleadings',
                'description': 'Rules for serving and filing court documents',
                'requirements': [
                    'All pleadings must be filed with the clerk',
                    'Service must be made within 20 days of filing'
                ],
                'deadlines': {
                    'answer_to_complaint': 20,
                    'motion_response': 10
                },
                'fees': {
                    'complaint': 150.0,
                    'motion': 25.0
                },
                'forms': ['Civil Cover Sheet', 'Summons'],
                'electronic_filing': True,
                'efiling_system': 'Rhode Island eFiling'
            }
        ]
    }

@pytest.fixture
def mock_filing_templates():
    """Mock filing templates data for testing"""
    return {
        'success': True,
        'templates': [
            {
                'id': 'complaint_template',
                'name': 'Civil Complaint Template',
                'document_type': 'complaint',
                'jurisdiction': 'Rhode Island',
                'court': 'Superior Court',
                'required_fields': [
                    'plaintiff_name',
                    'defendant_name',
                    'cause_of_action',
                    'damages_sought'
                ],
                'optional_fields': [
                    'attorney_info',
                    'exhibits',
                    'witnesses'
                ],
                'instructions': 'Complete all required fields and file with the court clerk.'
            }
        ]
    }

@pytest.fixture
def mock_websocket_message():
    """Mock WebSocket message for testing"""
    return {
        'type': 'notification',
        'message': 'Test notification message',
        'user_id': 'test_user',
        'timestamp': '2024-01-01T00:00:00Z'
    }

@pytest.fixture
def mock_audit_event():
    """Mock audit event for testing"""
    return {
        'event_type': 'user_login',
        'user_id': 'test_user',
        'timestamp': '2024-01-01T00:00:00Z',
        'ip_address': '127.0.0.1',
        'user_agent': 'Test Browser',
        'details': {
            'success': True,
            'method': 'password'
        }
    }

@pytest.fixture
def mock_security_event():
    """Mock security event for testing"""
    return {
        'event_type': 'failed_login',
        'user_id': 'test_user',
        'timestamp': '2024-01-01T00:00:00Z',
        'ip_address': '192.168.1.100',
        'severity': 'medium',
        'description': 'Multiple failed login attempts',
        'details': {
            'attempt_count': 5,
            'time_window': '5 minutes'
        }
    }

@pytest.fixture
def mock_performance_event():
    """Mock performance event for testing"""
    return {
        'event_type': 'slow_query',
        'timestamp': '2024-01-01T00:00:00Z',
        'severity': 'low',
        'description': 'Database query took longer than expected',
        'details': {
            'query_time': 2.5,
            'threshold': 2.0,
            'query_type': 'SELECT'
        }
    }

@pytest.fixture(autouse=True)
def cleanup_mocks():
    """Clean up mocks after each test"""
    yield
    # Cleanup happens automatically when fixtures go out of scope

@pytest.fixture
def mock_file_upload():
    """Mock file upload for testing"""
    return {
        'filename': 'test_document.pdf',
        'content_type': 'application/pdf',
        'size': 1024,
        'content': b'PDF content here'
    }

@pytest.fixture
def mock_document_data():
    """Mock document data for testing"""
    return {
        'id': 'TEST-DOC-001',
        'title': 'Test Document',
        'content': 'This is test document content',
        'type': 'legal_brief',
        'created_by': 'test_user',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z',
        'version': 1,
        'collaborators': ['test_user'],
        'permissions': {
            'test_user': 'edit'
        }
    }

# Test markers
def pytest_configure(config):
    """Configure test markers"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "websocket: marks tests that require WebSocket server"
    )
    config.addinivalue_line(
        "markers", "external: marks tests that require external services"
    )

# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers based on test names
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        if "websocket" in item.nodeid.lower():
            item.add_marker(pytest.mark.websocket)
        if "external" in item.nodeid.lower():
            item.add_marker(pytest.mark.external)

# Test reporting (console only - no HTML)

# Test warnings
def pytest_configure(config):
    """Configure pytest warnings"""
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
