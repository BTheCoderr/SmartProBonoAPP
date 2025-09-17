import requests
import re
from html import unescape

def decode_secret_message(url):
    """
    Takes a Google Doc URL, retrieves and parses the data to print a grid of characters
    that forms a secret message when displayed in a fixed-width font.
    """
    # Fetch the document text
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    
    # Extract table row data using regex
    # The Google Doc contains a table with format: x-coordinate, character, y-coordinate
    row_pattern = r'<tr class="c4">(.*?)</tr>'
    rows = re.findall(row_pattern, html_content, re.DOTALL)
    
    entries = []
    max_x, max_y = 0, 0
    
    for row in rows:
        # Extract cell contents from each row
        cell_pattern = r'<span class="c1">(.*?)</span>'
        cells = re.findall(cell_pattern, row)
        
        if len(cells) >= 3:
            try:
                x = int(cells[0].strip())
                char = unescape(cells[1].strip())
                y = int(cells[2].strip())
                
                entries.append((char, x, y))
                max_x, max_y = max(max_x, x), max(max_y, y)
                    
            except (ValueError, IndexError):
                continue
    
    if not entries:
        print("No valid character entries found!")
        return
    
    # Create and fill the grid
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    for char, x, y in entries:
        grid[y][x] = char
    
    # Print the result
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    test_url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
    decode_secret_message(test_url)
