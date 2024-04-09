import random
import math
import os
import sys
from importlib import import_module

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../blockchain')))
from keys import Keys
from helper import compute_sha256_hash, encrypt_rsa, decrypt_rsa, generate_signature, generate_random_binary_string

class BlindSignatureProtocol():
    def __init__(self) -> None:
        self.pr_key_ca = None
        self.pb_key_ca = None
        self.pr_key_bn = None
        self.pb_key_bn = None
        self.blinding_factor = 1
        # assume we have a public key (n, e)
        self.modulus = 3233
        self.exponent = 17
    
    def perform_algorithm(self, token, candidate_id, num_candidates):
        point, lambda_num = self.ballot_conformation_algorithm(candidate_id, num_candidates)

        # read the keys
        self.read_keys_of_CA_and_BN()
        
        # encrypt 
        p_x = point[0].to_bytes(length=16, byteorder='big').hex()
        p_y = point[1].to_bytes(length=16, byteorder='big').hex()
        t1 = encrypt_rsa(p_x + p_y + compute_sha256_hash(hex(lambda_num)[2:]), self.pb_key_bn)

        # Blind the message
        blind_message = self.blind(compute_sha256_hash(bytes.hex(t1)))
        message_bytes = bytes(blind_message)

        # SEND MESSAGE TO 3rd CA
        # message = encrypt_rsa(token, self.pb_key_ca) + blind_message

        # --------------------------------
        # decrypt the token and verify it

        # get the blind message and produce a signature from it
        signature = generate_signature(message_bytes, self.pr_key_ca)
        # --------------------------------

        # get the t2 value 
        t2 = self.unblind(signature)
        t3 = encrypt_rsa(str(lambda_num), self.pb_key_ca)

        print("Transaction components before conversion: ", t1, t2, t3)

        return str(bytes.hex(t1)), str(hex(t2)[2:]), str(bytes.hex(t3))

    # Algorithm for masking and randomzing a voter's vote to make a brute force attack harder
    def ballot_conformation_algorithm(self, candidate_id, num_candidates):
        candidate_id = int(candidate_id)
        
        # Selects a random point on the linear equation: y = lambda * x + N
        def point_on_line(lambda_val, n_val):
            x_val = random.randint(1, 1000)
            n_val = int(str(n_val), 2)

            return (x_val, lambda_val * x_val + n_val)

        # Computing the number of zeros for masking
        lowerbound = 1
        upperbound = 256 - math.ceil(math.log2(num_candidates))
        num_zeros = random.randint(lowerbound, upperbound)
        zero_string = ''.join(['0' for _ in range(num_zeros)])

        # Masking the candidate id
        random_binary_string = generate_random_binary_string(16)
        binary_candidate_id = bin(candidate_id)[2:]
        masked_candidate_id = zero_string + binary_candidate_id + random_binary_string

        # Selecting a point,lambda combination 
        lambda_num = random.randint(1, 256)
        point = point_on_line(lambda_num, masked_candidate_id)

        return point, lambda_num

    def generate_blinding_factor(self):
        self.blinding_factor = random.randint(1, 1000)
        return self.blinding_factor

    # Simple blinding function
    def blind(self, message_to_blind):
        blinding_factor = self.generate_blinding_factor()
        blinded_message = (int(message_to_blind, 16) * pow(blinding_factor, self.exponent, self.modulus)) % self.modulus
        
        return blinded_message

    # calculate inverse of 'num' modulo 'm'
    def mod_inverse(self, num, m):
        original_m = m
        x0, x1 = 0, 1

        while num > 1:
            quotient = num // m
            m, num = num % m, m
            x0, x1 = x1 - quotient * x0, x0

        return x1 + original_m if x1 < 0 else x1

    def unblind(self, blinded_message):
        unblinded_message = (int.from_bytes(blinded_message, byteorder='little') * pow(self.mod_inverse(self.blinding_factor, self.modulus), self.exponent, self.modulus)) % self.modulus
        
        return unblinded_message

    def read_keys_of_CA_and_BN(self):
        self.pr_key_ca = Keys.read_key_from_pem_file("./../resources/keys/private_key_CA", "private")
        self.pb_key_ca = Keys.read_key_from_pem_file("./../resources/keys/public_key_CA", "public")
        self.pr_key_bn = Keys.read_key_from_pem_file("./../resources/keys/private_key_BN", "private")
        self.pb_key_bn = Keys.read_key_from_pem_file("./../resources/keys/public_key_BN", "public")
