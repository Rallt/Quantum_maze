class QuantumMazeError(Exception):
    """Base exception for maze generation errors"""


class QuantumSecurityError(Exception):
    """Exception for security constraint violations"""


class QuantumCryptoError(Exception):
    """Cryptographic operation failure"""


class PathValidationError(QuantumSecurityError):
    """Invalid path configuration"""