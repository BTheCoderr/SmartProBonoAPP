#!/usr/bin/env python

"""
This script checks if reportlab can be imported correctly
"""

try:
    from reportlab.pdfgen import canvas
    print("Successfully imported reportlab.pdfgen.canvas")
except ImportError as e:
    print(f"Failed to import reportlab.pdfgen.canvas: {e}")

try:
    from reportlab.lib import colors
    print("Successfully imported reportlab.lib.colors")
except ImportError as e:
    print(f"Failed to import reportlab.lib.colors: {e}")

try:
    from reportlab.lib.pagesizes import letter
    print("Successfully imported reportlab.lib.pagesizes")
except ImportError as e:
    print(f"Failed to import reportlab.lib.pagesizes: {e}")

try:
    from reportlab.lib.styles import getSampleStyleSheet
    print("Successfully imported reportlab.lib.styles")
except ImportError as e:
    print(f"Failed to import reportlab.lib.styles: {e}")

try:
    from reportlab.lib.units import inch
    print("Successfully imported reportlab.lib.units")
except ImportError as e:
    print(f"Failed to import reportlab.lib.units: {e}")

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    print("Successfully imported reportlab.platypus")
except ImportError as e:
    print(f"Failed to import reportlab.platypus: {e}")

print("Test completed") 