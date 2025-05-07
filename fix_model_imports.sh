#!/bin/bash

# Fix all model imports
find ./backend/models -type f -name "*.py" -exec sed -i '' 's/from backend\.database/from database/g' {} \;
find ./backend/models -type f -name "*.py" -exec sed -i '' 's/from backend\.extensions/from extensions/g' {} \;
find ./backend/models -type f -name "*.py" -exec sed -i '' 's/from backend\.models/from models/g' {} \;

echo "All model import paths have been fixed!" 