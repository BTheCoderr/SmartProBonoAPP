import os
from dotenv import load_dotenv

load_dotenv()

# AI Model API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
FALCON_API_KEY = os.getenv('FALCON_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# Service API Keys
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')

SMTP_CONFIG = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': 'your-email@gmail.com',  # Replace with actual email
    'password': 'your-app-password',     # Replace with actual app password
    'use_tls': True,
    'sender': 'SmartProBono <noreply@smartprobono.com>'
}

def validate_api_keys():
    """Validate that required API keys are present"""
    required_keys = {
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'ANTHROPIC_API_KEY': ANTHROPIC_API_KEY,
        'MISTRAL_API_KEY': MISTRAL_API_KEY,
        'LLAMA_API_KEY': LLAMA_API_KEY,
        'FALCON_API_KEY': FALCON_API_KEY,
        'DEEPSEEK_API_KEY': DEEPSEEK_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
        return False
    return True 