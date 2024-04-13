from .block import Block
from .exceptions.block_exception import BlockException

class BlockChain():
    def __init__(self) -> None:
        self.blocks = []
    
    def __str__(self):
        return f"{self.blocks}"

    # Adds a new the block to the chain
    def add_block(self, block: Block):
        if block.block_header.previous_block_hash == None: # Genesis Block
            self.blocks.append(block)
        else: # Non-Genesis Block
            last_block = self.blocks[-1]

            if last_block.block_header.current_block_hash == block.block_header.previous_block_hash:
                self.blocks.append(block)
            else:
                raise BlockException("The new block doesn't include the correct previous block hash")
    
    # Gets the hash for the last block in the chain
    def get_last_block_hash(self):

        # No blocks in the chain
        if len(self.blocks) == 0:
            return None

        last_block = self.blocks[-1]
        last_block_header = last_block.block_header
        last_block_header_hash = last_block_header.current_block_hash

        return last_block_header_hash

