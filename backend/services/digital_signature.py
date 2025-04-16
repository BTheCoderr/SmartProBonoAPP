from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from datetime import datetime
import os
import json
from typing import Dict, Optional, Tuple
from .audit_trail import audit_trail_service

class DigitalSignatureService:
    def __init__(self):
        self.keys_path = os.path.join('data', 'keys')
        self.signatures_path = os.path.join('data', 'signatures')
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.keys_path, exist_ok=True)
        os.makedirs(self.signatures_path, exist_ok=True)

    def generate_key_pair(self, user_id: str) -> Tuple[str, str]:
        """Generate a new RSA key pair for a user"""
        try:
            # Generate key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()

            # Serialize keys
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Save keys
            private_key_path = os.path.join(self.keys_path, f"{user_id}_private.pem")
            public_key_path = os.path.join(self.keys_path, f"{user_id}_public.pem")

            with open(private_key_path, 'wb') as f:
                f.write(private_pem)
            with open(public_key_path, 'wb') as f:
                f.write(public_pem)

            # Log key generation event
            audit_trail_service.log_event(
                entity_id=user_id,
                event_type='key_generation',
                user_id=user_id,
                details={'timestamp': datetime.now().isoformat()}
            )

            return public_key_path, private_key_path
        except Exception as e:
            raise ValueError(f"Failed to generate key pair: {str(e)}")

    def get_user_public_key(self, user_id: str) -> bytes:
        """Get a user's public key"""
        try:
            public_key_path = os.path.join(self.keys_path, f"{user_id}_public.pem")
            with open(public_key_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"Public key not found for user {user_id}")

    def get_user_private_key(self, user_id: str) -> bytes:
        """Get a user's private key"""
        try:
            private_key_path = os.path.join(self.keys_path, f"{user_id}_private.pem")
            with open(private_key_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"Private key not found for user {user_id}")

    def sign_document(self, user_id: str, document_id: str, document_hash: str) -> str:
        """Sign a document and return the signature ID"""
        try:
            # Load private key
            private_key_bytes = self.get_user_private_key(user_id)
            private_key = serialization.load_pem_private_key(
                private_key_bytes,
                password=None
            )

            # Create signature
            signature = private_key.sign(
                document_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Generate signature ID
            signature_id = f"sig_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"

            # Store signature metadata
            metadata = {
                'signature_id': signature_id,
                'document_id': document_id,
                'signer_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'signature': signature.hex()
            }

            signature_path = os.path.join(self.signatures_path, f"{signature_id}.json")
            with open(signature_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            # Log signature event
            audit_trail_service.log_event(
                entity_id=document_id,
                event_type='document_signed',
                user_id=user_id,
                details={
                    'signature_id': signature_id,
                    'timestamp': metadata['timestamp']
                }
            )

            return signature_id
        except Exception as e:
            raise ValueError(f"Failed to sign document: {str(e)}")

    def verify_signature(self, signature_id: str, document_hash: str) -> bool:
        """Verify a document signature"""
        try:
            # Load signature metadata
            metadata = self.get_signature_metadata(signature_id)
            if not metadata:
                return False

            # Load signer's public key
            public_key_bytes = self.get_user_public_key(metadata['signer_id'])
            public_key = serialization.load_pem_public_key(public_key_bytes)

            # Convert signature from hex
            signature = bytes.fromhex(metadata['signature'])

            # Verify signature
            try:
                public_key.verify(
                    signature,
                    document_hash.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                
                # Log verification event
                audit_trail_service.log_event(
                    entity_id=metadata['document_id'],
                    event_type='signature_verified',
                    user_id=metadata['signer_id'],
                    details={
                        'signature_id': signature_id,
                        'verification_time': datetime.now().isoformat(),
                        'result': 'valid'
                    }
                )
                
                return True
            except InvalidSignature:
                # Log failed verification
                audit_trail_service.log_event(
                    entity_id=metadata['document_id'],
                    event_type='signature_verified',
                    user_id=metadata['signer_id'],
                    details={
                        'signature_id': signature_id,
                        'verification_time': datetime.now().isoformat(),
                        'result': 'invalid'
                    }
                )
                return False
        except Exception as e:
            raise ValueError(f"Failed to verify signature: {str(e)}")

    def get_signature_metadata(self, signature_id: str) -> Optional[Dict]:
        """Get metadata for a signature"""
        try:
            signature_path = os.path.join(self.signatures_path, f"{signature_id}.json")
            with open(signature_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def list_user_signatures(self, user_id: str) -> list:
        """List all signatures by a user"""
        signatures = []
        try:
            for filename in os.listdir(self.signatures_path):
                if filename.endswith('.json'):
                    signature_path = os.path.join(self.signatures_path, filename)
                    with open(signature_path, 'r') as f:
                        metadata = json.load(f)
                        if metadata['signer_id'] == user_id:
                            signatures.append(metadata)
            return signatures
        except Exception:
            return []

# Create a global instance
digital_signature_service = DigitalSignatureService() 
