"""
Document filter service for styling and modifying PDFs
"""
from typing import Optional
from weasyprint import CSS
import uuid
from flask import current_app

class DocumentFilterService:
    """Service for applying filters and styles to PDF documents."""
    
    def __init__(self):
        """Initialize the document filter service."""
        self._instance_id = uuid.uuid4().hex[:8]
    
    def add_watermark(self, watermark_text: str) -> CSS:
        """
        Add a watermark to the document.
        
        Args:
            watermark_text: Text to use as watermark
            
        Returns:
            CSS: CSS style for watermark
        """
        return CSS(string=f'''
            @page {{
                background: linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 0));
                background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'><text x='50%' y='50%' font-family='Arial' font-size='50' font-weight='bold' fill-opacity='0.15' fill='gray' text-anchor='middle' transform='rotate(-45 50% 50%)'>{watermark_text}</text></svg>");
                background-repeat: repeat;
            }}
        ''')
    
    def add_header_footer(
        self,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> CSS:
        """
        Add custom header and footer to the document.
        
        Args:
            header_text: Text to use as header
            footer_text: Text to use as footer
            
        Returns:
            CSS: CSS style for header and footer
        """
        css_string = '@page {'
        
        if header_text:
            css_string += f'''
                @top-center {{
                    content: "{header_text}";
                    font-family: Arial;
                    font-size: 9pt;
                }}
            '''
        
        if footer_text:
            css_string += f'''
                @bottom-center {{
                    content: "{footer_text}";
                    font-family: Arial;
                    font-size: 9pt;
                }}
            '''
            
        css_string += '}'
        
        return CSS(string=css_string)
    
    def add_page_numbers(self) -> CSS:
        """
        Add page numbers to the document.
        
        Returns:
            CSS: CSS style for page numbers
        """
        return CSS(string='''
            @page {
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-family: Arial;
                    font-size: 9pt;
                }
            }
        ''')
    
    def apply_confidential_stamp(self) -> CSS:
        """
        Apply a confidential stamp to the document.
        
        Returns:
            CSS: CSS style for confidential stamp
        """
        return CSS(string='''
            @page {
                @top-right {
                    content: "CONFIDENTIAL";
                    font-family: Arial;
                    font-size: 12pt;
                    font-weight: bold;
                    color: #ff0000;
                }
            }
        ''')
    
    def apply_draft_watermark(self) -> CSS:
        """
        Apply a draft watermark to the document.
        
        Returns:
            CSS: CSS style for draft watermark
        """
        return self.add_watermark("DRAFT")
    
    def apply_copy_watermark(self) -> CSS:
        """
        Apply a copy watermark to the document.
        
        Returns:
            CSS: CSS style for copy watermark
        """
        return self.add_watermark("COPY")

# Singleton instance
_document_filter_service = None

def get_document_filter_service() -> DocumentFilterService:
    """
    Get the document filter service singleton instance.
    
    Returns:
        DocumentFilterService: The document filter service instance
    """
    global _document_filter_service
    if _document_filter_service is None:
        _document_filter_service = DocumentFilterService()
    return _document_filter_service 