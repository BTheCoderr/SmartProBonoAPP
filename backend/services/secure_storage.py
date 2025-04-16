import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import json
from utils.encryption import encryption_service

class SecureStorageService:
    def __init__(self):
        self.base_path = os.path.join('data', 'secure_storage')
        self.metadata_path = os.path.join(self.base_path, 'metadata')
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.metadata_path, exist_ok=True)

    def _get_file_path(self, file_id: str) -> str:
        """Get the full path for a file"""
        return os.path.join(self.base_path, f"{file_id}.encrypted")

    def _get_metadata_path(self, file_id: str) -> str:
        """Get the full path for a file's metadata"""
        return os.path.join(self.metadata_path, f"{file_id}.json")

    def _generate_file_id(self) -> str:
        """Generate a unique file ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"file_{timestamp}_{os.urandom(4).hex()}"

    def store_file(self, file_path: str, metadata: Dict) -> str:
        """
        Store a file securely with encryption
        Returns the file ID
        """
        try:
            file_id = self._generate_file_id()
            encrypted_path = self._get_file_path(file_id)
            
            # Encrypt and store the file
            encryption_service.encrypt_file(file_path, encrypted_path)
            
            # Store metadata
            metadata.update({
                'file_id': file_id,
                'created_at': datetime.now().isoformat(),
                'original_filename': os.path.basename(file_path),
                'encrypted_path': encrypted_path
            })
            
            with open(self._get_metadata_path(file_id), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return file_id
        except Exception as e:
            raise ValueError(f"Failed to store file securely: {str(e)}")

    def retrieve_file(self, file_id: str, output_path: str) -> str:
        """
        Retrieve and decrypt a file
        Returns the path to the decrypted file
        """
        try:
            encrypted_path = self._get_file_path(file_id)
            if not os.path.exists(encrypted_path):
                raise FileNotFoundError(f"File {file_id} not found")
            
            return encryption_service.decrypt_file(encrypted_path, output_path)
        except Exception as e:
            raise ValueError(f"Failed to retrieve file: {str(e)}")

    def get_metadata(self, file_id: str) -> Optional[Dict]:
        """Get metadata for a file"""
        try:
            metadata_path = self._get_metadata_path(file_id)
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def update_metadata(self, file_id: str, metadata_updates: Dict) -> bool:
        """Update metadata for a file"""
        try:
            current_metadata = self.get_metadata(file_id)
            if not current_metadata:
                return False
            
            current_metadata.update(metadata_updates)
            current_metadata['updated_at'] = datetime.now().isoformat()
            
            with open(self._get_metadata_path(file_id), 'w') as f:
                json.dump(current_metadata, f, indent=2)
            
            return True
        except Exception:
            return False

    def delete_file(self, file_id: str) -> bool:
        """Delete a file and its metadata"""
        try:
            # Delete encrypted file
            file_path = self._get_file_path(file_id)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete metadata
            metadata_path = self._get_metadata_path(file_id)
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            return True
        except Exception:
            return False

    def list_files(self, filters: Dict = None) -> List[Dict]:
        """List all files with their metadata"""
        try:
            files = []
            for filename in os.listdir(self.metadata_path):
                if filename.endswith('.json'):
                    file_id = filename[:-5]  # Remove .json extension
                    metadata = self.get_metadata(file_id)
                    if metadata:
                        if filters:
                            # Apply filters
                            match = all(
                                metadata.get(key) == value 
                                for key, value in filters.items()
                            )
                            if match:
                                files.append(metadata)
                        else:
                            files.append(metadata)
            
            return sorted(files, key=lambda x: x['created_at'], reverse=True)
        except Exception:
            return []

# Create a global instance
secure_storage = SecureStorageService() 