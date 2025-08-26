from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_hash(masterpass):
    # Convert the master password to bytes
    masterpass = masterpass.encode()

    # create a SHA256 hash object using the default backend
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

    # Update the hash object with the master password
    digest.update(masterpass)

    # Get the final digest of the hash object and return it
    hashed_password = digest.finalize()
    return hashed_password


def generate_key():
    # This function generates a random key using the Fernet library

    return Fernet.generate_key()
