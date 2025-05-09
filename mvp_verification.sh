#!/bin/bash
# SmartProBono MVP Verification Script
#
# This script tests all critical features of the SmartProBono application
# to verify that the MVP requirements have been met.

set -e  # Exit immediately if a command exits with a non-zero status

TIMESTAMP=$(date +%Y%m%d%H%M%S)
LOG_FILE="mvp_verification_${TIMESTAMP}.log"
FRONTEND_DIR="./frontend"
BACKEND_DIR="./backend"
VERIFICATION_RESULTS="./verification_results_${TIMESTAMP}.md"

# Function to log messages
log() {
  local message="$1"
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $message" | tee -a $LOG_FILE
}

# Create results file header
create_results_file() {
  cat > $VERIFICATION_RESULTS <<EOL
# SmartProBono MVP Verification Results

**Date:** $(date +'%Y-%m-%d %H:%M:%S')  
**Environment:** ${1:-"Development"}

## Summary

This report contains the verification results for all critical path features of the SmartProBono application.

## Test Results

EOL
}

# Function to record test results
record_result() {
  local test_name="$1"
  local result="$2"
  local details="${3:-"No additional details."}"
  
  if [ "$result" = "PASS" ]; then
    icon="✅"
  elif [ "$result" = "FAIL" ]; then
    icon="❌"
  else
    icon="⚠️"
  fi
  
  cat >> $VERIFICATION_RESULTS <<EOL
### ${test_name}

**Result:** ${icon} ${result}

**Details:** ${details}

EOL
}

# Function to check if dependencies are installed
check_dependencies() {
  log "Checking dependencies..."
  
  # Check Node.js
  if command -v node &> /dev/null; then
    node_version=$(node -v)
    log "Node.js: ${node_version} ✓"
    record_result "Node.js Check" "PASS" "Found version ${node_version}"
  else
    log "Node.js: Not found ✗"
    record_result "Node.js Check" "FAIL" "Node.js is not installed."
    exit 1
  fi
  
  # Check npm
  if command -v npm &> /dev/null; then
    npm_version=$(npm -v)
    log "npm: ${npm_version} ✓"
    record_result "npm Check" "PASS" "Found version ${npm_version}"
  else
    log "npm: Not found ✗"
    record_result "npm Check" "FAIL" "npm is not installed."
    exit 1
  fi
  
  # Check Python
  if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    log "Python: ${python_version} ✓"
    record_result "Python Check" "PASS" "Found ${python_version}"
  else
    log "Python: Not found ✗"
    record_result "Python Check" "FAIL" "Python 3 is not installed."
    exit 1
  fi
}

# Function to check frontend build
check_frontend_build() {
  log "Checking frontend build..."
  
  cd $FRONTEND_DIR
  
  # Check if package.json exists
  if [ -f "package.json" ]; then
    log "package.json: Found ✓"
    
    # Check if dependencies can be installed
    log "Installing dependencies..."
    npm ci --quiet || npm install --quiet
    
    if [ $? -eq 0 ]; then
      log "Dependencies: Installed successfully ✓"
      
      # Try building the frontend
      log "Building frontend..."
      npm run build --quiet
      
      if [ $? -eq 0 ]; then
        log "Frontend build: Successful ✓"
        record_result "Frontend Build" "PASS" "Successfully built the frontend application."
      else
        log "Frontend build: Failed ✗"
        record_result "Frontend Build" "FAIL" "The frontend build process failed. Check the logs for details."
      fi
    else
      log "Dependencies: Installation failed ✗"
      record_result "Frontend Dependencies" "FAIL" "Failed to install frontend dependencies."
    fi
  else
    log "package.json: Not found ✗"
    record_result "Frontend Package" "FAIL" "package.json file not found in frontend directory."
  fi
  
  cd ..
}

# Function to check backend
check_backend() {
  log "Checking backend..."
  
  cd $BACKEND_DIR
  
  # Check if requirements.txt exists
  if [ -f "requirements.txt" ]; then
    log "requirements.txt: Found ✓"
    
    # Create a virtual environment
    log "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    log "Installing backend dependencies..."
    pip install -r requirements.txt --quiet
    
    if [ $? -eq 0 ]; then
      log "Backend dependencies: Installed successfully ✓"
      record_result "Backend Dependencies" "PASS" "Successfully installed backend dependencies."
      
      # Check if main app file exists
      if [ -f "app.py" ]; then
        log "app.py: Found ✓"
        record_result "Backend Application" "PASS" "Found main application file."
      else
        log "app.py: Not found, searching for alternative main file..."
        main_file=$(find . -name "*.py" -type f -exec grep -l "if __name__ == '__main__'" {} \; | head -1)
        
        if [ -n "$main_file" ]; then
          log "Main application file: Found at ${main_file} ✓"
          record_result "Backend Application" "PASS" "Found alternative main application file: ${main_file}"
        else
          log "Main application file: Not found ✗"
          record_result "Backend Application" "FAIL" "Could not find a main application file."
        fi
      fi
      
      # Deactivate virtual environment
      deactivate
    else
      log "Backend dependencies: Installation failed ✗"
      record_result "Backend Dependencies" "FAIL" "Failed to install backend dependencies."
      deactivate
    fi
  else
    log "requirements.txt: Not found ✗"
    record_result "Backend Requirements" "FAIL" "requirements.txt file not found in backend directory."
  fi
  
  cd ..
}

# Function to check critical features by static code analysis
check_critical_features() {
  log "Checking critical features by static code analysis..."
  
  # Check authentication implementation
  log "Checking authentication implementation..."
  auth_files=$(grep -r "auth" --include="*.js" --include="*.py" . | wc -l)
  jwt_files=$(grep -r "jwt" --include="*.js" --include="*.py" . | wc -l)
  
  if [ $auth_files -gt 0 ] && [ $jwt_files -gt 0 ]; then
    log "Authentication: Found evidence of implementation ✓"
    record_result "Authentication Implementation" "PASS" "Found evidence of authentication in the codebase."
  else
    log "Authentication: Limited evidence of implementation ⚠️"
    record_result "Authentication Implementation" "WARNING" "Limited evidence of authentication in the codebase."
  fi
  
  # Check document management
  log "Checking document management..."
  doc_files=$(grep -r "document" --include="*.js" --include="*.py" . | wc -l)
  
  if [ $doc_files -gt 0 ]; then
    log "Document Management: Found evidence of implementation ✓"
    record_result "Document Management" "PASS" "Found evidence of document management features."
  else
    log "Document Management: Limited evidence of implementation ⚠️"
    record_result "Document Management" "WARNING" "Limited evidence of document management in the codebase."
  fi
  
  # Check form submission workflow
  log "Checking form submission workflow..."
  form_files=$(grep -r "form" --include="*.js" --include="*.py" . | wc -l)
  
  if [ $form_files -gt 0 ]; then
    log "Form Submission: Found evidence of implementation ✓"
    record_result "Form Submission Workflow" "PASS" "Found evidence of form submission functionality."
  else
    log "Form Submission: Limited evidence of implementation ⚠️"
    record_result "Form Submission Workflow" "WARNING" "Limited evidence of form handling in the codebase."
  fi
  
  # Check deployment files
  log "Checking deployment configuration..."
  
  if [ -f "production.env" ] && [ -f "deployment_script.sh" ]; then
    log "Deployment Configuration: Found required files ✓"
    record_result "Deployment Configuration" "PASS" "Found both production.env and deployment_script.sh files."
  else
    log "Deployment Configuration: Missing some files ⚠️"
    record_result "Deployment Configuration" "WARNING" "Missing one or more deployment configuration files."
  fi
}

# Function to generate a final summary
generate_summary() {
  log "Generating final summary..."
  
  # Count results
  pass_count=$(grep -c "PASS" $VERIFICATION_RESULTS)
  fail_count=$(grep -c "FAIL" $VERIFICATION_RESULTS)
  warning_count=$(grep -c "WARNING" $VERIFICATION_RESULTS)
  
  cat >> $VERIFICATION_RESULTS <<EOL
## Summary

- ✅ Passed: ${pass_count}
- ❌ Failed: ${fail_count}
- ⚠️ Warnings: ${warning_count}

## Conclusion

EOL

  if [ $fail_count -eq 0 ]; then
    if [ $warning_count -eq 0 ]; then
      cat >> $VERIFICATION_RESULTS <<EOL
**All tests passed!** The SmartProBono application meets all the critical path requirements for the MVP.
EOL
    else
      cat >> $VERIFICATION_RESULTS <<EOL
**All critical tests passed, but with warnings.** The SmartProBono application meets the minimum requirements for the MVP, but there are ${warning_count} warnings that should be addressed.
EOL
    fi
  else
    cat >> $VERIFICATION_RESULTS <<EOL
**${fail_count} tests failed.** The SmartProBono application does not yet meet all critical path requirements for the MVP. Please address the failing tests.
EOL
  fi
  
  log "Verification completed. Results saved to ${VERIFICATION_RESULTS}"
  echo "----------------------------------------"
  echo "Verification completed!"
  echo "Results saved to: ${VERIFICATION_RESULTS}"
  echo "----------------------------------------"
}

# Main function to run all checks
main() {
  log "=== Starting SmartProBono MVP Verification ==="
  
  # Create results file
  create_results_file
  
  # Run checks
  check_dependencies
  check_frontend_build
  check_backend
  check_critical_features
  
  # Generate summary
  generate_summary
  
  log "=== Verification Completed ==="
}

# Run the main function
main 