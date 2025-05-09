# SmartProBono Deployment Guide

This guide provides detailed instructions for deploying the SmartProBono application to production, staging, and development environments.

## Prerequisites

Before proceeding with deployment, ensure the following prerequisites are met:

1. **Server Requirements**:
   - Ubuntu 20.04 LTS or newer
   - At least 2GB RAM
   - At least 20GB storage
   - SSH access with sudo privileges

2. **Software Requirements**:
   - Node.js 16+ and npm 8+
   - Python 3.9+
   - PostgreSQL 13+
   - Redis 6+
   - Nginx
   - Certbot (for SSL)

3. **Domain Names**:
   - Production: smartprobono.org and api.smartprobono.org
   - Staging: staging.smartprobono.org and api-staging.smartprobono.org

4. **Environment Files**:
   - Properly configured production.env (or staging.env) file with all required variables

## Quick Start

For a standard deployment to production:

```bash
# Clone the repository
git clone https://github.com/yourusername/smartprobono.git
cd smartprobono

# Deploy the application
./deployment_script.sh production
```

## Deployment Environments

The application supports multiple deployment environments:

### Production

Production is the live environment accessed by end users. It should be deployed on robust infrastructure with proper security measures.

```bash
./deployment_script.sh production
```

### Staging

Staging is a pre-production environment that mirrors production for testing before deploying new features.

```bash
./deployment_script.sh staging
```

### Development

Development environment for local testing and development.

```bash
./deployment_script.sh development
```

## Manual Deployment Steps

If you need to perform a manual deployment, follow these steps:

### 1. Backend Deployment

```bash
# Navigate to backend directory
cd backend

# Install dependencies
python -m pip install -r requirements.txt

# Set up environment variables
cp ../production.env .env  # Adjust as needed

# Run database migrations
python manage.py migrate

# Start the application
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

### 2. Frontend Deployment

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm ci --production

# Create environment file
cp ../production.env.frontend .env  # Adjust as needed

# Build the application
npm run build

# Deploy to web server
sudo cp -r build/* /var/www/html/smartprobono/
```

### 3. Web Server Configuration

Configure Nginx to serve the frontend and proxy API requests to the backend:

```nginx
# Frontend configuration
server {
    listen 80;
    server_name smartprobono.org www.smartprobono.org;
    
    location / {
        root /var/www/html/smartprobono;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}

# Backend API configuration
server {
    listen 80;
    server_name api.smartprobono.org;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. SSL Configuration

Set up SSL certificates using Certbot:

```bash
sudo certbot --nginx -d smartprobono.org -d www.smartprobono.org
sudo certbot --nginx -d api.smartprobono.org
```

### 5. Process Management

Set up systemd to manage the backend service:

```bash
sudo nano /etc/systemd/system/smartprobono_backend.service
```

Add the following content:

```
[Unit]
Description=SmartProBono Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/smartprobono/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn app:app --bind 0.0.0.0:5000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable smartprobono_backend
sudo systemctl start smartprobono_backend
```

## Environment Variables

The application requires various environment variables to function properly. Refer to production.env for a complete list of required variables.

Key environment variables include:

- `API_URL`: The URL of the backend API
- `JWT_SECRET`: Secret key for JWT token generation
- `DB_*`: Database connection parameters
- `SMTP_*`: Email server configuration
- `S3_*`: Storage configuration

## Database Management

### Backup

To manually create a database backup:

```bash
pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -F c -f backup_$(date +%Y%m%d%H%M%S).dump
```

### Restore

To restore from a backup:

```bash
pg_restore -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c backup_file.dump
```

## Troubleshooting

### Common Issues

1. **Backend Service Won't Start**
   - Check logs with: `sudo journalctl -u smartprobono_backend`
   - Verify environment variables are correctly set
   - Check for permission issues

2. **Frontend Shows Blank Screen**
   - Check browser console for errors
   - Verify API URL is correctly set
   - Ensure Nginx is properly configured

3. **Database Connection Failures**
   - Check database is running with: `sudo systemctl status postgresql`
   - Verify database credentials
   - Check firewall settings

### Get Help

If you encounter issues not covered by this guide, please contact the development team at support@smartprobono.org or create an issue in the repository. 