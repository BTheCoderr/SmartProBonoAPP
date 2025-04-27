"""Test cases for PDF generation service"""
import unittest
import os
import tempfile
from backend.services.pdf_service import PDFService, get_pdf_service
from weasyprint import HTML
from pypdf import PdfReader
from datetime import datetime

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

if __name__ == '__main__':
    unittest.main() 