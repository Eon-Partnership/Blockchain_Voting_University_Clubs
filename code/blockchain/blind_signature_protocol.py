import random
import math
from helper import generate_random_binary_string

class BlindSignatureProtocol():
    def __init__(self, candidate) -> None:
        self.t1 = None
        self.t2 = None
        self.t3 = None
    
    # Algorithm for masking and randomziing a a voter's vote to make a brute force attack harder
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

    def blind(self):
        pass

    def unblind(self):
        pass

    