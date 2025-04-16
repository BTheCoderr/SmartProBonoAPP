from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64
import os

class EncryptionService:
    def __init__(self):
        self.symmetric_key = self._load_or_generate_key()
        self.fernet = Fernet(self.symmetric_key)
        
    def _load_or_generate_key(self):
        """Load existing key or generate a new one"""
        key_path = os.path.join('config', 'encryption.key')
        try:
            if os.path.exists(key_path):
                with open(key_path, 'rb') as key_file:
                    return key_file.read()
            else:
                key = Fernet.generate_key()
                os.makedirs('config', exist_ok=True)
                with open(key_path, 'wb') as key_file:
                    key_file.write(key)
                return key
        except Exception as e:
            # If file operations fail, generate an in-memory key
            return Fernet.generate_key()

    def encrypt_message(self, message: str) -> str:
        """Encrypt a message using symmetric encryption"""
        if not isinstance(message, str):
            message = str(message)
        encrypted = self.fernet.encrypt(message.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a message using symmetric encryption"""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_message.encode())
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt message: {str(e)}")

    def generate_key_pair(self):
        """Generate a new RSA key pair for asymmetric encryption"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        
        return private_key, public_key

    def serialize_public_key(self, public_key):
        """Serialize a public key to bytes"""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def serialize_private_key(self, private_key):
        """Serialize a private key to bytes"""
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    def encrypt_file(self, file_path: str, output_path: str = None) -> str:
        """Encrypt a file using symmetric encryption"""
        if output_path is None:
            output_path = file_path + '.encrypted'
            
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                
            encrypted_data = self.fernet.encrypt(file_data)
            
            with open(output_path, 'wb') as file:
                file.write(encrypted_data)
                
            return output_path
        except Exception as e:
            raise ValueError(f"Failed to encrypt file: {str(e)}")

    def decrypt_file(self, encrypted_file_path: str, output_path: str = None) -> str:
        """Decrypt a file using symmetric encryption"""
        if output_path is None:
            output_path = encrypted_file_path.replace('.encrypted', '.decrypted')
            
        try:
            with open(encrypted_file_path, 'rb') as file:
                encrypted_data = file.read()
                
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
                
            return output_path
        except Exception as e:
            raise ValueError(f"Failed to decrypt file: {str(e)}")

    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Derive a key from a password using PBKDF2"""
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

# Create a global instance
encryption_service = EncryptionService() 