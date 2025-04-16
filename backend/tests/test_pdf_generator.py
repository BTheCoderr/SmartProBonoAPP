import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import io
from datetime import datetime

# Add the parent directory to sys.path to allow importing from parent modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.pdf_generator import PDFGenerator


class TestPDFGenerator(unittest.TestCase):
    """Test cases for the PDF Generator functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        self.pdf_generator = PDFGenerator()
        
        # Sample user data
        self.user_data = {
            "id": "user123",
            "name": "Test User",
            "email": "test@example.com"
        }
        
        # Sample document data for different templates
        self.demand_letter_data = {
            "recipientName": "John Doe",
            "recipientAddress": "123 Main St, Anytown, USA 12345",
            "demandAmount": "5000",
            "paymentDueDate": "2023-08-30",
            "description": "Unpaid services rendered",
            "desiredOutcome": "Full payment of the amount owed"
        }
        
        self.will_data = {
            "fullName": "Jane Smith",
            "address": "456 Oak Avenue, Cityville, USA 67890",
            "executorName": "Robert Smith",
            "executorAddress": "789 Pine Road, Townsville, USA 54321",
            "beneficiaries": "Spouse: 50%, Children: 25% each",
            "assets": "House, Car, Savings Account",
            "specificRequests": "Family heirlooms to my daughter",
            "funeralInstructions": "Cremation"
        }
        
        self.divorce_petition_data = {
            "petitionerName": "Alice Johnson",
            "petitionerAddress": "101 Maple Street, Stateville, USA 13579",
            "respondentName": "Bob Johnson",
            "respondentAddress": "202 Cedar Lane, Countyville, USA 24680",
            "marriageDate": "2010-06-15",
            "marriageLocation": "Las Vegas, Nevada",
            "separationDate": "2023-01-10",
            "groundsForDivorce": "Irreconcilable differences",
            "childrenNames": "Carol Johnson (12), David Johnson (9)",
            "propertyDivision": "Equal division of marital assets"
        }

    @patch('ai.pdf_generator.canvas.Canvas')
    def test_generate_demand_letter(self, mock_canvas):
        """Test generation of a demand letter."""
        # Set up canvas mock
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        mock_buffer = io.BytesIO()
        
        # Generate the PDF
        result = self.pdf_generator.generate_document(
            "demand_letter",
            self.demand_letter_data,
            self.user_data
        )
        
        # Assertions - verify canvas methods were called appropriately
        mock_canvas_instance.drawString.assert_called()
        mock_canvas_instance.save.assert_called_once()
        
        # Verify result structure
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('file_path', result)
        self.assertIn('demand_letter', result['file_path'])

    @patch('ai.pdf_generator.canvas.Canvas')
    def test_generate_will(self, mock_canvas):
        """Test generation of a will document."""
        # Set up canvas mock
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        
        # Generate the PDF
        result = self.pdf_generator.generate_document(
            "will",
            self.will_data,
            self.user_data
        )
        
        # Assertions
        mock_canvas_instance.drawString.assert_called()
        mock_canvas_instance.save.assert_called_once()
        
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('file_path', result)
        self.assertIn('will', result['file_path'])

    @patch('ai.pdf_generator.canvas.Canvas')
    def test_generate_divorce_petition(self, mock_canvas):
        """Test generation of a divorce petition."""
        # Set up canvas mock
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        
        # Generate the PDF
        result = self.pdf_generator.generate_document(
            "divorce_petition",
            self.divorce_petition_data,
            self.user_data
        )
        
        # Assertions
        mock_canvas_instance.drawString.assert_called()
        mock_canvas_instance.save.assert_called_once()
        
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('file_path', result)
        self.assertIn('divorce_petition', result['file_path'])

    def test_invalid_template(self):
        """Test handling of an invalid template name."""
        result = self.pdf_generator.generate_document(
            "nonexistent_template",
            {},
            self.user_data
        )
        
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('Template not found', result['error'])

    @patch('ai.pdf_generator.canvas.Canvas')
    def test_missing_required_data(self, mock_canvas):
        """Test handling of missing required data fields."""
        # Create data with missing fields
        incomplete_data = {
            "recipientName": "John Doe"
            # Missing other required fields
        }
        
        # Generate document with incomplete data
        result = self.pdf_generator.generate_document(
            "demand_letter",
            incomplete_data,
            self.user_data
        )
        
        # We expect it to handle missing fields gracefully
        # The implementation might either fail with an error or use default/empty values
        if not result.get('success', False):
            self.assertIn('error', result)
            self.assertIn('missing', result['error'].lower())
        else:
            # If it succeeds, canvas should have been called
            mock_canvas_instance = mock_canvas.return_value
            mock_canvas_instance.drawString.assert_called()
            mock_canvas_instance.save.assert_called_once()

    @patch('ai.pdf_generator.canvas.Canvas')
    @patch('ai.pdf_generator.os.path.exists')
    @patch('ai.pdf_generator.os.makedirs')
    def test_output_directory_creation(self, mock_makedirs, mock_path_exists, mock_canvas):
        """Test that output directories are created if they don't exist."""
        # Setup mocks
        mock_path_exists.return_value = False
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        
        # Generate document
        result = self.pdf_generator.generate_document(
            "demand_letter",
            self.demand_letter_data,
            self.user_data
        )
        
        # Verify directory creation was attempted
        mock_makedirs.assert_called()
        self.assertTrue(result['success'])

    @patch('ai.pdf_generator.canvas.Canvas')
    def test_filename_contains_timestamp(self, mock_canvas):
        """Test that generated filenames contain timestamps for uniqueness."""
        # Setup mock
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        
        # Get current date for comparison
        current_date = datetime.now().strftime("%Y%m%d")
        
        # Generate document
        result = self.pdf_generator.generate_document(
            "demand_letter",
            self.demand_letter_data,
            self.user_data
        )
        
        # Verify filename contains current date
        self.assertIn(current_date, result['file_path'])


if __name__ == '__main__':
    unittest.main() 