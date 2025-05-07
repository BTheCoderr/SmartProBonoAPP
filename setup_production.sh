#!/bin/bash

# Exit on error
set -e

echo "Setting up SmartProBono production environment..."

# Check for required tools
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Create necessary directories
echo "Creating required directories..."
mkdir -p nginx/conf.d nginx/ssl nginx/logs backend/logs frontend/build data/mongodb data/postgres data/redis

# Generate SSL certificate for development (replace with real certificates in production)
echo "Generating self-signed SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/nginx.key -out nginx/ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Generated on $(date)
# Replace these values with secure production values
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=$(openssl rand -base64 32)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(openssl rand -base64 64)
EOL
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo "Checking service health..."
docker-compose ps

# Initialize database
echo "Initializing database..."
docker-compose exec backend flask db upgrade

echo "Setup complete! The application should be running at:"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:5000"
echo ""
echo "Please make sure to:"
echo "1. Replace the self-signed SSL certificate with a real one"
echo "2. Update the .env file with secure production values"
echo "3. Configure your domain DNS settings"
echo "4. Set up monitoring and logging"
echo "5. Configure backup solutions" 