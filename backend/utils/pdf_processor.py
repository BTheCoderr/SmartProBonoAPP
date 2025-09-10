"""
PDF Processing Utility with Fallback Support
Handles different PDF libraries gracefully based on availability
"""

import logging
from typing import Optional, Dict, Any, List
import io

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    PDF processing class with fallback support for different PDF libraries
    """
    
    def __init__(self):
        self.available_libraries = self._detect_available_libraries()
        self.primary_lib = self._select_primary_library()
        logger.info(f"PDF Processor initialized with libraries: {self.available_libraries}")
        logger.info(f"Primary library: {self.primary_lib}")
    
    def _detect_available_libraries(self) -> Dict[str, bool]:
        """Detect which PDF libraries are available"""
        libraries = {}
        
        # Check PyMuPDF
        try:
            import fitz
            libraries['pymupdf'] = True
        except ImportError:
            libraries['pymupdf'] = False
        
        # Check pymupdf4llm
        try:
            import pymupdf4llm
            libraries['pymupdf4llm'] = True
        except ImportError:
            libraries['pymupdf4llm'] = False
        
        # Check pypdf
        try:
            import pypdf
            libraries['pypdf'] = True
        except ImportError:
            libraries['pypdf'] = False
        
        # Check pdfplumber
        try:
            import pdfplumber
            libraries['pdfplumber'] = True
        except ImportError:
            libraries['pdfplumber'] = False
        
        # Check PyPDF2
        try:
            import PyPDF2
            libraries['pypdf2'] = True
        except ImportError:
            libraries['pypdf2'] = False
        
        return libraries
    
    def _select_primary_library(self) -> str:
        """Select the best available PDF library"""
        if self.available_libraries.get('pymupdf'):
            return 'pymupdf'
        elif self.available_libraries.get('pymupdf4llm'):
            return 'pymupdf4llm'
        elif self.available_libraries.get('pdfplumber'):
            return 'pdfplumber'
        elif self.available_libraries.get('pypdf'):
            return 'pypdf'
        elif self.available_libraries.get('pypdf2'):
            return 'pypdf2'
        else:
            raise ImportError("No PDF processing libraries available")
    
    def extract_text(self, pdf_data: bytes) -> str:
        """Extract text from PDF using the best available library"""
        try:
            if self.primary_lib == 'pymupdf':
                return self._extract_text_pymupdf(pdf_data)
            elif self.primary_lib == 'pymupdf4llm':
                return self._extract_text_pymupdf4llm(pdf_data)
            elif self.primary_lib == 'pdfplumber':
                return self._extract_text_pdfplumber(pdf_data)
            elif self.primary_lib == 'pypdf':
                return self._extract_text_pypdf(pdf_data)
            elif self.primary_lib == 'pypdf2':
                return self._extract_text_pypdf2(pdf_data)
            else:
                raise ValueError(f"Unknown primary library: {self.primary_lib}")
        except Exception as e:
            logger.error(f"Error extracting text with {self.primary_lib}: {e}")
            # Try fallback libraries
            return self._extract_text_fallback(pdf_data)
    
    def _extract_text_pymupdf(self, pdf_data: bytes) -> str:
        """Extract text using PyMuPDF (fitz)"""
        try:
            import fitz
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
            raise
    
    def _extract_text_pymupdf4llm(self, pdf_data: bytes) -> str:
        """Extract text using pymupdf4llm"""
        import pymupdf4llm
        return pymupdf4llm.to_markdown(pdf_data)
    
    def _extract_text_pdfplumber(self, pdf_data: bytes) -> str:
        """Extract text using pdfplumber"""
        import pdfplumber
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _extract_text_pypdf(self, pdf_data: bytes) -> str:
        """Extract text using pypdf"""
        import pypdf
        text = ""
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_data))
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _extract_text_pypdf2(self, pdf_data: bytes) -> str:
        """Extract text using PyPDF2"""
        import PyPDF2
        text = ""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _extract_text_fallback(self, pdf_data: bytes) -> str:
        """Try fallback libraries if primary fails"""
        fallback_order = ['pdfplumber', 'pypdf', 'pypdf2', 'pymupdf4llm']
        
        for lib in fallback_order:
            if self.available_libraries.get(lib):
                try:
                    if lib == 'pdfplumber':
                        return self._extract_text_pdfplumber(pdf_data)
                    elif lib == 'pypdf':
                        return self._extract_text_pypdf(pdf_data)
                    elif lib == 'pypdf2':
                        return self._extract_text_pypdf2(pdf_data)
                    elif lib == 'pymupdf4llm':
                        return self._extract_text_pymupdf4llm(pdf_data)
                except Exception as e:
                    logger.warning(f"Fallback library {lib} also failed: {e}")
                    continue
        
        raise Exception("All PDF processing libraries failed")
    
    def get_page_count(self, pdf_data: bytes) -> int:
        """Get the number of pages in the PDF"""
        try:
            if self.primary_lib == 'pymupdf':
                import fitz
                doc = fitz.open(stream=pdf_data, filetype="pdf")
                count = doc.page_count
                doc.close()
                return count
            elif self.primary_lib in ['pypdf', 'pypdf2']:
                if self.primary_lib == 'pypdf':
                    import pypdf
                    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_data))
                else:
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
                return len(pdf_reader.pages)
            elif self.primary_lib == 'pdfplumber':
                import pdfplumber
                with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
                    return len(pdf.pages)
            else:
                # Fallback: try to extract text and count pages
                text = self.extract_text(pdf_data)
                return text.count('\f') + 1 if text else 1
        except Exception as e:
            logger.error(f"Error getting page count: {e}")
            return 1
    
    def get_metadata(self, pdf_data: bytes) -> Dict[str, Any]:
        """Get PDF metadata"""
        try:
            if self.primary_lib == 'pymupdf':
                import fitz
                doc = fitz.open(stream=pdf_data, filetype="pdf")
                metadata = doc.metadata
                doc.close()
                return metadata
            elif self.primary_lib in ['pypdf', 'pypdf2']:
                if self.primary_lib == 'pypdf':
                    import pypdf
                    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_data))
                else:
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
                return pdf_reader.metadata or {}
            else:
                return {}
        except Exception as e:
            logger.error(f"Error getting metadata: {e}")
            return {}

# Global instance
pdf_processor = PDFProcessor()
