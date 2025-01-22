import os
from dataclasses import dataclass


@dataclass
class SecurityConfig:
    maze_size: int = 12
    security_level: str = "medium"
    seed: bytes = None
    time_window: int = 90
    key_rotation: int = 1000
    max_path_attempts: int = 1000
    
    def __post_init__(self):
        if self.seed is None:
            self.seed = self.generate_seed()
    
    @staticmethod
    def generate_seed(length: int = 64) -> bytes:
        return os.urandom(length)