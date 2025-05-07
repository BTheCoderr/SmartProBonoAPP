#!/bin/bash

# Fix all routes imports
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.models/from models/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.extensions/from extensions/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.utils/from utils/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.middleware/from middleware/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.services/from services/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.database/from database/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.websocket/from websocket/g' {} \;
find ./backend/routes -type f -name "*.py" -exec sed -i '' 's/from backend\.auth/from auth/g' {} \;

echo "All import paths have been fixed!" 