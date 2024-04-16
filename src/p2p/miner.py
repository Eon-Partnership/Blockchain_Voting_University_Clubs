import asyncio
import websockets
import json
import netifaces as ni
from ..blockchain.blockchain import BlockChain
from .election_server import Election
from ..blockchain.transaction import VoteTransaction
from ..blockchain.block import Block
from ..blockchain.helper import decrypt_rsa
from ..blockchain.keys import Keys

print("Starting Mining Node...")

# Initializing the Election
election = Election()

print("Creating the Genesis Block:")
genesis_block = election.create_genesis_block()

# Initializing the Election Blockchain
block_chain = BlockChain()
block_chain.add_block(genesis_block)

class Miner():
    def __init__(self, port):
        self.ip_address = self.initializeIPAddress()
        self.port = port
        self.server = websockets.serve(self.message_handler, self.ip_address, self.port)
        self.current_block = None
    
    # Initializes the IP Address for a miner dynamically
    def initializeIPAddress(self):
        # Get the name of the default network interface (e.g., 'en0' on macOS, 'wlan0' on Linux)
        default_interface = ni.gateways()['default'][ni.AF_INET][1]
        
        # Retrieve IP address associated with the default network interface
        ip_address = ni.ifaddresses(default_interface)[ni.AF_INET][0]['addr']

        return ip_address
    
    # Handles incoming websocket messages
    async def message_handler(self, websocket, path):
        async for message in websocket:
            json_object = json.loads(message)
            json_message = json.dumps(json_object, indent=4)
            
            print(f"Received message: {json_message}")
            
            self.process_message(json_object)
    
    # TODO: Implement functionality for verifying incoming transactions
    def verify_transaction(self, transaction):
        pass
    
    # TODO: Implement functionality for verifying incoming blocks
    def verify_block(self, block):
        pass

    # TODO: Implement functionality for broadcasting a message (transaction/block)
    def broadcast_message(self, message):
        pass

    # Handler for processing incoming messages from other Miners, VoteMachines, CentralAuthority and BlockchainNetwork
    def process_message(self, json_object):
        message_type = json_object["message_type"]

        if message_type == 'vote_transaction':
            t1 = json_object["t1"]
            t2 = json_object["t2"]
            t3 = json_object["t3"]
            timestamp = json_object["timestamp"]

            # Creating the Vote Transaction
            new_vote = VoteTransaction(t1, t2, t3, timestamp)

            # Creating a new block
            if self.current_block == None:
                # Initializing block parameters
                magic_number = 1
                version = 1
                previous_block_hash = block_chain.get_last_block_hash()
                bits = 4

                self.current_block = Block(magic_number, version, previous_block_hash, bits)

            # Adding the vote transaction to the block
            self.current_block.add_transaction(new_vote)
            
            # Adding the block to the blockchain
            if self.current_block.transaction_counter == 2:
                self.current_block.mine_block()
                block_chain.add_block(self.current_block)
                self.current_block = None
            
        elif message_type == 'election_results':
            vote_counts = {"Myron": 0, "Daniel": 0, "Eric": 0, "Kirisan": 0}
        
            print("Block Chain: ", block_chain)
            
            # Start counting votes
            if len(block_chain.blocks) != 1:
                
                # Iterating over blocks in blockchain
                for block in block_chain.blocks:
                    if block.block_header.previous_block_hash != None: # Skipping over genesis block
                        
                        # Iterating over transaction in a block
                        for transaction in block.transactions:
                            original_t1 = bytes.fromhex(transaction.ballot_point)
                            original_t2 = int(transaction.ballot_slope, 16)
                            original_t3 = bytes.fromhex(transaction.ballot_signature)

                            pr_key_ca = Keys.read_key_from_pem_file("./src/resources/keys/private_key_CA", "private")
                            pr_key_bn = Keys.read_key_from_pem_file("./src/resources/keys/private_key_BN", "private")

                            raw_t1 = decrypt_rsa(original_t1, pr_key_bn)
                            raw_t3 = decrypt_rsa(original_t3, pr_key_ca)

                            retrived_x_val = int(raw_t1[0:32], 16)
                            retrived_y_val = int(raw_t1[33:64], 16)

                            retrived_lambda_val = int(raw_t3)

                            N = retrived_y_val - retrived_lambda_val * retrived_x_val
                            binary_N = bin(N)[2:]
                            candidate_id = int(binary_N[:-16], 2)

                            if candidate_id == 1:
                                vote_counts['Myron'] += 1
                            elif candidate_id == 2:
                                vote_counts['Daniel'] += 1
                            elif candidate_id == 3:
                                vote_counts['Eric'] += 1
                            elif candidate_id == 4:
                                vote_counts['Kirisan'] += 1
                            
            print("The result of the election so far is as follows:\n", vote_counts)

if __name__ == "__main__":
    port = 8765
    miner = Miner(port)
    asyncio.get_event_loop().run_until_complete(miner.server)
    asyncio.get_event_loop().run_forever()
