#!/bin/bash
# SmartProBono Production Deployment Script
# 
# This script automates the deployment of the SmartProBono application
# to a production environment.

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration variables
DEPLOY_ENV=${1:-production}  # Default to production if no argument provided
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="./backups/${TIMESTAMP}"
APP_NAME="smartprobono"
FRONTEND_DIR="./frontend"
BACKEND_DIR="./backend"
DEPLOY_LOG="deploy_${TIMESTAMP}.log"

# Load environment variables from file
if [ -f "${DEPLOY_ENV}.env" ]; then
  echo "Loading environment variables from ${DEPLOY_ENV}.env..."
  export $(grep -v '^#' ${DEPLOY_ENV}.env | xargs)
else
  echo "Error: Environment file ${DEPLOY_ENV}.env not found!"
  exit 1
fi

# Function to log messages
log() {
  local message="$1"
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $message" | tee -a $DEPLOY_LOG
}

# Function to create backup
create_backup() {
  log "Creating backup in ${BACKUP_DIR}..."
  mkdir -p $BACKUP_DIR
  
  # Backup frontend build
  if [ -d "${FRONTEND_DIR}/build" ]; then
    log "Backing up frontend build..."
    mkdir -p "${BACKUP_DIR}/frontend"
    cp -r "${FRONTEND_DIR}/build" "${BACKUP_DIR}/frontend/"
  fi
  
  # Backup database (assumes PostgreSQL)
  if command -v pg_dump &> /dev/null; then
    log "Backing up database..."
    mkdir -p "${BACKUP_DIR}/database"
    pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -F c -f "${BACKUP_DIR}/database/${DB_NAME}_${TIMESTAMP}.dump"
  else
    log "Warning: pg_dump not found. Skipping database backup."
  fi
  
  log "Backup created successfully!"
}

# Function to build frontend
build_frontend() {
  log "Building frontend..."
  cd $FRONTEND_DIR
  
  # Install dependencies
  log "Installing frontend dependencies..."
  npm ci --production
  
  # Create .env file for frontend
  log "Creating frontend environment file..."
  cat > .env <<EOL
REACT_APP_API_URL=${REACT_APP_API_URL}
REACT_APP_ENV=${REACT_APP_ENV}
REACT_APP_GA_TRACKING_ID=${REACT_APP_GA_TRACKING_ID}
REACT_APP_VERSION=${REACT_APP_VERSION}
REACT_APP_NAME=${REACT_APP_NAME}
REACT_APP_ENABLE_ANALYTICS=${REACT_APP_ENABLE_ANALYTICS}
REACT_APP_SUPPORT_EMAIL=${REACT_APP_SUPPORT_EMAIL}
EOL
  
  # Build the frontend
  log "Building frontend production bundle..."
  npm run build
  
  # Return to root directory
  cd ..
  log "Frontend build completed successfully!"
}

# Function to build backend
build_backend() {
  log "Building backend..."
  cd $BACKEND_DIR
  
  # Install dependencies
  log "Installing backend dependencies..."
  python -m pip install -r requirements.txt --no-cache-dir
  
  # Create .env file for backend
  log "Creating backend environment file..."
  cat > .env <<EOL
# API Settings
API_HOST=${API_HOST}
API_PORT=${API_PORT}
API_PROTOCOL=${API_PROTOCOL}

# JWT Configuration
JWT_SECRET=${JWT_SECRET}
JWT_ACCESS_TOKEN_EXPIRY=${JWT_ACCESS_TOKEN_EXPIRY}
JWT_REFRESH_TOKEN_EXPIRY=${JWT_REFRESH_TOKEN_EXPIRY}

# Database Settings
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_POOL_SIZE=${DB_POOL_SIZE}
DB_SSL=${DB_SSL}

# Redis Settings
REDIS_HOST=${REDIS_HOST}
REDIS_PORT=${REDIS_PORT}
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_SSL=${REDIS_SSL}

# Email Settings
SMTP_HOST=${SMTP_HOST}
SMTP_PORT=${SMTP_PORT}
SMTP_USER=${SMTP_USER}
SMTP_PASSWORD=${SMTP_PASSWORD}
SMTP_FROM_EMAIL=${SMTP_FROM_EMAIL}
SMTP_FROM_NAME=${SMTP_FROM_NAME}

# Security Settings
CORS_ALLOW_ORIGINS=${CORS_ALLOW_ORIGINS}
RATE_LIMIT_WINDOW_MS=${RATE_LIMIT_WINDOW_MS}
RATE_LIMIT_MAX_REQUESTS=${RATE_LIMIT_MAX_REQUESTS}
COOKIE_SECRET=${COOKIE_SECRET}
ENABLE_HTTPS_REDIRECT=${ENABLE_HTTPS_REDIRECT}
SESSION_COOKIE_SECURE=${SESSION_COOKIE_SECURE}

# Logging & Monitoring
LOG_LEVEL=${LOG_LEVEL}
ENABLE_REQUEST_LOGGING=${ENABLE_REQUEST_LOGGING}
SENTRY_DSN=${SENTRY_DSN}
ENABLE_PERFORMANCE_MONITORING=${ENABLE_PERFORMANCE_MONITORING}

# AI Features
AI_MODEL_API_KEY=${AI_MODEL_API_KEY}
AI_MODEL_ENDPOINT=${AI_MODEL_ENDPOINT}
AI_MODEL_VERSION=${AI_MODEL_VERSION}

# Storage Configuration
STORAGE_TYPE=${STORAGE_TYPE}
S3_BUCKET=${S3_BUCKET}
S3_REGION=${S3_REGION}
S3_ACCESS_KEY=${S3_ACCESS_KEY}
S3_SECRET_KEY=${S3_SECRET_KEY}

# Feature Flags
ENABLE_DOCUMENT_GENERATION=${ENABLE_DOCUMENT_GENERATION}
ENABLE_AI_FEATURES=${ENABLE_AI_FEATURES}
ENABLE_PREMIUM_FEATURES=${ENABLE_PREMIUM_FEATURES}
ENABLE_NOTIFICATIONS=${ENABLE_NOTIFICATIONS}
ENABLE_ANALYTICS=${ENABLE_ANALYTICS}
ENABLE_EMAIL_NOTIFICATIONS=${ENABLE_EMAIL_NOTIFICATIONS}
EOL
  
  # Return to root directory
  cd ..
  log "Backend build completed successfully!"
}

# Function to deploy the application
deploy() {
  log "Starting deployment to ${DEPLOY_ENV} environment..."
  
  # Run database migrations
  log "Running database migrations..."
  cd $BACKEND_DIR
  python manage.py migrate
  cd ..
  
  # Deploy frontend to web server (Example for nginx)
  log "Deploying frontend..."
  if [ -d "/var/www/html/${APP_NAME}" ]; then
    sudo rm -rf "/var/www/html/${APP_NAME}"
  fi
  sudo mkdir -p "/var/www/html/${APP_NAME}"
  sudo cp -r "${FRONTEND_DIR}/build/"* "/var/www/html/${APP_NAME}/"
  
  # Restart services
  log "Restarting services..."
  sudo systemctl restart nginx
  sudo systemctl restart ${APP_NAME}_backend
  
  log "Deployment completed successfully!"
}

# Function to run post-deployment tests
run_tests() {
  log "Running post-deployment tests..."
  
  # Test backend health endpoint
  log "Testing backend health endpoint..."
  curl -s -o /dev/null -w "%{http_code}" "${API_PROTOCOL}://${API_HOST}:${API_PORT}/api/health" | grep -q "200" 
  if [ $? -eq 0 ]; then
    log "Backend health check: SUCCESS"
  else
    log "Backend health check: FAILED"
    exit 1
  fi
  
  # Test frontend
  log "Testing frontend..."
  curl -s -o /dev/null -w "%{http_code}" "https://smartprobono.org" | grep -q "200"
  if [ $? -eq 0 ]; then
    log "Frontend check: SUCCESS"
  else
    log "Frontend check: FAILED"
    exit 1
  fi
  
  log "All tests passed successfully!"
}

# Main deployment process
main() {
  log "=== Starting SmartProBono Deployment Process ==="
  
  # Create backup before deployment
  create_backup
  
  # Build and deploy
  build_frontend
  build_backend
  deploy
  
  # Run tests
  run_tests
  
  log "=== Deployment Completed Successfully ==="
}

# Start the deployment process
main 