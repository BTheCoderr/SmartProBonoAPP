#!/bin/bash

# Set the directory to the frontend source code
SOURCE_DIR="frontend/src"

# Message about what this script does
echo "============================================================"
echo "SmartProBono ESLint Warning Cleanup Script"
echo "============================================================"
echo "This script will fix some of the most common ESLint warnings"
echo "by commenting out unused imports and variables."
echo ""

# Function to count lines in a file
count_lines() {
  wc -l "$1" | awk '{print $1}'
}

# Function to process each JavaScript/JSX file
process_file() {
  local file=$1
  echo "Processing $file..."
  
  # Variables for tracking modifications
  local original_lines=$(count_lines "$file")
  local modified=false
  
  # Create a temporary file
  local temp_file=$(mktemp)
  
  # Comment out unused imports and variables
  awk '
    # If line contains "import" and any marker suggesting it is unused
    /import.*/ && /.*\/\/ no-unused-vars/ {
      print "// DISABLED BY CLEANUP: " $0
      next
    }
    # Lines with variable assignments marked as unused
    /.*=.*/ && /.*\/\/ no-unused-vars/ {
      print "// DISABLED BY CLEANUP: " $0
      next
    }
    # Otherwise, print the line unchanged
    {
      print
    }
  ' "$file" > "$temp_file"
  
  # Check if file was modified
  if ! cmp -s "$file" "$temp_file"; then
    modified=true
    cp "$temp_file" "$file"
    local new_lines=$(count_lines "$file")
    echo "  - Modified: $file ($original_lines -> $new_lines lines)"
  else
    echo "  - No changes needed for $file"
  fi
  
  # Remove the temporary file
  rm "$temp_file"
}

# Find and process all JavaScript and JSX files
find "$SOURCE_DIR" -type f -name "*.js" -o -name "*.jsx" | while read file; do
  process_file "$file"
done

echo ""
echo "Cleanup complete!"
echo "Note: You should still review the code to make sure functionality wasn't affected."
echo "Many ESLint warnings may still exist that require manual fixing." 