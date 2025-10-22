"""
Encryption Manager for AI Clinical Notes Assistant
Handles AES-256 encryption/decryption of sensitive data
"""
from cryptography.fernet import Fernet
import os
from pathlib import Path

class EncryptionManager:
    def __init__(self, key_path=None):
        """
        Initialize encryption manager
        Args:
            key_path: Path to encryption key file
        """
        if key_path is None:
            key_path = Path(__file__).parent.parent / "data" / ".encryption.key"

        self.key_path = Path(key_path)
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)

    def _load_or_create_key(self):
        """Load existing key or create a new one"""
        if self.key_path.exists():
            with open(self.key_path, 'rb') as f:
                return f.read()
        else:
            # Create new key
            key = Fernet.generate_key()
            # Ensure directory exists
            self.key_path.parent.mkdir(parents=True, exist_ok=True)
            # Save key
            with open(self.key_path, 'wb') as f:
                f.write(key)
            # Set restrictive permissions (Unix-like systems)
            try:
                os.chmod(self.key_path, 0o600)
            except:
                pass
            return key

    def encrypt(self, data):
        """
        Encrypt data
        Args:
            data: String or bytes to encrypt
        Returns:
            Encrypted bytes
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data):
        """
        Decrypt data
        Args:
            encrypted_data: Encrypted bytes
        Returns:
            Decrypted string
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode('utf-8')

    def encrypt_file(self, input_path, output_path=None):
        """
        Encrypt a file
        Args:
            input_path: Path to file to encrypt
            output_path: Path to save encrypted file (defaults to input_path + .enc)
        """
        input_path = Path(input_path)
        if output_path is None:
            output_path = Path(str(input_path) + '.enc')

        with open(input_path, 'rb') as f:
            data = f.read()

        encrypted = self.encrypt(data)

        with open(output_path, 'wb') as f:
            f.write(encrypted)

        return output_path

    def decrypt_file(self, input_path, output_path=None):
        """
        Decrypt a file
        Args:
            input_path: Path to encrypted file
            output_path: Path to save decrypted file
        """
        input_path = Path(input_path)
        if output_path is None:
            output_path = Path(str(input_path).replace('.enc', ''))

        with open(input_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted = self.decrypt(encrypted_data)

        with open(output_path, 'w') as f:
            f.write(decrypted)

        return output_path
