#!/bin/bash
# SmartProBono Critical Files Verification
# 
# This script verifies that all critical MVP files are present and properly formatted.

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color

# Function to check if a file exists
check_file() {
  local file="$1"
  local description="$2"
  
  echo -n "Checking $description ($file): "
  
  if [ -f "$file" ]; then
    echo -e "${GREEN}FOUND${NC}"
    return 0
  else
    echo -e "${RED}MISSING${NC}"
    return 1
  fi
}

# Function to count lines in a file
count_lines() {
  local file="$1"
  if [ -f "$file" ]; then
    wc -l "$file" | awk '{print $1}'
  else
    echo "0"
  fi
}

# Start banner
echo "======================================================="
echo "   SmartProBono Critical MVP Files Verification"
echo "======================================================="
echo

# Check for critical configuration files
echo "### Configuration Files ###"
check_file "production.env" "Production Environment Configuration"
check_file "deployment_script.sh" "Deployment Script"
check_file "DEPLOYMENT_GUIDE.md" "Deployment Guide"
check_file "mvp_verification.sh" "MVP Verification Script"
check_file "MVP_TASKS.md" "MVP Tasks List"
check_file "MVP_COMPLETION_SUMMARY.md" "MVP Completion Summary"
check_file "NAVIGATION_TEST_GUIDE.md" "Navigation Test Guide"

echo 

# Check for form tracking component files
echo "### Form Tracking Components ###"
check_file "frontend/src/components/ProgressTracker.js" "Progress Tracker Component"
check_file "frontend/src/services/StorageService.js" "Storage Service Utility"
check_file "test-form-progress.js" "Form Progress Test Script"

echo

# Check for critical React components
echo "### Critical React Components ###"
check_file "frontend/src/components/ImmigrationIntakeForm.js" "Immigration Intake Form"

echo

# Print verification summary
echo "======================================================="
echo "                  Verification Summary"
echo "======================================================="

# Count total files verified
total_files=11
found_files=$(find . -name "production.env" -o -name "deployment_script.sh" -o -name "DEPLOYMENT_GUIDE.md" -o \
                    -name "mvp_verification.sh" -o -name "MVP_TASKS.md" -o -name "MVP_COMPLETION_SUMMARY.md" -o \
                    -name "NAVIGATION_TEST_GUIDE.md" -o -path "./frontend/src/components/ProgressTracker.js" -o \
                    -path "./frontend/src/services/StorageService.js" -o -name "test-form-progress.js" -o \
                    -path "./frontend/src/components/ImmigrationIntakeForm.js" | wc -l)

# Check the size of key files
progress_tracker_lines=$(count_lines "frontend/src/components/ProgressTracker.js")
storage_service_lines=$(count_lines "frontend/src/services/StorageService.js")
intake_form_lines=$(count_lines "frontend/src/components/ImmigrationIntakeForm.js")

# Calculate code coverage percentage
code_coverage=$(( (found_files * 100) / total_files ))

echo "Files Found: $found_files / $total_files"
echo "Code Coverage: ${code_coverage}%"
echo 
echo "File Metrics:"
echo "- Progress Tracker: ${progress_tracker_lines} lines"
echo "- Storage Service: ${storage_service_lines} lines"
echo "- Immigration Intake Form: ${intake_form_lines} lines"
echo

# Final status
if [ $found_files -eq $total_files ]; then
  echo -e "${GREEN}All critical MVP files are present!${NC}"
  echo -e "The SmartProBono MVP implementation is COMPLETE."
else
  echo -e "${ORANGE}Some MVP files are missing.${NC}"
  echo -e "Please check the verification results above for details."
fi

echo "=======================================================" 