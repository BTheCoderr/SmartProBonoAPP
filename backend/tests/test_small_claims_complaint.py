"""Tests for small claims complaint template generation"""
import os
import tempfile
import unittest
from datetime import datetime
from backend.services.pdf_service import PDFService, get_pdf_service
from pypdf import PdfReader

class TestSmallClaimsComplaint(unittest.TestCase):
    """Test case for small claims complaint template"""

    def setUp(self):
        """Set up test case with test data"""
        self.pdf_service = get_pdf_service()
        self.test_data = {
            "plaintiff_name": "Jane Doe",
            "plaintiff_address": "123 Main St, Anytown, CA 90210",
            "defendant_name": "ABC Corporation",
            "defendant_address": "456 Business Ave, Cityville, CA 90220",
            "court_county": "Los Angeles",
            "court_state": "California",
            "claim_amount": 3500.00,
            "claim_description": "Breach of contract for services rendered between January 1, 2023 and March 15, 2023.",
            "incident_location": "Los Angeles, California",
            "incident_date": "2023-02-15",
            "fact_1": "On January 1, 2023, Plaintiff entered into a written contract with Defendant for website development services.",
            "fact_2": "Plaintiff completed all services on February 28, 2023, as specified in the contract.",
            "fact_3": "Despite multiple attempts to collect payment, Defendant has failed to pay the agreed amount of $3,500.00.",
            "evidence_list": "1. Copy of written contract dated January 1, 2023\n2. Invoice #12345 dated March 1, 2023\n3. Email correspondence regarding payment",
            "witness_list": "1. John Smith, Project Manager\n2. Mary Johnson, Accounting Department",
            "filing_date": "2023-05-15",
            "filing_fee": 75.00,
            "case_number": "SC-2023-45678"
        }

    def test_generate_html(self):
        """Test HTML generation for small claims complaint"""
        # Generate HTML output
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_complaint',
            self.test_data,
            output_format='html'
        )
        
        try:
            # Check that the file exists
            self.assertTrue(os.path.exists(output_path))
            
            # Read the HTML content
            with open(output_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Check for key content
            self.assertIn('Jane Doe', html_content)
            self.assertIn('ABC Corporation', html_content)
            self.assertIn('Los Angeles', html_content)
            self.assertIn('California', html_content)
            self.assertIn('$3,500.00', html_content)
            self.assertIn('Breach of contract', html_content)
            self.assertIn('Copy of written contract', html_content)
            self.assertIn('John Smith', html_content)
            self.assertIn('SC-2023-45678', html_content)
            
            # Check for template structure
            self.assertIn('STATEMENT OF CLAIM', html_content)
            self.assertIn('PRAYER FOR RELIEF', html_content)
            self.assertIn('VERIFICATION', html_content)
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_generate_pdf(self):
        """Test PDF generation for small claims complaint"""
        # Generate PDF output
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_complaint',
            self.test_data
        )
        
        try:
            # Check that the file exists
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.pdf'))
            
            # Check the PDF metadata
            reader = PdfReader(output_path)
            metadata = reader.metadata
            
            self.assertEqual(metadata['/Author'], 'SmartProBono')
            self.assertEqual(metadata['/Subject'], 'Legal Document')
            self.assertEqual(metadata['/Title'], 'Legal Document - small_claims_complaint')
            
            # Extract text from the PDF
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            # Check for key content in the extracted text
            self.assertIn('Jane Doe', text)
            self.assertIn('ABC Corporation', text)
            self.assertIn('Los Angeles', text)
            self.assertIn('California', text)
            self.assertIn('$3,500.00', text)
            self.assertIn('Breach of contract', text)
            self.assertIn('written contract', text)
            self.assertIn('John Smith', text)
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_generate_pdf_with_watermark(self):
        """Test PDF generation with watermark"""
        # Generate PDF output with watermark
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_complaint',
            self.test_data,
            watermark_text="DRAFT"
        )
        
        try:
            # Check that the file exists
            self.assertTrue(os.path.exists(output_path))
            
            # We can't easily verify the watermark in the PDF content,
            # but we can check that the function completes successfully
            self.assertTrue(output_path.endswith('.pdf'))
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.unlink(output_path)
            
    def test_generate_pdf_with_headers_footers(self):
        """Test PDF generation with custom headers and footers"""
        # Generate PDF output with headers/footers
        output_path = self.pdf_service.generate_legal_document(
            'small_claims_complaint',
            self.test_data,
            header_text="CONFIDENTIAL",
            footer_text="For settlement purposes only"
        )
        
        try:
            # Check that the file exists
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.pdf'))
            
            # Again, we can't easily verify the headers/footers in extracted text,
            # but we can check that the function completes successfully
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.unlink(output_path)

if __name__ == '__main__':
    unittest.main() 