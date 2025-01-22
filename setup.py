from setuptools import setup, find_packages

setup(
    name="quantum_maze",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'cryptography>=36.0.0',
    ],
    entry_points={
        'console_scripts': [
            'qmaze=quantum_maze.cli:main',
        ],
    },
    python_requires='>=3.8',
    author="Taxman",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)