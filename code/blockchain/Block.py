class BlockHeader():
    def __init__(self) -> None:
        self.previous_block_hash = None
        self.current_block_hash = None
        self.nonce = None
        self.timestamp = None
        self.version = None


class Block():
    def __init__(self) -> None:
        self.block_header = None
