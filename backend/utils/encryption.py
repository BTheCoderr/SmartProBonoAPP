"""
Encryption utilities for secure data storage and transmission.
"""
import os
import base64
import json
from typing import Dict, Any, Union, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from flask import current_app

# Constants for encryption
DEFAULT_ITERATIONS = 100000
HASH_ALGORITHM = hashes.SHA256()
KEY_LENGTH = 32  # bytes

class EncryptionService:
    """Service for encrypting and decrypting sensitive data."""
    
    def __init__(self, secret_key: str = None):
        """Initialize the encryption service with a secret key."""
        self.secret_key = secret_key or os.environ.get('ENCRYPTION_KEY')
        if not self.secret_key:
            raise ValueError("Encryption key is required")
        
        # Derive a key from the secret key
        self.key = self._derive_key(self.secret_key.encode())
        self.fernet = Fernet(base64.urlsafe_b64encode(self.key))
    
    def _derive_key(self, password: bytes, salt: bytes = None) -> bytes:
        """Derive a key from a password and salt using PBKDF2."""
        if salt is None:
            # Use a static salt for consistency
            # In a production system, you might want to use a secure, 
            # per-application salt stored elsewhere
            salt = b'smartprobono_static_salt'
            
        kdf = PBKDF2HMAC(
            algorithm=HASH_ALGORITHM,
            length=KEY_LENGTH,
            salt=salt,
            iterations=DEFAULT_ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password)
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        if not data:
            return data
            
        encoded_data = data.encode('utf-8')
        encrypted_data = self.fernet.encrypt(encoded_data)
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt an encrypted string."""
        if not encrypted_data:
            return encrypted_data
            
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    def encrypt_dict(self, data: Dict[str, Any], fields_to_encrypt: List[str] = None) -> Dict[str, Any]:
        """Encrypt specified fields in a dictionary."""
        if not data:
            return data
            
        encrypted_data = data.copy()
        
        # If no fields specified, encrypt everything
        if not fields_to_encrypt:
            for key, value in encrypted_data.items():
                if isinstance(value, str):
                    encrypted_data[key] = self.encrypt(value)
                elif isinstance(value, dict):
                    encrypted_data[key] = self.encrypt_dict(value)
                elif isinstance(value, list):
                    encrypted_data[key] = self.encrypt_list(value)
            return encrypted_data
        
        # Encrypt only specified fields
        for field in fields_to_encrypt:
            if field in encrypted_data and isinstance(encrypted_data[field], str):
                encrypted_data[field] = self.encrypt(encrypted_data[field])
        
        return encrypted_data
    
    def decrypt_dict(self, encrypted_data: Dict[str, Any], fields_to_decrypt: List[str] = None) -> Dict[str, Any]:
        """Decrypt specified fields in a dictionary."""
        if not encrypted_data:
            return encrypted_data
            
        decrypted_data = encrypted_data.copy()
        
        # If no fields specified, decrypt everything
        if not fields_to_decrypt:
            for key, value in decrypted_data.items():
                if isinstance(value, str):
                    try:
                        decrypted_data[key] = self.decrypt(value)
                    except:
                        # If decryption fails, assume it wasn't encrypted
                        pass
                elif isinstance(value, dict):
                    decrypted_data[key] = self.decrypt_dict(value)
                elif isinstance(value, list):
                    decrypted_data[key] = self.decrypt_list(value)
            return decrypted_data
        
        # Decrypt only specified fields
        for field in fields_to_decrypt:
            if field in decrypted_data and isinstance(decrypted_data[field], str):
                try:
                    decrypted_data[field] = self.decrypt(decrypted_data[field])
                except:
                    # If decryption fails, assume it wasn't encrypted
                    pass
        
        return decrypted_data
    
    def encrypt_list(self, data_list: List[Any]) -> List[Any]:
        """Encrypt items in a list."""
        if not data_list:
            return data_list
            
        encrypted_list = []
        for item in data_list:
            if isinstance(item, str):
                encrypted_list.append(self.encrypt(item))
            elif isinstance(item, dict):
                encrypted_list.append(self.encrypt_dict(item))
            elif isinstance(item, list):
                encrypted_list.append(self.encrypt_list(item))
            else:
                encrypted_list.append(item)
        
        return encrypted_list
    
    def decrypt_list(self, encrypted_list: List[Any]) -> List[Any]:
        """Decrypt items in a list."""
        if not encrypted_list:
            return encrypted_list
            
        decrypted_list = []
        for item in encrypted_list:
            if isinstance(item, str):
                try:
                    decrypted_list.append(self.decrypt(item))
                except:
                    # If decryption fails, assume it wasn't encrypted
                    decrypted_list.append(item)
            elif isinstance(item, dict):
                decrypted_list.append(self.decrypt_dict(item))
            elif isinstance(item, list):
                decrypted_list.append(self.decrypt_list(item))
            else:
                decrypted_list.append(item)
        
        return decrypted_list

# Singleton instance
_encryption_service = None

def get_encryption_service() -> EncryptionService:
    """Get the encryption service singleton."""
    global _encryption_service
    if _encryption_service is None:
        try:
            secret_key = current_app.config.get('SECRET_KEY') or os.environ.get('ENCRYPTION_KEY')
            _encryption_service = EncryptionService(secret_key)
        except RuntimeError:
            # Outside of application context, use environment variable
            secret_key = os.environ.get('ENCRYPTION_KEY', 'development_key_not_secure')
            _encryption_service = EncryptionService(secret_key)
    return _encryption_service

def encrypt_field(value: str) -> str:
    """Encrypt a single field."""
    return get_encryption_service().encrypt(value)

def decrypt_field(value: str) -> str:
    """Decrypt a single field."""
    return get_encryption_service().decrypt(value)

def mask_field(value: str, visible_chars: int = 4) -> str:
    """Mask a sensitive field, showing only a few characters."""
    if not value:
        return value
        
    if len(value) <= visible_chars:
        return '*' * len(value)
        
    # Show last few characters
    return '*' * (len(value) - visible_chars) + value[-visible_chars:]

def encrypt_document(document: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
    """Encrypt sensitive fields in a document."""
    return get_encryption_service().encrypt_dict(document, sensitive_fields)

def decrypt_document(document: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
    """Decrypt sensitive fields in a document."""
    return get_encryption_service().decrypt_dict(document, sensitive_fields) 