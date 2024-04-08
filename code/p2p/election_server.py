from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../blockchain')))

from block import Block
from keys import Keys
from transaction import KeyTransaction

# Election class is used to initialize and terminate an election
class Election():
    def create_genesis_block(self):
        # Initializing block parameters
        magic_number = 1
        version = 1
        previous_block_hash = None
        bits = 5

        # Creating the genesis block
        new_block = Block(magic_number, version, previous_block_hash, bits)

        # Creating the KeyTransactions
        timestamp = int(datetime.now().timestamp())
        ca_key = Keys.read_raw_key_from_file('./code/resources/keys/public_key_CA')
        bn_key = Keys.read_raw_key_from_file('./code/resources/keys/public_key_BN')
        key_transaction = KeyTransaction(ca_key, bn_key, timestamp)
        
        # Adding the transaction to the block
        new_block.add_transaction(key_transaction)

        # Mining for the block
        new_block.mine_block()

        return new_block

    def create_final_block(self):
        pass

new_election = Election()
genesis_block = new_election.create_genesis_block()
print(genesis_block)
