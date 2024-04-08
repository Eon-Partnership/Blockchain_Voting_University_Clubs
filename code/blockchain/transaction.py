from hashlib import sha256
from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, transaction_type, timestamp) -> None:
        self.type = transaction_type
        self.timestamp = self.initialize_timestamp(timestamp)
    
    @abstractmethod
    def compute_hash(self):
        pass
    
    # Ensure the timestamp is a string
    def initialize_timestamp(self, timestamp):
        if isinstance(timestamp, str):
            return timestamp

        return str(timestamp)
    
    # Compute a sha256 hash on a string
    def compute_sha256_hash(self, string):
            input_bytes_string = bytes.fromhex(string)
            hash_object = sha256(input_bytes_string)
            hex_digest = hash_object.hexdigest()

            return hex_digest

class VoteTransaction(Transaction):
    def __init__(self, ballot_point, ballot_slope, ballot_signature, timestamp):
        # Encrypted candidiate information for a ballot 
        self.ballot_point = ballot_point # Enc(P || H(lambda), PK_BN)
        self.ballot_slope = ballot_slope # Enc(H(ballot_point), SK_CA)
        self.ballot_signature = ballot_signature # Enc(lambda, PK_CA)

        # Calling super class constructor
        super().__init__('vote', timestamp)

        # Initializing the transaction hash
        self.transaction_hash = self.compute_hash()
    
    # Computes the hash for a VoteTransaction
    def compute_hash(self):
        # Concatenating the transaction components to compute a hash
        # ballot_point || ballot_slope || ballot_signature || timestamp
        string_to_hash = self.ballot_point + self.ballot_slope + self.ballot_signature + self.timestamp
        hex_string_to_hash = string_to_hash.encode('utf-8').hex()

        # Applying the double sha-256 hash
        first_hash_hex = self.compute_sha256_hash(hex_string_to_hash)
        second_hash_hex = self.compute_sha256_hash(first_hash_hex)
        
        return second_hash_hex

class KeyTransaction(Transaction):
    def __init__(self, central_authority_key, blockchain_network_key, timestamp):
        # Central Authority and Blockchain Network key to start and end an election
        self.central_authority_key = central_authority_key
        self.blockchain_network_key = blockchain_network_key

        # Calling super class constructor
        super().__init__('key', timestamp)

        # Initializing the transaction hash
        self.transaction_hash = self.compute_hash()
    
     # Computes the hash for a VoteTransaction
    def compute_hash(self):
        # Concatenating the transaction components to compute a hash
        # ballot_point || ballot_slope || ballot_signature || timestamp
        string_to_hash = self.central_authority_key + self.blockchain_network_key + self.timestamp
        hex_string_to_hash = string_to_hash.encode('utf-8').hex()

        # Applying the double sha-256 hash
        first_hash_hex = self.compute_sha256_hash(hex_string_to_hash)
        second_hash_hex = self.compute_sha256_hash(first_hash_hex)

        return second_hash_hex

if __name__ == '__main__':
    from datetime import datetime
    from keys import Keys

    # # Testing a KeyTransaction
    # timestamp = int(datetime.now().timestamp())
    # ca_key = Keys.read_raw_key_from_file('./public_key_ca')
    # ca_key = str(ca_key.encode('utf-8').hex())
    # bn_key = Keys.read_raw_key_from_file('./public_key_bn')
    # bn_key = str(bn_key.encode('utf-8').hex())
    # key_transaction = KeyTransaction(ca_key, bn_key, timestamp)
    # print(key_transaction.transaction_hash)

    # Testing a VoteTransaction
    