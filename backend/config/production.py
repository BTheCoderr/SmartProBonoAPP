"""Production configuration"""
import os
from datetime import timedelta

# Security
SECRET_KEY = os.environ.get('SECRET_KEY') or 'generate-a-secure-key-in-production'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'generate-a-secure-jwt-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Rate Limiting
RATELIMIT_DEFAULT = "200 per day"
RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or "memory://"

# Cache
CACHE_TYPE = "redis"
CACHE_REDIS_URL = os.environ.get('REDIS_URL')
CACHE_DEFAULT_TIMEOUT = 300

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# CORS
CORS_ORIGINS = [
    'https://smartprobono.org',
    'https://www.smartprobono.org',
    'http://localhost:3000',
    'http://localhost:5002'
]

# File Upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

# AI Service
OLLAMA_ENDPOINT = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
DEFAULT_AI_MODEL = 'mistral'
AI_TIMEOUT = 60  # seconds

# Queue Settings
QUEUE_SNAPSHOT_INTERVAL = 3600  # 1 hour
QUEUE_CACHE_TTL = 300  # 5 minutes

# Email
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_USE_TLS = True

# Admin
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@smartprobono.org') 