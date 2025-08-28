"""Test cases for legal document templates endpoints"""
import pytest
from datetime import datetime, timedelta
import json
from io import BytesIO
from unittest.mock import patch, MagicMock
from pypdf import PdfReader
import re
from weasyprint import HTML
import os
import tempfile
from weasyprint import CSS
from services.pdf_service import PDFService
from models.template import Template

def test_get_templates(client):
    """Test getting all templates."""
    response = client.get('/templates')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 4  # We have 4 templates
    
    # Check template structure
    template = data[0]
    assert 'id' in template
    assert 'name' in template
    assert 'description' in template
    assert 'fields' in template
    assert isinstance(template['fields'], list)

def test_get_template_valid(client):
    """Test getting a specific valid template."""
    response = client.get('/templates/expungement')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 'expungement'
    assert data['name'] == 'Expungement Letter'
    assert isinstance(data['fields'], list)

def test_get_template_invalid(client):
    """Test getting a non-existent template."""
    response = client.get('/templates/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

@pytest.mark.parametrize('template_id,valid_data', [
    ('expungement', {
        'court_name': 'Superior Court of California',
        'case_number': 'CR123-456',
        'defendant_name': 'John Doe',
        'defendant_address': '123 Main St, City, ST 12345',
        'defendant_phone': '+11234567890',
        'defendant_email': 'john@example.com',
        'offense_date': '2020-01-01',
        'offense_description': 'Minor offense description',
        'conviction_date': '2020-02-01',
        'sentence_description': 'Community service',
        'completion_date': '2021-02-01',
        'attorney_name': 'Jane Smith',
        'attorney_bar_number': 'ABC123',
        'attorney_phone': '+11234567890',
        'attorney_email': 'jane@lawfirm.com'
    }),
    ('eviction', {
        'court_name': 'Housing Court',
        'case_number': 'HC789-012',
        'tenant_name': 'Alice Johnson',
        'tenant_phone': '+11234567890',
        'tenant_email': 'alice@example.com',
        'landlord_name': 'Property LLC',
        'landlord_address': '456 Oak St, City, ST 12345',
        'property_address': '789 Pine St, City, ST 12345',
        'lease_start_date': '2022-01-01',
        'monthly_rent': 1500,
        'notice_date': '2023-01-01',
        'notice_type': 'Non-Payment',
        'response_reasons': ['Payment was made', 'Maintenance issues'],
        'relief_requested': 'Dismiss eviction notice'
    }),
    ('small_claims', {
        'court_name': 'Small Claims Court',
        'plaintiff_name': 'Bob Wilson',
        'plaintiff_address': '321 Elm St, City, ST 12345',
        'plaintiff_phone': '+11234567890',
        'plaintiff_email': 'bob@example.com',
        'defendant_name': 'Service Corp',
        'defendant_address': '654 Oak St, City, ST 12345',
        'claim_amount': 5000,
        'claim_type': 'Contract Dispute',
        'claim_reason': 'Failed to provide agreed services',
        'incident_date': '2023-06-01',
        'evidence_list': ['Contract', 'Email communications'],
        'filing_date': '2023-07-01',
        'service_method': 'Certified Mail'
    }),
    ('tenant_rights', {
        'state_name': 'California',
        'max_security_deposit': 'Two months\' rent',
        'deposit_return_timeline': '21 days',
        'emergency_contact': '911 for emergencies',
        'emergency_maintenance_procedures': 'Call maintenance hotline',
        'month_to_month_notice': '30 days',
        'fixed_term_notice': '60 days',
        'eviction_notice_period': '3 days for non-payment',
        'rent_increase_rules': 'Maximum 10% per year',
        'legal_aid_contact': 'Legal Aid Society',
        'legal_aid_hours': 'Mon-Fri 9am-5pm',
        'housing_authority_contact': 'Housing Authority',
        'housing_authority_hours': 'Mon-Fri 8am-4pm',
        'tenant_org_contact': 'Tenants Union',
        'tenant_org_services': ['Counseling', 'Education', 'Advocacy'],
        'fair_housing_contact': 'Fair Housing Office',
        'current_date': datetime.now().strftime('%Y-%m-%d')
    })
])
def test_generate_document_valid(client, auth_tokens, template_id, valid_data):
    """Test generating documents with valid data."""
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = client.post(
        f'/generate/{template_id}',
        json=valid_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
    assert isinstance(response.data, bytes)

@pytest.mark.parametrize('template_id,invalid_data,expected_errors', [
    ('expungement', {
        'court_name': 'A' * 101,  # Exceeds max_length
        'case_number': 'invalid-case-number',  # Invalid pattern
        'defendant_phone': '123',  # Invalid phone
        'defendant_email': 'invalid-email',  # Invalid email
        'offense_date': '2020-13-45'  # Invalid date
    }, ['Court Name must be at most 100 characters',
        'Case Number has an invalid format',
        'Defendant Phone must be a valid phone number',
        'Defendant Email must be a valid email address',
        'Date of Offense must be a valid date (YYYY-MM-DD)']),
    ('small_claims', {
        'claim_amount': 'not-a-number',  # Invalid number
        'claim_type': 'Invalid Type',  # Invalid option
        'filing_date': 'invalid-date'  # Invalid date
    }, ['Claim Amount must be a number',
        'Type of Claim must be one of: Contract Dispute, Property Damage, Personal Injury, Unpaid Debt, Other',
        'Filing Date must be a valid date (YYYY-MM-DD)'])
])
def test_generate_document_invalid(client, auth_tokens, template_id, invalid_data, expected_errors):
    """Test generating documents with invalid data."""
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = client.post(
        f'/generate/{template_id}',
        json=invalid_data,
        headers=headers
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'validation_errors' in data
    for error in expected_errors:
        assert error in data['validation_errors']

def test_generate_document_unauthorized(client):
    """Test generating document without authentication."""
    response = client.post('/generate/expungement', json={})
    assert response.status_code == 401

def test_generate_document_not_found(client, auth_tokens):
    """Test generating document with invalid template ID."""
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = client.post(
        '/generate/nonexistent',
        json={},
        headers=headers
    )
    assert response.status_code == 404

def test_generate_document_no_data(client, auth_tokens):
    """Test generating document without providing data."""
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = client.post(
        '/generate/expungement',
        json=None,
        headers=headers
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'No data provided'

@patch('backend.routes.legal_templates.generate_pdf_from_template')
def test_generate_document_pdf_error(mock_generate_pdf, client, auth_tokens):
    """Test handling PDF generation errors."""
    mock_generate_pdf.side_effect = Exception('PDF generation failed')
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = client.post(
        '/generate/expungement',
        json={'court_name': 'Test Court'},
        headers=headers
    )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['error'] == 'Failed to generate PDF'

def test_field_validation():
    """Test field validation functions."""
    from backend.routes.legal_templates import validate_phone, validate_email, validate_date
    
    # Test phone validation
    assert validate_phone('+11234567890')
    assert validate_phone('11234567890')
    assert not validate_phone('123')
    assert not validate_phone('abcdefghijk')
    
    # Test email validation
    assert validate_email('test@example.com')
    assert validate_email('user.name+tag@example.co.uk')
    assert not validate_email('invalid.email')
    assert not validate_email('@example.com')
    
    # Test date validation
    assert validate_date('2023-12-31')
    assert validate_date('2024-02-29')  # Leap year
    assert not validate_date('2023-13-01')  # Invalid month
    assert not validate_date('2023-04-31')  # Invalid day
    assert not validate_date('invalid-date')

class TestPDFGeneration:
    @pytest.fixture
    def pdf_service(self):
        return PDFService()

    @pytest.fixture
    def mock_template(self):
        return Template(
            template_id="test_template",
            name="Test Template",
            title="Test Form Template",
            fields=[{
                "name": "title",
                "type": "text",
                "required": True
            }, {
                "name": "content",
                "type": "text",
                "required": True
            }],
            version="1.0",
            is_active=True
        )

    def test_pdf_metadata(self, pdf_service, mock_template):
        """Test that PDF metadata is correctly set"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            data = {"title": "Test", "content": "Content"}
            output_path = pdf_service.generate_legal_document(
                template_id=mock_template.template_id,
                data=data,
                output_format='pdf'
            )
            
            reader = PdfReader(output_path)
            info = reader.metadata
            
            assert info.get('/Title') == "Test Document"
            assert info.get('/Author') == "SmartProBono"
            assert info.get('/Subject') == "Legal Document"
            assert info.get('/Producer').startswith('WeasyPrint')
            
            os.unlink(output_path)

    def test_pdf_formatting(self, pdf_service, mock_template):
        """Test PDF formatting and content"""
        data = {
            "title": "Small Claims Court",
            "amount": "$5,000.00",
            "date": "January 15, 2024"
        }
        output_path = pdf_service.generate_legal_document(
            mock_template.template_id,
            data,
            output_format='pdf'
        )
        
        # Extract text from PDF
        reader = PdfReader(output_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        assert "Small Claims Court" in text
        assert "$5,000.00" in text
        assert "January 15, 2024" in text
        
        os.unlink(output_path)

    def test_pdf_attachments(self, pdf_service, mock_template):
        """Test PDF attachments and template rendering"""
        data = {
            "title": "Tenant Rights",
            "content": "Important legal information"
        }
        
        with patch('weasyprint.HTML') as mock_html:
            output_path = pdf_service.generate_legal_document(
                mock_template.template_id,
                data,
                output_format='pdf'
            )
            mock_html.assert_called_once()
            
            # Verify HTML content
            html_content = mock_html.call_args[0][0]
            assert "Tenant Rights" in html_content
            assert "Important legal information" in html_content
            
            os.unlink(output_path)

    def test_date_formatting(self, pdf_service):
        """Test date formatting in PDFs"""
        test_date = datetime(2024, 1, 15)
        formatted = test_date.strftime('%B %d, %Y')
        assert formatted == "January 15, 2024"
        
        # Test with different date
        test_date = datetime(2023, 12, 31)
        formatted = test_date.strftime('%B %d, %Y')
        assert formatted == "December 31, 2023"

    def test_currency_formatting(self, pdf_service):
        """Test currency formatting in PDFs"""
        def format_currency(value):
            return "${:,.2f}".format(float(value))
            
        assert format_currency(1000) == "$1,000.00"
        assert format_currency(1000.50) == "$1,000.50"
        assert format_currency(999999.99) == "$999,999.99"
        assert format_currency(0) == "$0.00"

    def test_document_id_generation(self, pdf_service, mock_template):
        """Test unique document ID generation"""
        data = {"title": "Test", "content": "Content"}
        
        # Generate two PDFs in quick succession
        output_path1 = pdf_service.generate_legal_document(
            mock_template.template_id,
            data,
            output_format='pdf'
        )
        output_path2 = pdf_service.generate_legal_document(
            mock_template.template_id,
            data,
            output_format='pdf'
        )
        
        reader1 = PdfReader(output_path1)
        reader2 = PdfReader(output_path2)
        
        # Extract document IDs from metadata
        doc_id1 = reader1.metadata.get('/Keywords', '')
        doc_id2 = reader2.metadata.get('/Keywords', '')
        
        # Verify they are different
        assert doc_id1 != doc_id2
        assert doc_id1.startswith('DOC-')
        assert doc_id2.startswith('DOC-')
        
        os.unlink(output_path1)
        os.unlink(output_path2) 