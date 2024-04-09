import asyncio
import websockets
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../blockchain')))
from blockchain import BlockChain
from election_server import Election
from transaction import VoteTransaction
from block import Block
from helper import decrypt_rsa
from keys import Keys

# This server simulates 1 Miner
# ip_address = "10.12.143.86"
ip_address = "10.12.159.102"
port = 8765
current_block = None

def process_message(json_object):
    message_type = json_object["message_type"]

    if message_type == 'vote_transaction':
        t1 = json_object["t1"]
        t2 = json_object["t2"]
        t3 = json_object["t3"]
        timestamp = json_object["timestamp"]

        # Creating the Vote Transaction
        new_vote = VoteTransaction(t1, t2, t3, timestamp)

        # Creating a new block
        global current_block
        if current_block == None:
            # Initializing block parameters
            magic_number = 1
            version = 1
            previous_block_hash = block_chain.get_last_block_hash()
            bits = 4

            current_block = Block(magic_number, version, previous_block_hash, bits)

        # Adding the vote transaction to the block
        current_block.add_transaction(new_vote)
        
        # Adding the block to the blockchain
        if current_block.transaction_counter == 2:
            current_block.mine_block()
            block_chain.add_block(current_block)
            current_block = None
        
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

                        pr_key_ca = Keys.read_key_from_pem_file("./code/resources/keys/private_key_CA", "private")
                        pr_key_bn = Keys.read_key_from_pem_file("./code/resources/keys/private_key_BN", "private")

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

async def server(websocket, path):
    async for message in websocket:
        json_object = json.loads(message)
        json_message = json.dumps(json_object, indent=4)
        
        print(f"Received message: {json_message}")
        
        process_message(json_object)

print("Starting Mining Node...")

# Initializing the Election
election = Election()

print("Creating the Genesis Block:")
genesis_block = election.create_genesis_block()

# Initializing the Election Blockchain
block_chain = BlockChain()
block_chain.add_block(genesis_block)

# Main
start_server = websockets.serve(server, ip_address, port)

# This needs to be explored/mpodified
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
