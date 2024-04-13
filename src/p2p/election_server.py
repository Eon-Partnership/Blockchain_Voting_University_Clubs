from datetime import datetime
from ..blockchain.block import Block
from ..blockchain.keys import Keys
from ..blockchain.transaction import KeyTransaction

# Election class is used to initialize and terminate an election
class Election():
    def create_genesis_block(self):
        # Initializing block parameters
        magic_number = 1
        version = 1
        previous_block_hash = None
        bits = 4

        # Creating the genesis block
        new_block = Block(magic_number, version, previous_block_hash, bits)

        # Creating the KeyTransactions
        timestamp = int(datetime.now().timestamp())
        ca_key = Keys.read_raw_key_from_file('./src/resources/keys/public_key_CA')
        bn_key = Keys.read_raw_key_from_file('./src/resources/keys/public_key_BN')
        key_transaction = KeyTransaction(ca_key, bn_key, timestamp)
        
        # Adding the transaction to the block
        new_block.add_transaction(key_transaction)

        # Mining for the block
        new_block.mine_block()

        return new_block

    def create_final_block(self):
        pass
    