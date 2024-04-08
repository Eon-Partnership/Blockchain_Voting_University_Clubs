from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from helper import generate_random_string
from exceptions.key_exception import KeyException

class Keys():
    @staticmethod
    def generate_key_pair(write_key_to_file = False):
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Retrieve the public key
        public_key = private_key.public_key()
        
        # Serialize the private key to PEM format
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize the public key to PEM format
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Convert bytes to strings (for easier storage, printing, etc.)
        str_private_key = pem_private_key.decode('utf-8')
        str_public_key = pem_public_key.decode('utf-8')

        # Conditional writing to file:
        if write_key_to_file:
            # Creating the file names
            public_key_file_name = 'public_key_' + generate_random_string(16)
            private_key_file_name = 'private_key_' + generate_random_string(16)

            # Writing keys to file
            with open("./" + public_key_file_name, 'w') as file:
                file.write(str_public_key)

            with open("./" + private_key_file_name, 'w') as file:
                file.write(str_private_key)
            
            print(f'Public key written to: {public_key_file_name}')
            print(f'Private key written to: {private_key_file_name}')
        
        return str_private_key, str_public_key

    @staticmethod
    def read_raw_key_from_file(filename):
        # Read the contents of the public key file
        with open(filename, "r") as key_file:
            lines = key_file.readlines()

        # Ensuring that the key file is in a semi-valid format
        if len(lines) <= 2:
            raise KeyException("Invalid Key File")
        
        # Cutting out begin/end statements
        valid_lines = lines[1:-1]

        # Stripping the new lines and creating a single key string
        key_string = ''.join(line.rstrip('\n') for line in valid_lines)
        
        return key_string

    @staticmethod
    def read_key_from_pem_file(file_path, file_type):
        # Open and read the PEM file
        with open(file_path, "rb") as pem_file:
            pem_data = pem_file.read()

        if file_type == 'public':
            key = serialization.load_pem_public_key(pem_data)
        elif file_type == 'private':
            key = serialization.load_pem_private_key(pem_data, None)
        
        return key

# Generate a key pair
# private_key, public_key = Keys.generate_key_pair(write_key_to_file=True)
# print(Keys.read_key_from_file('./private_key_bn', 'private'))
