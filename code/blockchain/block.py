from datetime import datetime
from hashlib import sha256
import re
from merkly.mtree import MerkleTree
from transaction import Transaction
from exceptions.transaction_exception import TransactionException

class BlockHeader():
    def __init__(self, version, previous_block_hash, bits) -> None:
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.bits = bits
        self.timestamp = self.initialize_timestamp()
        self.merkle_root = None
        self.nonce = 0
        self.current_block_hash = None 
    
    # Initializes the timestamp for the block
    # returns a float  
    def initialize_timestamp(self):
        return int(datetime.now().timestamp())

    # Increments the nonce value to compute a new hash value
    def increment_nonce(self):
        self.nonce += 1
    
    # Computes the block header hash
    def compute_hash(self):
        def compute_sha256_hash(hex_string):
            input_bytes_string = bytes.fromhex(hex_string)
            hash_object = sha256(input_bytes_string)
            hex_digest = hash_object.hexdigest()

            return hex_digest
        
        # Converting values to hex
        version_hex = hex(self.version)[2:]
        merkle_root_hex = self.merkle_root
        timestamp_hex = hex(self.timestamp)[2:]
        bits_hex = hex(self.bits)[2:]
        nonce_hex = hex(self.nonce)[2:]

        # Checking if the previous block hash is the genesis block
        if self.previous_block_hash == None:
            previous_block_hash_hex = hex(0)[2:]
        else:
            previous_block_hash_hex = hex(self.previous_block_hash)[2:]

        # Concattenating values into one input one hex value
        # version || PrevHash || MerkleRoot || Timestamp || Bits || Nonce
        block_header_hex = (version_hex + previous_block_hash_hex + merkle_root_hex + timestamp_hex
                                + bits_hex + nonce_hex)
        
        # Formatting the string to get encoded
        if len(block_header_hex) % 2 != 0:
            block_header_hex += '0'

        # Applying double SHA-256 Hash
        first_hash_hex = compute_sha256_hash(block_header_hex)
        second_hash_hex = compute_sha256_hash(first_hash_hex)
        
        return second_hash_hex

    # Sets the merkle_root for the Block
    def set_merkle_root(self, new_merkle_root):
        self.merkle_root = new_merkle_root
    
    # Sets the block hash value for the Block
    def set_block_hash(self, new_block_hash):
        self.current_block_hash = new_block_hash
    

class Block():
    def __init__(self, magic_number, version, previous_block_hash, bits) -> None:
        self.magic_number = magic_number
        self.block_header = BlockHeader(version, previous_block_hash, bits)
        self.transaction_counter = 0
        self.transaction_limit = 16
        self.transactions = []
    
    def __str__(self):
        return f"{self.transactions=}"
    
    # Mines for a valid block that can be added to the blockchain
    # aka it computes block header hash values until a valid one is found
    def mine_block(self):
        def valid_block_header_hash():
            hash_value = self.block_header.compute_hash()

            # Counting the number of leading zeros the hash_value has
            match_leading_zeros = re.match(r"^0*", hash_value)
            num_zeros = len(match_leading_zeros.group(0))

            if num_zeros >= self.block_header.bits:
                self.block_header.set_block_hash(hash_value)

                return True
            return False
        
        # Setting the merkle root of the Block
        if self.transaction_counter == 0:
            raise TransactionException("A Block requires at least one transaction before it can be mined.")
        
        transaction_hashes = []
        for transaction in self.transactions:
            transaction_hashes.append(transaction.compute_hash())
        
        # Setting the merkle root
        if len(transaction_hashes) != 1:
            merkle_tree = MerkleTree(transaction_hashes)
            merkle_tree_root = merkle_tree.root.hex()
            self.block_header.set_merkle_root(merkle_tree_root)
        else:
            self.block_header.set_merkle_root(transaction_hashes[0])

        print("Mining has begun...")
        
        # Mining for a valid block hash
        while not valid_block_header_hash():
            self.block_header.increment_nonce()
        
        print("Valid Block Found")
    
    # Adds a new transaction to the Block
    def add_transaction(self, transaction: Transaction):
        if self.transaction_counter < self.transaction_limit:
            self.transactions.append(transaction)
            self.transaction_counter += 1
        else:
            raise TransactionException("The Block is full! It cannot store more than 16 transaction.")
