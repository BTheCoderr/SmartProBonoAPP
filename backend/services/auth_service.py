import pyotp
import qrcode
import base64
from io import BytesIO
from datetime import datetime, timedelta
import jwt
from typing import Dict, Optional, Tuple
import bcrypt
from .encryption_service import encryption_service

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.token_expiry = timedelta(hours=1)
        self.refresh_token_expiry = timedelta(days=7)
    
    def hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def verify_password(self, password: str, hashed: bytes) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode(), hashed)
    
    def generate_2fa_secret(self) -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    def get_2fa_qr_code(self, email: str, secret: str) -> str:
        """Generate QR code for 2FA setup"""
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(email, issuer_name="SmartProBono")
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def verify_2fa_token(self, secret: str, token: str) -> bool:
        """Verify a 2FA token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def generate_tokens(self, user_id: str, is_2fa_enabled: bool) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        now = datetime.utcnow()
        
        # Access token payload
        access_payload = {
            'user_id': user_id,
            'type': 'access',
            '2fa_enabled': is_2fa_enabled,
            'exp': now + self.token_expiry,
            'iat': now
        }
        
        # Refresh token payload
        refresh_payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': now + self.refresh_token_expiry,
            'iat': now
        }
        
        # Encrypt tokens
        access_token = encryption_service.encrypt_message(
            jwt.encode(access_payload, self.secret_key, algorithm='HS256')
        )
        refresh_token = encryption_service.encrypt_message(
            jwt.encode(refresh_payload, self.secret_key, algorithm='HS256')
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': int(self.token_expiry.total_seconds())
        }
    
    def verify_token(self, token: str, token_type: str = 'access') -> Tuple[bool, Optional[Dict]]:
        """Verify and decode a token"""
        try:
            # Decrypt token
            decrypted_token = encryption_service.decrypt_message(token)
            
            # Decode and verify token
            payload = jwt.decode(decrypted_token, self.secret_key, algorithms=['HS256'])
            
            # Verify token type
            if payload.get('type') != token_type:
                return False, None
            
            return True, payload
        except (jwt.InvalidTokenError, Exception):
            return False, None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Generate new access token using refresh token"""
        is_valid, payload = self.verify_token(refresh_token, 'refresh')
        if not is_valid:
            return None
        
        # Get user from payload
        user_id = payload.get('user_id')
        if not user_id:
            return None
        
        # Generate new access token
        now = datetime.utcnow()
        access_payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': now + self.token_expiry,
            'iat': now
        }
        
        access_token = encryption_service.encrypt_message(
            jwt.encode(access_payload, self.secret_key, algorithm='HS256')
        )
        
        return {
            'access_token': access_token,
            'expires_in': int(self.token_expiry.total_seconds())
        }
    
    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """Revoke a refresh token"""
        is_valid, payload = self.verify_token(refresh_token, 'refresh')
        if not is_valid:
            return False
        
        # In a production environment, you would add the token to a blacklist
        # or remove it from a whitelist in your database
        return True

# Create a global instance with a secure secret key
# auth_service = AuthService('your-secure-secret-key-here')

def init_auth_service(app=None):
    """Initialize the auth service with the app's secret key"""
    from flask import current_app
    secret_key = None
    
    if app:
        secret_key = app.config.get('JWT_SECRET_KEY')
    else:
        try:
            secret_key = current_app.config.get('JWT_SECRET_KEY')
        except RuntimeError:
            # If running outside of application context
            secret_key = 'temporary-key-replace-in-context'
            
    return AuthService(secret_key)

def get_auth_service():
    """Get or create the auth service"""
    try:
        from flask import current_app, g
        if 'auth_service' not in g:
            g.auth_service = AuthService(current_app.config.get('JWT_SECRET_KEY'))
        return g.auth_service
    except (RuntimeError, ImportError):
        # If running outside of application context
        return AuthService('temporary-key-replace-in-context') 