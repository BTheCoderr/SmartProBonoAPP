#!/usr/bin/env python3
import os
import shutil
import urllib.request
from typing import Dict, List

# Define fonts to download
FONTS = {
    'NotoSans': {
        'regular': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf',
        'bold': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf',
        'italic': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Italic.ttf'
    },
    'NotoSansArabic': {
        'regular': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf',
        'bold': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf'
    },
    'NotoSansCJK': {
        'regular': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansCJKsc/NotoSansCJKsc-Regular.ttf',
        'bold': 'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansCJKsc/NotoSansCJKsc-Bold.ttf'
    }
}

def setup_fonts_directory() -> None:
    """Set up the fonts directory and download required fonts."""
    # Create fonts directory
    fonts_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'templates',
        'fonts'
    )
    os.makedirs(fonts_dir, exist_ok=True)
    
    print("Downloading fonts...")
    for font_family, variants in FONTS.items():
        for variant, url in variants.items():
            filename = f"{font_family}-{variant}.ttf"
            output_path = os.path.join(fonts_dir, filename)
            
            if not os.path.exists(output_path):
                print(f"Downloading {filename}...")
                try:
                    urllib.request.urlretrieve(url, output_path)
                    print(f"Successfully downloaded {filename}")
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")
            else:
                print(f"{filename} already exists, skipping...")
    
    print("\nFont setup complete!")

if __name__ == "__main__":
    setup_fonts_directory() 