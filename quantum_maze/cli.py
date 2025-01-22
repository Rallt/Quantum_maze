import argparse
from .core import QuantumMaze, QuantumNavigator, PostQuantumCipher
from .config.security import SecurityConfig
from .exceptions import QuantumMazeError, QuantumSecurityError


def main():
    parser = argparse.ArgumentParser(
        description="Quantum-Resistant 3D Maze Cryptography System"
    )
    
    # Command line arguments
    parser.add_argument('-s', '--size', type=int, default=12,
                        help='Maze dimension (default: 12)')
    parser.add_argument('-t', '--time', type=int, default=90,
                        help='Time window in seconds (default: 90)')
    parser.add_argument('-l', '--level', choices=['low', 'medium', 'high'],
                        default='medium', help='Security level')
    
    args = parser.parse_args()
    
    try:
        config = SecurityConfig(
            maze_size=args.size,
            time_window=args.time,
            security_level=args.level
        )
        
        # Execute core workflow
        maze = QuantumMaze(config)
        nav = QuantumNavigator(maze, config)
        
        if path := nav.find_secure_path():
            cipher = PostQuantumCipher(nav, config)
            # ... (Demo encryption/decryption workflow) ...
    
    except (QuantumMazeError, QuantumSecurityError) as e:
        print(f"Security Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()