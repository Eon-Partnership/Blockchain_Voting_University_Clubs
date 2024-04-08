import random
import math
from helper import generate_random_binary_string
from helper import read_data_from_file 

class BlindSignatureProtocol():
    def __init__(self) -> None:
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.pr_key_ca = None
        self.pb_key_ca = None
        self.pr_key_bn = None
        self.pb_key_bn = None
        self.blinding_factor = 1
        # assume we have a public key (n, e)
        self.modulus = 3233
        self.exponent = 17
    
    # Algorithm for masking and randomzing a voter's vote to make a brute force attack harder
    def ballot_conformation_algorithm(self, candidate_id, num_candidates):
        
        # Selects a random point on the linear equation: y = lambda * x + N
        def point_on_line(lambda_val, n_val):
            x_val = random.randint(-100000000, 100000000)
            n_val = int(n_val, 2)

            return (x_val, lambda_val * x_val + n_val)

        # Computing the number of zeros for masking
        lowerbound = 1
        upperbound = 256 - math.ceil(math.log2(num_candidates))
        num_zeros = random.randint(lowerbound, upperbound)
        zero_string = ''.join(['0' for _ in range(num_zeros)])

        # Masking the candidate id
        random_binary_string = generate_random_binary_string(256)
        binary_candidate_id = bin(candidate_id)
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
        blinded_message = (message_to_blind * pow(blinding_factor, self.exponent, self.modulus)) % self.modulus
        return blinded_message

    # calculate inverse of 'num' modulo 'm'
    def mod_inverse(num, m):
        original_m = m
        x0, x1 = 0, 1

        while num > 1:
            quotient = num // m
            m, num = num % m, m
            x0, x1 = x1 - quotient * x0, x0

        return x1 + original_m if x1 < 0 else x1

    def unblind(self, blinded_message):
        unblinded_message = (blinded_message * pow(self.mod_inverse(self.blinding_factor, self.modulus), self.exponent, self.modulus)) % self.modulus
        return unblinded_message

    def read_keys_of_CA_and_BN(self):
        self.pr_key_ca = read_data_from_file("./../resources/private_key_CA")
        self.pb_key_ca = read_data_from_file("./../resources/public_key_CA")
        self.pr_key_bn = read_data_from_file("./../resources/private_key_BN")
        self.pb_key_bn = read_data_from_file("./../resources/public_key_BN")

    