from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64
import os
from typing import Dict, Optional
from datetime import datetime
import json

class EncryptionService:
    def __init__(self):
        self.fernet_key = self._load_or_generate_key()
        self.fernet = Fernet(self.fernet_key)
        self.data_path = os.path.join('data', 'encryption')
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_path, exist_ok=True)
        
    def _get_key_file(self, conversation_id: str) -> str:
        """Get path to conversation's key file"""
        return os.path.join(self.data_path, f"{conversation_id}_key.txt")

    def _load_or_generate_key(self):
        """Load existing key or generate a new one"""
        key_path = 'data/encryption/fernet.key'
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key
    
    def generate_key_pair(self):
        """Generate RSA key pair for asymmetric encryption"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        
        return {
            'private_key': private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ),
            'public_key': public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        }
    
    def encrypt_message(self, message: str) -> str:
        """Encrypt a message using Fernet (symmetric encryption)"""
        return self.fernet.encrypt(message.encode()).decode()
    
    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a Fernet-encrypted message"""
        return self.fernet.decrypt(encrypted_message.encode()).decode()
    
    def encrypt_file(self, file_path: str) -> str:
        """Encrypt a file and return the path to the encrypted file"""
        with open(file_path, 'rb') as file:
            data = file.read()
        
        encrypted_data = self.fernet.encrypt(data)
        encrypted_path = f"{file_path}.encrypted"
        
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_file_path: str) -> str:
        """Decrypt an encrypted file and return the path to the decrypted file"""
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = self.fernet.decrypt(encrypted_data)
        decrypted_path = encrypted_file_path.replace('.encrypted', '.decrypted')
        
        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        return decrypted_path
    
    def encrypt_json(self, data: dict) -> str:
        """Encrypt JSON data"""
        json_str = json.dumps(data)
        return self.encrypt_message(json_str)
    
    def decrypt_json(self, encrypted_data: str) -> dict:
        """Decrypt JSON data"""
        json_str = self.decrypt_message(encrypted_data)
        return json.loads(json_str)
    
    def generate_key_from_password(self, password: str, salt: bytes = None):
        """Generate a key from a password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_with_public_key(self, public_key_pem: bytes, message: str) -> bytes:
        """Encrypt data with a public key (asymmetric encryption)"""
        public_key = serialization.load_pem_public_key(public_key_pem)
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    
    def decrypt_with_private_key(self, private_key_pem: bytes, encrypted_message: bytes) -> str:
        """Decrypt data with a private key (asymmetric encryption)"""
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
        )
        decrypted = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

    def create_conversation(self, conversation_id: str, password: str) -> Dict:
        """Create a new encrypted conversation"""
        try:
            key, salt = self.generate_key_from_password(password)
            
            # Store key and salt
            with open(self._get_key_file(conversation_id), 'wb') as f:
                f.write(salt + b'\n' + key)
                
            return {
                'conversation_id': conversation_id,
                'status': 'created'
            }
        except Exception as e:
            raise Exception(f"Failed to create conversation: {str(e)}")

    def get_conversation_key(self, conversation_id: str, password: str) -> bytes:
        """Get encryption key for a conversation"""
        try:
            with open(self._get_key_file(conversation_id), 'rb') as f:
                salt = f.readline().strip()
                key, _ = self.generate_key_from_password(password, salt)
                return key
        except FileNotFoundError:
            raise Exception(f"Conversation {conversation_id} not found")
        except Exception as e:
            raise Exception(f"Failed to get conversation key: {str(e)}")

    def encrypt_message_for_conversation(self, conversation_id: str, password: str, message: str) -> str:
        """Encrypt a message for a conversation"""
        try:
            key = self.get_conversation_key(conversation_id, password)
            f = Fernet(key)
            encrypted_message = f.encrypt(message.encode())
            return base64.urlsafe_b64encode(encrypted_message).decode()
        except Exception as e:
            raise Exception(f"Failed to encrypt message: {str(e)}")

    def decrypt_message_for_conversation(self, conversation_id: str, password: str, encrypted_message: str) -> str:
        """Decrypt a message from a conversation"""
        try:
            key = self.get_conversation_key(conversation_id, password)
            f = Fernet(key)
            decoded_message = base64.urlsafe_b64decode(encrypted_message.encode())
            decrypted_message = f.decrypt(decoded_message)
            return decrypted_message.decode()
        except Exception as e:
            raise Exception(f"Failed to decrypt message: {str(e)}")

    def rotate_key(self, conversation_id: str, old_password: str, new_password: str) -> Dict:
        """Rotate encryption key for a conversation"""
        try:
            # Verify old password works
            self.get_conversation_key(conversation_id, old_password)
            
            # Generate new key
            new_key, new_salt = self.generate_key_from_password(new_password)
            
            # Store new key and salt
            with open(self._get_key_file(conversation_id), 'wb') as f:
                f.write(new_salt + b'\n' + new_key)
                
            return {
                'conversation_id': conversation_id,
                'status': 'rotated'
            }
        except Exception as e:
            raise Exception(f"Failed to rotate key: {str(e)}")

# Create global instance
encryption_service = EncryptionService() 