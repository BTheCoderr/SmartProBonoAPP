import os
import logging
import tempfile
import pytesseract
from PIL import Image
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class OCRService:
    """Service for extracting text and data from images using OCR"""
    
    def __init__(self):
        """Initialize the OCR service with default configurations"""
        # Configure pytesseract path if needed (uncomment and set if required)
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Linux
        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # macOS with Homebrew
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
        self.supported_formats = ['jpeg', 'jpg', 'png', 'bmp', 'tiff']
    
    def process_image(self, image_file, document_type='general'):
        """
        Process an image file using OCR to extract text and structured data
        
        Args:
            image_file: File object from request
            document_type: Type of document to process (general, identification, immigration, legal)
            
        Returns:
            dict: Extracted data and metadata
        """
        try:
            if not self._is_valid_image(image_file.filename):
                raise ValueError(f"Unsupported file format: {image_file.filename}")
            
            # Save temporary file
            temp_file = self._save_temp_file(image_file)
            
            # Extract text from image
            extracted_text = self._extract_text(temp_file)
            
            # Extract structured data based on document type
            extracted_data = self._extract_structured_data(extracted_text, document_type)
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return {
                "success": True,
                "extractedText": extracted_text,
                "extractedData": extracted_data,
                "documentType": document_type,
                "processingTimestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _is_valid_image(self, filename):
        """Check if the file format is supported"""
        if not filename:
            return False
        ext = filename.split('.')[-1].lower()
        return ext in self.supported_formats
    
    def _save_temp_file(self, image_file):
        """Save image to a temporary file"""
        try:
            # Create temp file with same extension
            ext = image_file.filename.split('.')[-1].lower()
            temp_file = tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False)
            temp_file_path = temp_file.name
            temp_file.close()
            
            # Save uploaded file to temp file
            image_file.save(temp_file_path)
            return temp_file_path
        except Exception as e:
            logger.error(f"Error saving temporary file: {str(e)}")
            raise
    
    def _extract_text(self, image_path):
        """Extract all text from an image using pytesseract"""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise
    
    def _extract_structured_data(self, text, document_type):
        """
        Extract structured data from text based on document type
        
        Args:
            text: Extracted text from image
            document_type: Type of document (identification, immigration, legal, general)
            
        Returns:
            dict: Structured data extracted from text
        """
        structured_data = {}
        
        if document_type == "identification":
            # Extract common ID document fields
            structured_data = self._extract_id_data(text)
        elif document_type == "immigration":
            # Extract immigration document specific data
            structured_data = self._extract_immigration_data(text)
        elif document_type == "legal":
            # Extract legal document data
            structured_data = self._extract_legal_data(text)
        else:
            # General document - extract any recognizable fields
            structured_data = self._extract_general_data(text)
        
        return structured_data
    
    def _extract_id_data(self, text):
        """Extract data from ID documents like driver's licenses, passports, etc."""
        data = {}
        
        # Extract name
        name_match = re.search(r"name[:\s]+([a-zA-Z\s]+)", text, re.IGNORECASE)
        if name_match:
            data["name"] = name_match.group(1).strip()
        
        # Extract date of birth
        dob_patterns = [
            r"(DOB|Date of Birth|Birth Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(DOB|Date of Birth|Birth Date)[:\s]+([a-zA-Z]{3,9}\s+\d{1,2},?\s+\d{2,4})"
        ]
        
        for pattern in dob_patterns:
            dob_match = re.search(pattern, text, re.IGNORECASE)
            if dob_match:
                data["dateOfBirth"] = dob_match.group(2).strip()
                break
        
        # Extract ID number
        id_match = re.search(r"(ID|License|DL|No|Number)[.:\s#]+([A-Z0-9-]+)", text, re.IGNORECASE)
        if id_match:
            data["idNumber"] = id_match.group(2).strip()
        
        # Extract address - common in ID cards and driver's licenses
        addr_match = re.search(r"(address|addr)[:\s]+(.+?)(?=\n\n|\n[A-Z]|$)", text, re.IGNORECASE)
        if addr_match:
            data["address"] = addr_match.group(2).strip().replace('\n', ', ')
        
        return data
    
    def _extract_immigration_data(self, text):
        """Extract data from immigration documents"""
        data = {}
        
        # Extract passport number
        passport_match = re.search(r"passport[.\s#:]+([A-Z0-9]+)", text, re.IGNORECASE)
        if passport_match:
            data["passportNumber"] = passport_match.group(1).strip()
        
        # Extract nationality
        nationality_match = re.search(r"nationality[:\s]+([a-zA-Z\s]+)", text, re.IGNORECASE)
        if nationality_match:
            data["nationality"] = nationality_match.group(1).strip()
        
        # Extract visa type
        visa_match = re.search(r"(visa type|visa)[:\s]+([a-zA-Z0-9-\s]+)", text, re.IGNORECASE)
        if visa_match:
            data["visaType"] = visa_match.group(2).strip()
        
        # Extract expiration date
        exp_match = re.search(r"(expiry date|expiration date|expiration|valid until)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.IGNORECASE)
        if exp_match:
            data["expirationDate"] = exp_match.group(2).strip()
        
        # Also include ID data as many immigration docs have similar fields
        id_data = self._extract_id_data(text)
        for key, value in id_data.items():
            if key not in data:
                data[key] = value
        
        return data
    
    def _extract_legal_data(self, text):
        """Extract data from legal documents"""
        data = {}
        
        # Extract case number if present
        case_match = re.search(r"(case|docket)[.\s#:]+([A-Z0-9-]+)", text, re.IGNORECASE)
        if case_match:
            data["caseNumber"] = case_match.group(2).strip()
        
        # Extract court information
        court_match = re.search(r"(court of|in the)(.+?)(?=\n|\r|$)", text, re.IGNORECASE)
        if court_match:
            data["court"] = court_match.group(2).strip()
        
        # Extract date from document
        date_match = re.search(r"dated[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.IGNORECASE)
        if date_match:
            data["documentDate"] = date_match.group(1).strip()
        
        # Extract parties involved (plaintiff, defendant, etc.)
        plaintiff_match = re.search(r"plaintiff[:\s]+([A-Za-z\s,]+)", text, re.IGNORECASE)
        if plaintiff_match:
            data["plaintiff"] = plaintiff_match.group(1).strip()
            
        defendant_match = re.search(r"defendant[:\s]+([A-Za-z\s,]+)", text, re.IGNORECASE)
        if defendant_match:
            data["defendant"] = defendant_match.group(1).strip()
        
        return data
    
    def _extract_general_data(self, text):
        """Extract general data from any document"""
        data = {}
        
        # Extract dates
        dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
        if dates:
            data["dates"] = dates
        
        # Extract email addresses
        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        if emails:
            data["emails"] = emails
        
        # Extract phone numbers
        phones = re.findall(r"\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b", text)
        if phones:
            data["phones"] = phones
        
        # Extract URLs
        urls = re.findall(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", text)
        if urls:
            data["urls"] = urls
        
        # Extract potentially important keywords
        keywords = ["invoice", "receipt", "contract", "agreement", "bill", "statement", "order"]
        found_keywords = []
        for keyword in keywords:
            if re.search(r"\b" + keyword + r"\b", text, re.IGNORECASE):
                found_keywords.append(keyword)
        
        if found_keywords:
            data["documentType"] = found_keywords
        
        return data

# Initialize service
ocr_service = OCRService() 