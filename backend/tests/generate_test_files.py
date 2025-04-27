"""Generate test files for testing."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_image(output_dir: Path) -> None:
    """Create a test image with text for OCR testing."""
    # Create a new image with white background
    width = 800
    height = 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Use a larger font size for better OCR
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 36)
    except OSError:
        # Fallback for non-macOS systems
        font = ImageFont.load_default()
    
    text = "This is a test image for OCR"
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw black text
    draw.text((x, y), text, fill='black', font=font)
    
    # Save to file
    image.save(output_dir / 'test_image.jpg', format='JPEG')

def create_test_pdf(output_dir: Path) -> None:
    """Create a test PDF with text for OCR testing."""
    c = canvas.Canvas(str(output_dir / 'test.pdf'), pagesize=letter)
    c.drawString(100, 750, "This is a test PDF document")
    c.save()

def main():
    """Generate all test files."""
    # Get the test_files directory
    test_files_dir = Path(__file__).parent / 'test_files'
    test_files_dir.mkdir(exist_ok=True)
    
    # Generate test files
    create_test_image(test_files_dir)
    create_test_pdf(test_files_dir)
    
    print("Test files generated successfully!")

if __name__ == '__main__':
    main() 