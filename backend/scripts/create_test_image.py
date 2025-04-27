#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import sys

print(f"Current working directory: {os.getcwd()}")

# Create a blank image with white background
img = Image.new('RGB', (800, 400), color='white')
draw = ImageDraw.Draw(img)

# Add some text
text = 'Hello SmartProBono OCR Test'
try:
    # Try to use a system font
    font = ImageFont.truetype('Arial', 40)
    print("Using Arial font")
except IOError:
    # If the font is not available, use default
    font = ImageFont.load_default()
    print("Using default font")

# Draw text
draw.text((50, 50), text, fill='black', font=font)
draw.text((50, 120), 'Date of Birth: 01/01/1980', fill='black', font=font)
draw.text((50, 190), 'ID Number: ABC-123-456-789', fill='black', font=font)
draw.text((50, 260), 'Address: 123 Main St, City, State 12345', fill='black', font=font)

# Ensure test_data directory exists
test_dir = os.path.join(os.getcwd(), 'test_data')
os.makedirs(test_dir, exist_ok=True)
print(f"Created directory: {test_dir}")

# Save the image with absolute path as PNG
image_path = os.path.join(test_dir, 'ocr_test.png')
img.save(image_path, format='PNG')
print(f"Test image created: {image_path}")

# Verify file exists
if os.path.exists(image_path):
    print(f"File exists at {image_path} with size {os.path.getsize(image_path)} bytes")
else:
    print(f"Failed to create file at {image_path}") 