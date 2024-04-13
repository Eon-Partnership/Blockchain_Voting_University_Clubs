import random
import string
from hashlib import sha256
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Generates a random string
def generate_random_string(length):
    # The set of characters to choose from
    characters = string.ascii_letters + string.digits

    #Creating the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

# Generate a random binary string
def generate_random_binary_string(length):
    # Generate a list of random binary digits (0 or 1) of the specified length
    binary_digits = [random.choice('01') for _ in range(length)]
    
    # Join the list of binary digits into a string
    binary_string = ''.join(binary_digits)
    
    return binary_string

# Computes a sha256 hash on a string of hexadeimal digits
def compute_sha256_hash(hex_string):
    input_bytes_string = bytes.fromhex(hex_string)
    hash_object = sha256(input_bytes_string)
    hex_digest = hash_object.hexdigest()

    return hex_digest

def encrypt_rsa(message, pb_key):
    encrypted_message = pb_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message    

def decrypt_rsa(enc_message, pr_key):
    # Decrypt the message using RSA-OAEP padding
    decrypted_message = pr_key.decrypt(
        enc_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message.decode()

def generate_signature(hash_value, private_key):

    # Sign the hash value using the private key
    signature = private_key.sign(
        hash_value,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature