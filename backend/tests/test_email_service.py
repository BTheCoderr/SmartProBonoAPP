import pytest
from unittest.mock import Mock, patch, MagicMock
from services.email_service import EmailService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@pytest.fixture
def email_service():
    """Create an email service instance with mocked SMTP."""
    with patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        service = EmailService()
        service._smtp = mock_server
        yield service

@pytest.fixture
def sample_email():
    """Create a sample email object."""
    return {
        'to': 'user@example.com',
        'subject': 'Test Email',
        'body': 'This is a test email',
        'from_name': 'Test Sender',
        'reply_to': 'support@example.com',
        'template_id': 'welcome_email',
        'template_data': {
            'user_name': 'John Doe',
            'activation_link': 'https://example.com/activate'
        }
    }

def test_send_email(email_service, sample_email):
    """Test sending a basic email."""
    result = email_service.send_email(
        to=sample_email['to'],
        subject=sample_email['subject'],
        body=sample_email['body']
    )
    
    assert result is True
    email_service._smtp.send_message.assert_called_once()
    args = email_service._smtp.send_message.call_args[0]
    assert isinstance(args[0], MIMEMultipart)
    assert args[0]['To'] == sample_email['to']
    assert args[0]['Subject'] == sample_email['subject']

def test_send_html_email(email_service, sample_email):
    """Test sending an HTML email."""
    html_content = '<h1>Test Email</h1><p>This is a test email</p>'
    
    result = email_service.send_html_email(
        to=sample_email['to'],
        subject=sample_email['subject'],
        html_content=html_content,
        text_content=sample_email['body']
    )
    
    assert result is True
    email_service._smtp.send_message.assert_called_once()
    args = email_service._smtp.send_message.call_args[0]
    assert isinstance(args[0], MIMEMultipart)
    assert args[0].get_content_type() == 'multipart/alternative'

def test_send_template_email(email_service, sample_email):
    """Test sending a templated email."""
    with patch.object(email_service, '_render_template') as mock_render:
        mock_render.return_value = (
            'Welcome John Doe',
            '<h1>Welcome John Doe</h1>'
        )
        
        result = email_service.send_template_email(
            to=sample_email['to'],
            template_id=sample_email['template_id'],
            template_data=sample_email['template_data']
        )
        
        assert result is True
        mock_render.assert_called_once_with(
            sample_email['template_id'],
            sample_email['template_data']
        )
        email_service._smtp.send_message.assert_called_once()

def test_send_bulk_emails(email_service):
    """Test sending bulk emails."""
    recipients = [
        {'email': 'user1@example.com', 'name': 'User 1'},
        {'email': 'user2@example.com', 'name': 'User 2'},
        {'email': 'user3@example.com', 'name': 'User 3'}
    ]
    subject = 'Bulk Test Email'
    body = 'This is a bulk test email'
    
    results = email_service.send_bulk_emails(
        recipients=recipients,
        subject=subject,
        body=body
    )
    
    assert len(results) == len(recipients)
    assert all(result['success'] for result in results)
    assert email_service._smtp.send_message.call_count == len(recipients)

def test_send_email_with_attachment(email_service, sample_email):
    """Test sending an email with attachment."""
    attachment_data = b'Test file content'
    attachment_name = 'test.txt'
    
    result = email_service.send_email_with_attachment(
        to=sample_email['to'],
        subject=sample_email['subject'],
        body=sample_email['body'],
        attachment_data=attachment_data,
        attachment_name=attachment_name
    )
    
    assert result is True
    email_service._smtp.send_message.assert_called_once()
    args = email_service._smtp.send_message.call_args[0]
    assert isinstance(args[0], MIMEMultipart)
    assert len(args[0].get_payload()) == 2  # Body + attachment

def test_smtp_connection_error():
    """Test handling SMTP connection error."""
    with patch('smtplib.SMTP_SSL') as mock_smtp:
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, 'Connection refused')
        
        with pytest.raises(smtplib.SMTPConnectError):
            EmailService().connect()

def test_smtp_authentication_error(email_service):
    """Test handling SMTP authentication error."""
    email_service._smtp.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Invalid credentials')
    
    with pytest.raises(smtplib.SMTPAuthenticationError):
        email_service.authenticate('user', 'wrong_password')

def test_render_template(email_service):
    """Test template rendering."""
    template_id = 'welcome'
    template_data = {'name': 'John Doe'}
    
    with patch('jinja2.Environment') as mock_env:
        mock_template = MagicMock()
        mock_template.render.return_value = 'Welcome John Doe'
        mock_env.get_template.return_value = mock_template
        
        text_content, html_content = email_service._render_template(
            template_id,
            template_data
        )
        
        assert isinstance(text_content, str)
        assert isinstance(html_content, str)
        mock_template.render.assert_called_with(template_data)

def test_email_validation(email_service, sample_email):
    """Test email validation."""
    invalid_email = 'invalid.email@'
    
    with pytest.raises(ValueError):
        email_service.send_email(
            to=invalid_email,
            subject=sample_email['subject'],
            body=sample_email['body']
        )

def test_retry_mechanism(email_service, sample_email):
    """Test email sending retry mechanism."""
    email_service._smtp.send_message.side_effect = [
        smtplib.SMTPServerDisconnected(),  # First attempt fails
        None  # Second attempt succeeds
    ]
    
    result = email_service.send_email(
        to=sample_email['to'],
        subject=sample_email['subject'],
        body=sample_email['body']
    )
    
    assert result is True
    assert email_service._smtp.send_message.call_count == 2

def test_email_queue(email_service):
    """Test email queuing system."""
    with patch.object(email_service, '_redis') as mock_redis:
        email_data = {
            'to': 'user@example.com',
            'subject': 'Test Email',
            'body': 'Test content'
        }
        
        email_service.queue_email(email_data)
        
        mock_redis.rpush.assert_called_once()
        args = mock_redis.rpush.call_args[0]
        assert 'email_queue' in args[0]

def test_process_email_queue(email_service):
    """Test processing email queue."""
    with patch.object(email_service, '_redis') as mock_redis:
        mock_redis.lpop.side_effect = [
            '{"to": "user1@example.com", "subject": "Test", "body": "Test"}',
            None  # Queue empty
        ]
        
        processed = email_service.process_email_queue()
        
        assert processed == 1
        assert email_service._smtp.send_message.call_count == 1

def test_email_tracking(email_service, sample_email):
    """Test email tracking functionality."""
    with patch.object(email_service, '_db') as mock_db:
        result = email_service.send_email_with_tracking(
            to=sample_email['to'],
            subject=sample_email['subject'],
            body=sample_email['body']
        )
        
        assert result is True
        mock_db.email_tracking.insert_one.assert_called_once()
        tracking_data = mock_db.email_tracking.insert_one.call_args[0][0]
        assert tracking_data['recipient'] == sample_email['to']
        assert tracking_data['subject'] == sample_email['subject'] 