import pytest
from weasyprint import HTML

def test_weasyprint_basic():
    """Test basic WeasyPrint functionality by generating a simple PDF."""
    html = '<h1>Test Document</h1><p>This is a test paragraph.</p>'
    pdf = HTML(string=html).write_pdf()
    assert len(pdf) > 0, "PDF generation failed" 