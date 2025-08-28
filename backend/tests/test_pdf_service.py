"""Test cases for PDF generation service"""
import unittest
import os
import tempfile
from services.pdf_service import PDFService, get_pdf_service
from weasyprint import HTML
from pypdf import PdfReader
from datetime import datetime
import pytest
import shutil

class TestPDFService(unittest.TestCase):
    def setUp(self):
        self.pdf_service = PDFService()
        self.test_data = {
            'court_name': 'Superior Court of California',
            'case_number': 'SC-2024-123',
            'plaintiff_name': 'John Smith',
            'plaintiff_address': '123 Main St, Anytown, CA 12345',
            'plaintiff_phone': '(555) 123-4567',
            'plaintiff_email': 'john.smith@example.com',
            'defendant_name': 'ABC Corporation',
            'defendant_address': '456 Business Ave, Anytown, CA 12345',
            'claim_amount': 5000.00,
            'claim_reason': 'Breach of contract for services rendered but not paid.',
            'evidence_list': [
                'Service Contract dated Jan 1, 2024',
                'Invoice #12345',
                'Email correspondence'
            ],
            'witness_list': [
                {'name': 'Jane Doe', 'relation': 'Project Manager'},
                {'name': 'Bob Wilson', 'relation': 'Account Representative'}
            ],
            'filing_date': datetime.now().strftime('%B %d, %Y')
        }
        # Create a temp directory for test outputs
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temp directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_legal_document_pdf(self):
        """Test generating a PDF legal document."""
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            self.test_data
        )
        
        # Verify the file exists and is a PDF
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.pdf'))
        
        # Read the generated PDF
        reader = PdfReader(output_path)
        
        # Check metadata
        self.assertEqual(reader.metadata['/Title'], 'Legal Document - small_claims_form')
        self.assertEqual(reader.metadata['/Author'], 'SmartProBono')
        self.assertEqual(reader.metadata['/Subject'], 'Legal Document')
        self.assertTrue(reader.metadata['/Keywords'].startswith('DOC-'))
        
        # Extract text from the first page
        text = reader.pages[0].extract_text()
        
        # Verify content
        self.assertIn('Superior Court of California', text)
        self.assertIn('SC-2024-123', text)
        self.assertIn('John Smith', text)
        self.assertIn('ABC Corporation', text)
        self.assertIn('$5,000.00', text)
        self.assertIn('Breach of contract', text)
        self.assertIn('Service Contract dated Jan 1, 2024', text)
        self.assertIn('Jane Doe', text)
        self.assertIn('Project Manager', text)
        
        # Clean up
        os.unlink(output_path)

    def test_generate_with_watermark(self):
        """Test generating a PDF with a watermark."""
        data = {
            'court_name': 'Test Court',
            'case_number': 'TEST-123',
            'plaintiff_name': 'Test Plaintiff',
            'plaintiff_address': 'Test Address',
            'plaintiff_phone': '555-0000',
            'plaintiff_email': 'test@example.com',
            'defendant_name': 'Test Defendant',
            'defendant_address': 'Test Address',
            'claim_amount': 1000.00,
            'claim_reason': 'Test claim',
            'evidence_list': ['Test evidence'],
            'witness_list': [{'name': 'Test Witness', 'relation': 'Test'}],
            'filing_date': datetime.now().strftime('%B %d, %Y')
        }
        
        # Generate base HTML
        template = self.pdf_service.jinja_env.get_template('legal/small_claims_form.html')
        html_content = template.render(**data)
        
        # Add watermark
        watermark = self.pdf_service.add_watermark(html_content, 'DRAFT - NOT FOR FILING')
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            data,
            output_format='pdf'
        )
        
        # Verify watermark in PDF
        reader = PdfReader(output_path)
        text = reader.pages[0].extract_text()
        self.assertIn('DRAFT - NOT FOR FILING', text)
        
        # Clean up
        os.unlink(output_path)

    def test_generate_with_header_footer(self):
        """Test generating a PDF with custom header and footer."""
        data = {
            'court_name': 'Test Court',
            'case_number': 'TEST-123',
            'plaintiff_name': 'Test Plaintiff',
            'plaintiff_address': 'Test Address',
            'plaintiff_phone': '555-0000',
            'plaintiff_email': 'test@example.com',
            'defendant_name': 'Test Defendant',
            'defendant_address': 'Test Address',
            'claim_amount': 1000.00,
            'claim_reason': 'Test claim',
            'evidence_list': ['Test evidence'],
            'witness_list': [{'name': 'Test Witness', 'relation': 'Test'}],
            'filing_date': datetime.now().strftime('%B %d, %Y')
        }
        
        # Generate base HTML
        template = self.pdf_service.jinja_env.get_template('legal/small_claims_form.html')
        html_content = template.render(**data)
        
        # Add header and footer
        header_footer = self.pdf_service.add_header_footer(
            html_content,
            header_text='CONFIDENTIAL',
            footer_text='For Settlement Purposes Only'
        )
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            data,
            output_format='pdf'
        )
        
        # Verify header and footer in PDF
        reader = PdfReader(output_path)
        text = reader.pages[0].extract_text()
        self.assertIn('CONFIDENTIAL', text)
        self.assertIn('For Settlement Purposes Only', text)
        
        # Clean up
        os.unlink(output_path)

    def test_get_pdf_service(self):
        """Test getting the PDF service singleton."""
        service = get_pdf_service()
        self.assertIsInstance(service, PDFService)

    def test_invalid_output_format(self):
        """Test handling of invalid output format."""
        with self.assertRaises(Exception):
            self.pdf_service.generate_legal_document(
                'small_claims_form',
                self.test_data,
                output_format='invalid_format'
            )

    def test_pdf_encryption(self):
        """Test encrypting a PDF document."""
        # Generate a PDF
        pdf_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            self.test_data
        )
        
        # Encrypt the PDF
        password = "s3cureP@ssw0rd"
        encrypted_path = self.pdf_service.encrypt_pdf(pdf_path, password)
        
        # Check if encrypted file was created
        self.assertTrue(os.path.exists(encrypted_path))
        self.assertTrue(encrypted_path.endswith('.enc'))
        
        # Verify file sizes
        self.assertGreater(os.path.getsize(encrypted_path), 0)
        
        # Clean up
        os.unlink(pdf_path)
        os.unlink(encrypted_path)

    def test_pdf_decryption(self):
        """Test decrypting an encrypted PDF document."""
        # Generate a PDF
        pdf_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            self.test_data
        )
        
        # Get original file size for comparison
        original_size = os.path.getsize(pdf_path)
        
        # Encrypt the PDF
        password = "s3cureP@ssw0rd"
        encrypted_path = self.pdf_service.encrypt_pdf(pdf_path, password)
        
        # Decrypt the PDF
        decrypted_path = self.pdf_service.decrypt_pdf(encrypted_path, password)
        
        # Check if decrypted file was created
        self.assertTrue(os.path.exists(decrypted_path))
        
        # Verify file sizes - decrypted should match original
        decrypted_size = os.path.getsize(decrypted_path)
        self.assertEqual(original_size, decrypted_size)
        
        # Clean up
        os.unlink(pdf_path)
        os.unlink(encrypted_path)
        os.unlink(decrypted_path)

    def test_generate_encrypted_document(self):
        """Test generating an encrypted PDF document directly."""
        password = "s3cureP@ssw0rd"
        
        # Generate an encrypted PDF
        encrypted_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            self.test_data,
            encryption_password=password
        )
        
        # Check if encrypted file was created
        self.assertTrue(os.path.exists(encrypted_path))
        self.assertTrue(encrypted_path.endswith('.enc'))
        
        # Decrypt the PDF
        decrypted_path = self.pdf_service.decrypt_pdf(encrypted_path, password)
        
        # Check if decrypted file was created
        self.assertTrue(os.path.exists(decrypted_path))
        
        # Clean up
        os.unlink(encrypted_path)
        os.unlink(decrypted_path)

    def test_decrypt_with_wrong_password(self):
        """Test decrypting with an incorrect password."""
        # Generate a PDF
        pdf_path = self.pdf_service.generate_legal_document(
            'small_claims_form',
            self.test_data
        )
        
        # Encrypt the PDF
        correct_password = "s3cureP@ssw0rd"
        encrypted_path = self.pdf_service.encrypt_pdf(pdf_path, correct_password)
        
        # Try to decrypt with wrong password
        wrong_password = "wr0ngP@ssw0rd"
        with self.assertRaises(Exception) as context:
            self.pdf_service.decrypt_pdf(encrypted_path, wrong_password)
        
        self.assertIn("Failed to decrypt PDF", str(context.exception))
        
        # Clean up
        os.unlink(pdf_path)
        os.unlink(encrypted_path)

@pytest.fixture
def pdf_service():
    return PDFService()

@pytest.fixture
def sample_small_claims_data():
    return {
        "title": "Small Claims Complaint",
        "description": "Test small claims complaint",
        "plaintiff": {
            "name": "John Doe",
            "address": "123 Main St, Anytown, ST 12345",
            "phone": "(555) 123-4567",
            "email": "john.doe@email.com"
        },
        "defendant": {
            "name": "ABC Company",
            "address": "456 Business Ave, Anytown, ST 12345",
            "phone": "(555) 987-6543",
            "email": "contact@abccompany.com"
        },
        "caseNumber": "SC-2024-123",
        "court": {
            "name": "Superior Court of California",
            "county": "Sacramento",
            "state": "CA"
        },
        "claim": {
            "amount": 5000.00,
            "description": "Unpaid services rendered",
            "date": "2024-01-15",
            "location": "Sacramento, CA"
        },
        "claimType": "breach_of_contract",
        "facts": [
            "On January 15, 2024, I provided consulting services to defendant",
            "The agreed-upon fee was $5,000",
            "Despite multiple requests, payment has not been received"
        ],
        "evidence": [
            "Service agreement dated January 10, 2024",
            "Invoice #12345 dated January 15, 2024",
            "Email correspondence regarding payment"
        ],
        "witnesses": [
            {
                "name": "Jane Smith",
                "relation": "Project Manager",
                "testimony": "Can verify the completion of services"
            }
        ],
        "settlementAttempts": [
            {
                "date": "2024-02-01",
                "method": "Email",
                "outcome": "No response received"
            },
            {
                "date": "2024-02-15",
                "method": "Certified Mail",
                "outcome": "Letter returned unclaimed"
            }
        ],
        "filingDate": "2024-03-01",
        "filingFee": 75.00,
        "exhibits": [
            {
                "name": "Exhibit A",
                "description": "Service Agreement",
                "type": "contract"
            },
            {
                "name": "Exhibit B",
                "description": "Invoice",
                "type": "document"
            }
        ]
    }

@pytest.mark.asyncio
async def test_generate_small_claims_form(pdf_service, sample_small_claims_data):
    # Test basic PDF generation
    result = await pdf_service.generateLegalDocument(
        "small_claims_form",
        sample_small_claims_data
    )
    
    assert result["filename"].startswith("small_claims_form-")
    assert result["filename"].endswith(".pdf")
    assert os.path.exists(result["path"])
    assert result["size"] > 0

@pytest.mark.asyncio
async def test_generate_with_watermark(pdf_service, sample_small_claims_data):
    # Test PDF generation with watermark
    result = await pdf_service.generateLegalDocument(
        "small_claims_form",
        sample_small_claims_data,
        {"watermark": "DRAFT"}
    )
    
    assert result["filename"].startswith("small_claims_form-")
    assert os.path.exists(result["path"])

@pytest.mark.asyncio
async def test_generate_with_letterhead(pdf_service, sample_small_claims_data):
    # Test PDF generation with letterhead
    letterhead = {
        "companyName": "SmartProBono Legal Services",
        "address": "123 Legal Street\nLegal City, ST 12345",
        "contact": "Tel: (555) 123-4567"
    }
    
    result = await pdf_service.generateLegalDocument(
        "small_claims_form",
        sample_small_claims_data,
        {"letterhead": letterhead}
    )
    
    assert result["filename"].startswith("small_claims_form-")
    assert os.path.exists(result["path"])

@pytest.mark.asyncio
async def test_generate_with_encryption(pdf_service, sample_small_claims_data):
    # Test PDF generation with encryption
    result = await pdf_service.generateLegalDocument(
        "small_claims_form",
        sample_small_claims_data,
        {"encrypt": True}
    )
    
    assert result["filename"].startswith("small_claims_form-")
    assert os.path.exists(result["path"] + ".enc")

@pytest.mark.asyncio
async def test_missing_required_fields(pdf_service):
    # Test validation of required fields
    incomplete_data = {
        "title": "Incomplete Form",
        "plaintiff": {
            "name": "John Doe",
            "address": "123 Main St"
        }
    }
    
    with pytest.raises(ValueError) as exc_info:
        await pdf_service.generateLegalDocument(
            "small_claims_form",
            incomplete_data
        )
    
    assert "Missing required fields" in str(exc_info.value)

@pytest.mark.asyncio
async def test_invalid_date_format(pdf_service, sample_small_claims_data):
    # Test date format validation
    invalid_data = dict(sample_small_claims_data)
    invalid_data["claim"]["date"] = "01/15/2024"  # Wrong format
    
    with pytest.raises(ValueError) as exc_info:
        await pdf_service.generateLegalDocument(
            "small_claims_form",
            invalid_data
        )
    
    assert "Invalid date format" in str(exc_info.value)

@pytest.mark.asyncio
async def test_invalid_currency_amount(pdf_service, sample_small_claims_data):
    # Test currency amount validation
    invalid_data = dict(sample_small_claims_data)
    invalid_data["claim"]["amount"] = "5000.999"  # Invalid cents
    
    with pytest.raises(ValueError) as exc_info:
        await pdf_service.generateLegalDocument(
            "small_claims_form",
            invalid_data
        )
    
    assert "Invalid currency amount" in str(exc_info.value)

def test_cleanup(pdf_service):
    # Test cleanup of generated files
    test_file = "test-cleanup.pdf"
    open(os.path.join(pdf_service.outputPath, test_file), 'a').close()
    
    pdf_service.cleanup_old_files()
    
    assert not os.path.exists(os.path.join(pdf_service.outputPath, test_file))

if __name__ == '__main__':
    unittest.main() 