import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

# Generate AES key from password
def generate_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Encrypt file
def encrypt_file(file_path, password):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    encrypted_file = file_path + ".enc"
    with open(encrypted_file, "wb") as f:
        f.write(salt + encrypted)

    print(f"[+] File encrypted successfully: {encrypted_file}")

# Decrypt file
def decrypt_file(encrypted_file, password):
    with open(encrypted_file, "rb") as f:
        salt = f.read(16)
        encrypted_data = f.read()

    key = generate_key(password, salt)
    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted_data)

    output_file = encrypted_file.replace(".enc", "")
    with open(output_file, "wb") as f:
        f.write(decrypted)

    print(f"[+] File decrypted successfully: {output_file}")

# CLI
if __name__ == "__main__":
    print("1. Encrypt File")
    print("2. Decrypt File")
    choice = input("Choose option: ")

    file_path = input("Enter file path: ")
    password = input("Enter password: ")

    if choice == "1":
        encrypt_file(file_path, password)
    elif choice == "2":
        decrypt_file(file_path, password)
    else:
        print("Invalid option")
