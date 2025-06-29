#!/usr/bin/env python3
"""Quick Fernet key generator - ready to paste in .env file"""

from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()

print("=== Fernet Key for .env file ===")
print()
print("Copy this line to your .env file:")
print(f"FERNET_KEY={key.decode()}")
print()
print("Or just the key value:")
print(key.decode())
print()
print(f"Key length: {len(key)} bytes")
print()
print("=== Usage in your code ===")
print("When reading from .env file:")
print("import os")
print("from cryptography.fernet import Fernet")
print("key_string = os.getenv('FERNET_KEY')")
print("key_bytes = key_string.encode()  # Convert string back to bytes")
print("f = Fernet(key_bytes)") 