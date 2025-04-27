"""Encryption utilities for handling sensitive data."""
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import Union, Optional

# Initialize encryption key
def get_encryption_key() -> bytes:
    """Get or generate the encryption key."""
    key = os.environ.get('ENCRYPTION_KEY')
    if key:
        return base64.b64decode(key)
    
    # Generate a new key if none exists
    key = Fernet.generate_key()
    os.environ['ENCRYPTION_KEY'] = base64.b64encode(key).decode()
    return key

# Initialize Fernet cipher
_fernet = Fernet(get_encryption_key())

def encrypt_field(value: Union[str, bytes, None]) -> Optional[str]:
    """
    Encrypt a field value.
    
    Args:
        value: The value to encrypt
        
    Returns:
        str: The encrypted value as a base64 string, or None if input is None
    """
    if value is None:
        return None
    
    if isinstance(value, str):
        value = value.encode()
    
    try:
        encrypted = _fernet.encrypt(value)
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")

def decrypt_field(encrypted_value: Union[str, bytes, None]) -> Optional[str]:
    """
    Decrypt an encrypted field value.
    
    Args:
        encrypted_value: The encrypted value to decrypt
        
    Returns:
        str: The decrypted value, or None if input is None
    """
    if encrypted_value is None:
        return None
    
    if isinstance(encrypted_value, str):
        encrypted_value = base64.b64decode(encrypted_value)
    
    try:
        decrypted = _fernet.decrypt(encrypted_value)
        return decrypted.decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def mask_field(value: Optional[str], mask_char: str = '*') -> Optional[str]:
    """
    Mask a sensitive field value.
    
    Args:
        value: The value to mask
        mask_char: The character to use for masking
        
    Returns:
        str: The masked value, or None if input is None
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        value = str(value)
    
    # Keep first and last characters visible
    if len(value) <= 4:
        return mask_char * len(value)
    
    visible_start = 2
    visible_end = 2
    
    masked = (
        value[:visible_start] +
        mask_char * (len(value) - visible_start - visible_end) +
        value[-visible_end:]
    )
    return masked

def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, bytes]:
    """
    Hash a password using PBKDF2.
    
    Args:
        password: The password to hash
        salt: Optional salt bytes
        
    Returns:
        tuple: (hashed_password, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.b64encode(kdf.derive(password.encode()))
    return key.decode(), salt

def verify_password(password: str, hashed: str, salt: bytes) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: The password to verify
        hashed: The hashed password to compare against
        salt: The salt used in hashing
        
    Returns:
        bool: True if password matches, False otherwise
    """
    new_hash, _ = hash_password(password, salt)
    return new_hash == hashed 