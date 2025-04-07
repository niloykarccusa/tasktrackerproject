import os
from cryptography.fernet import Fernet

KEY_FILE_PATH = os.path.join(os.path.expanduser("~"), ".session_key")

def generate_or_load_key():
    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, "wb") as key_file:
            key_file.write(key)

    return key

ENCRYPTION_KEY = generate_or_load_key()