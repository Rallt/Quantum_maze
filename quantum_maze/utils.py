import os
import hashlib
from datetime import datetime
from typing import Tuple

def generate_seed(length: int = 64) -> bytes:
    """Cryptographically secure seed generation"""
    return os.urandom(length)

def collect_entropy(*sources: bytes) -> bytes:
    """Combine multiple entropy sources"""
    return hashlib.sha3_512(b''.join(sources)).digest()

def time_based_nonce() -> bytes:
    """Generate time-based nonce for encryption"""
    return datetime.now().isoformat().encode()