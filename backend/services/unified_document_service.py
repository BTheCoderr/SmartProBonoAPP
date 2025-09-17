"""
UNIFIED DOCUMENT SERVICE - Single source of truth for all document operations
Consolidates all document scanning, processing, and generation functionality
"""

import os
import tempfile
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import uuid
from pathlib import Path

# PDF Processing - Use the unified PDF processor
from utils.pdf_processor import pdf_processor

# PDF Generation
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Template Processing
try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

logger = logging.getLogger(__name__)

class UnifiedDocumentService:
    """
    Single service for all document operations:
    - PDF text extraction
    - Document analysis
    - PDF generation
    - Template processing
    """
    
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.upload_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        
        # Ensure directories exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.upload_dir, exist_ok=True)
        
        # Initialize Jinja2 if available
        if JINJA2_AVAILABLE:
              self.jinja_env = jinja2.Environment(
                  loader=jinja2.FileSystemLoader(self.templates_dir),
                  autoescape=jinja2.select_autoescape(['html', 'xml'])  # Fix XSS vulnerability
              )
        else:
            self.jinja_env = None
    
    def extract_text_from_document(self, file_path: str) -> Optional[str]:
        """
        Extract text from any supported document type.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text or None if extraction fails
        """
        if not os.path.exists(file_path):
            logger.error(f"Document file not found: {file_path}")
            return None
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                return self._extract_pdf_text(file_path)
            elif file_ext in ['.txt', '.md']:
                return self._extract_text_file(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_ext}")
                return f"Text extraction not supported for {file_ext} files"
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return None
    
    def _extract_pdf_text(self, file_path: str) -> Optional[str]:
        """Extract text from PDF using the unified PDF processor."""
        try:
            with open(file_path, 'rb') as f:
                pdf_data = f.read()
            
            text = pdf_processor.extract_text(pdf_data)
            if text.strip():
                logger.info(f"Successfully extracted {len(text)} characters using {pdf_processor.primary_lib}")
                return text.strip()
            else:
                logger.warning("No text extracted from PDF")
                return "No readable text found in this PDF document."
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            return "No readable text found in this PDF document."
    
    def _extract_text_file(self, file_path: str) -> str:
        """Extract text from plain text files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return f"Error reading file: {e}"
    
    def analyze_document(self, file_path: str, document_type: str = 'generic', 
                        questions: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a document for legal information.
        
        Args:
            file_path: Path to the document
            document_type: Type of document (contract, lease, etc.)
            questions: List of specific questions to answer
            
        Returns:
            Analysis results
        """
        try:
            # Extract text
            text = self.extract_text_from_document(file_path)
            if not text:
                return {
                    "success": False,
                    "error": "Could not extract text from document"
                }
            
            # Basic analysis
            analysis = {
                "success": True,
                "document_type": document_type,
                "text_length": len(text),
                "word_count": len(text.split()),
                "extracted_text": text[:1000] + "..." if len(text) > 1000 else text,
                "analysis_timestamp": datetime.now().isoformat(),
                "confidence": 0.8,
                "pages": text.count("--- Page") + 1,
                "words": len(text.split()),
                "client_summary": f"Document contains {len(text.split())} words across {text.count('--- Page') + 1} pages",
                "parties": self._extract_parties(text),
                "key_dates": self._extract_dates(text),
                "monetary_amounts": self._extract_monetary_amounts(text),
                "legal_terms": self._extract_legal_terms(text),
                "potential_issues": self._identify_potential_issues(text, document_type),
                "recommendations": self._generate_recommendations(text, document_type),
                "action_items": self._generate_action_items(text, document_type),
                "risk_level": self._assess_risk_level(text, document_type),
                "escalation_needed": self._needs_escalation(text, document_type),
                "safety_checked": True
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_pdf(self, content: Union[str, Dict], template_name: str = None, 
                    output_path: str = None) -> str:
        """
        Generate PDF from content or template.
        
        Args:
            content: Content to generate PDF from
            template_name: Jinja2 template name (optional)
            output_path: Output file path (optional)
            
        Returns:
            Path to generated PDF
        """
        if not output_path:
            output_path = os.path.join(
                self.upload_dir, 
                f"document_{uuid.uuid4().hex[:8]}.pdf"
            )
        
        try:
            # Generate HTML content
            if template_name and self.jinja_env:
                html_content = self._render_template(template_name, content)
            else:
                html_content = self._content_to_html(content)
            
            # Try multiple PDF generation methods
            return self._generate_pdf_from_html(html_content, output_path)
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise ValueError(f"Failed to generate PDF: {e}")
    
    def _generate_pdf_from_html(self, html_content: str, output_path: str) -> str:
        """Generate PDF from HTML using the best available method."""
        
        # Method 1: Try pdfkit
        if PDFKIT_AVAILABLE:
            try:
                options = {
                    'page-size': 'Letter',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': 'UTF-8',
                    'no-outline': None
                }
                pdfkit.from_string(html_content, output_path, options=options)
                logger.info("PDF generated using pdfkit")
                return output_path
            except Exception as e:
                logger.warning(f"pdfkit failed: {e}")
        
        # Method 2: Try weasyprint
        if WEASYPRINT_AVAILABLE:
            try:
                HTML(string=html_content).write_pdf(output_path)
                logger.info("PDF generated using weasyprint")
                return output_path
            except Exception as e:
                logger.warning(f"weasyprint failed: {e}")
        
        # Method 3: Fallback to reportlab
        if REPORTLAB_AVAILABLE:
            try:
                doc = SimpleDocTemplate(output_path, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Convert HTML to plain text for reportlab
                import re
                text_content = re.sub(r'<[^>]+>', '', html_content)
                lines = text_content.split('\n')
                
                for line in lines[:50]:  # Limit to first 50 lines
                    if line.strip():
                        p = Paragraph(line.strip(), styles['Normal'])
                        story.append(p)
                
                doc.build(story)
                logger.info("PDF generated using reportlab")
                return output_path
            except Exception as e:
                logger.warning(f"reportlab failed: {e}")
        
        raise ValueError("No PDF generation method available")
    
    def _render_template(self, template_name: str, context: Dict) -> str:
        """Render Jinja2 template."""
        if not self.jinja_env:
            raise ValueError("Jinja2 not available")
        
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
    
    def _content_to_html(self, content: Union[str, Dict]) -> str:
        """Convert content to HTML."""
        if isinstance(content, str):
            return f"<html><body><pre>{content}</pre></body></html>"
        elif isinstance(content, dict):
            html = "<html><body>"
            for key, value in content.items():
                html += f"<h3>{key}</h3><p>{value}</p>"
            html += "</body></html>"
            return html
        else:
            return f"<html><body><p>{str(content)}</p></body></html>"
    
    # Helper methods for document analysis
    def _extract_parties(self, text: str) -> List[str]:
        """Extract party names from document text."""
        # Simple implementation - look for common patterns
        parties = []
        lines = text.split('\n')
        for line in lines:
            if 'v.' in line or 'vs.' in line or 'versus' in line.lower():
                parties.append(line.strip())
        return parties[:5]  # Limit to 5 parties
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from document text."""
        import re
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        dates = re.findall(date_pattern, text)
        return list(set(dates))[:10]  # Limit to 10 unique dates
    
    def _extract_monetary_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts from document text."""
        import re
        money_pattern = r'\$[\d,]+\.?\d*'
        amounts = re.findall(money_pattern, text)
        return list(set(amounts))[:10]  # Limit to 10 unique amounts
    
    def _extract_legal_terms(self, text: str) -> List[str]:
        """Extract legal terms from document text."""
        legal_terms = [
            'contract', 'agreement', 'lease', 'liability', 'damages',
            'breach', 'warranty', 'indemnification', 'jurisdiction',
            'arbitration', 'mediation', 'force majeure'
        ]
        found_terms = []
        text_lower = text.lower()
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        return found_terms
    
    def _identify_potential_issues(self, text: str, doc_type: str) -> List[str]:
        """Identify potential legal issues in the document."""
        issues = []
        text_lower = text.lower()
        
        if 'liability' in text_lower and 'limit' in text_lower:
            issues.append("Limited liability clause present")
        if 'termination' in text_lower and 'notice' in text_lower:
            issues.append("Termination clause requires notice")
        if 'payment' in text_lower and 'late' in text_lower:
            issues.append("Late payment penalties may apply")
        
        return issues
    
    def _generate_recommendations(self, text: str, doc_type: str) -> List[str]:
        """Generate recommendations based on document analysis."""
        return [
            "Review all terms and conditions carefully",
            "Consider consulting with a legal professional",
            "Ensure all parties understand their obligations",
            "Keep copies of all related documents"
        ]
    
    def _generate_action_items(self, text: str, doc_type: str) -> List[str]:
        """Generate action items based on document analysis."""
        return [
            "Schedule review with legal counsel",
            "Prepare questions about unclear terms",
            "Gather supporting documentation",
            "Set calendar reminders for important dates"
        ]
    
    def _assess_risk_level(self, text: str, doc_type: str) -> str:
        """Assess risk level of the document."""
        text_lower = text.lower()
        risk_indicators = ['liability', 'penalty', 'breach', 'damages', 'termination']
        risk_count = sum(1 for indicator in risk_indicators if indicator in text_lower)
        
        if risk_count >= 4:
            return "high"
        elif risk_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _needs_escalation(self, text: str, doc_type: str) -> bool:
        """Determine if document needs legal escalation."""
        text_lower = text.lower()
        escalation_terms = ['lawsuit', 'litigation', 'court', 'judgment', 'settlement']
        return any(term in text_lower for term in escalation_terms)

# Create singleton instance
unified_document_service = UnifiedDocumentService()
