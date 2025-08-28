#!/bin/bash

# Script to fix backend import paths in Python files
echo "Starting backend import path fixes..."

# Find all Python files in the backend directory
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.models/from models/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.extensions/from extensions/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.utils/from utils/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.middleware/from middleware/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.services/from services/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.database/from database/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.websocket/from websocket/g' {} \;
find ./backend -type f -name "*.py" -exec sed -i '' 's/from backend\.auth/from auth/g' {} \;

# Create __init__.py files to ensure modules are importable
echo "Creating __init__.py files in necessary directories..."

dirs=(
  "backend/models"
  "backend/services"
  "backend/utils"
  "backend/extensions"
  "backend/middleware"
  "backend/database"
  "backend/routes"
  "backend/auth"
)

for dir in "${dirs[@]}"; do
  if [ -d "$dir" ]; then
    if [ ! -f "$dir/__init__.py" ]; then
      echo "Creating $dir/__init__.py"
      touch "$dir/__init__.py"
    fi
  else
    echo "Directory $dir does not exist, creating it..."
    mkdir -p "$dir"
    touch "$dir/__init__.py"
  fi
done

echo "Backend import path fixes completed!" 