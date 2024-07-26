import secrets
import base64

# Generate a secure random key
key = secrets.token_bytes(32)  # 32 bytes is a good size for HS256

# Encode the key in base64 for easier use in configurations
key_base64 = base64.urlsafe_b64encode(key).decode('utf-8')

print("Generated Key (Base64):", key_base64)