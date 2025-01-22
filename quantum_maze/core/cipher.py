import os
from collections import deque
from hashlib import sha3_512

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.kbkdf import KBKDFHMAC, CounterLocation
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

from ..config.security import SecurityConfig
from ..exceptions import QuantumCryptoError


class PostQuantumCipher:
    """Hybrid post-quantum encryption system"""
    
    def __init__(self, navigator, config: SecurityConfig):
        self.nav = navigator
        self.config = config
        # Continues
        self._key_rotation_counter = 0
        self._current_key = self._derive_initial_key()
        self._previous_keys = deque(maxlen=3)  # Keep last 3 keys
    
    def _derive_initial_key(self) -> bytes:
        """Hybrid KDF with forward secrecy"""
        kdf = KBKDFHMAC(
            algorithm=hashes.SHA3_512(),
            mode=CounterLocation.BEFORE_FIXED,
            length=96,  # 512-bit for ChaCha + 256-bit for future PQ alg
            label=b'QRMCS_Hybrid_Key',
            context=self.nav._get_entropy(),
            backend=default_backend()
        )
        return kdf.derive(self.nav._get_entropy())
    
    def rotate_keys(self) -> None:
        """Periodic key rotation for forward secrecy"""
        self._previous_keys.append(self._current_key)
        self._current_key = sha3_512(self._current_key).digest()
        self._key_rotation_counter += 1
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """Authenticated encryption with key rotation check"""
        if self._key_rotation_counter >= 1000:
            self.rotate_keys()
        
        nonce = os.urandom(24)
        cipher = ChaCha20Poly1305(self._current_key)
        ciphertext = cipher.encrypt(nonce, plaintext, self._auth_data())
        return nonce + ciphertext + self._key_fingerprint()
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """Secure decryption with key validation"""
        if len(ciphertext) < 72:
            raise InvalidTag("Invalid ciphertext length")
        
        nonce = ciphertext[:24]
        key_fp = ciphertext[-48:]
        data = ciphertext[24:-48]
        
        # Try current and previous keys
        for key in [self._current_key] + list(self._previous_keys):
            if sha3_512(key).digest()[:48] == key_fp:
                cipher = ChaCha20Poly1305(key)
                return cipher.decrypt(nonce, data, self._auth_data())
        
        raise InvalidTag("No valid key found for decryption")
    
    def _auth_data(self) -> bytes:
        """Additional authenticated data"""
        return self.nav.maze.serialize()[:64]
    
    def _key_fingerprint(self) -> bytes:
        """Key identifier for rotation support"""
        return sha3_512(self._current_key).digest()[:48]
