from hashlib import sha256
from abc import ABC, abstractmethod
from enum import Enum

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

class TransactionType(Enum):
    KEY = 'key'
    VOTE = 'vote'

class VoteTransaction(Transaction):
    def __init__(self, ballot_point, ballot_slope, ballot_signature, timestamp):
        # Encrypted candidiate information for a ballot 
        self.ballot_point = ballot_point # Enc(P || H(lambda), PK_BN)
        self.ballot_slope = ballot_slope # Enc(H(ballot_point), SK_CA)
        self.ballot_signature = ballot_signature # Enc(lambda, PK_CA)

        # Calling super class constructor
        super().__init__(TransactionType.VOTE, timestamp)

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
        super().__init__(TransactionType.KEY, timestamp)

        # Initializing the transaction hash
        self.transaction_hash = self.compute_hash()
    
    def __str__(self):
        return f"{self.central_authority_key=}\n{self.blockchain_network_key=}"
    
     # Computes the hash for a VoteTransaction
    def compute_hash(self):
        # Converting the transaction components into a hexadecimal representation
        ca_key = str(self.central_authority_key.encode('utf-8').hex())
        bn_key = str(self.blockchain_network_key.encode('utf-8').hex())
        timestamp = str(int(self.timestamp, 16))

        # Concatenating the transaction components to compute a hash
        # ballot_point || ballot_slope || ballot_signature || timestamp
        string_to_hash = ca_key + bn_key + timestamp
        hex_string_to_hash = string_to_hash.encode('utf-8').hex()

        # Applying the double sha-256 hash
        first_hash_hex = self.compute_sha256_hash(hex_string_to_hash)
        second_hash_hex = self.compute_sha256_hash(first_hash_hex)

        return second_hash_hex
    