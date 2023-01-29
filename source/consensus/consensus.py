from block import Block


def pow(block: Block, difficulty: int) -> Block:
  while True:
        # Create the new block's hash
        block.hash = block.calculate_hash()
        # Check if the hash meets the difficulty level
        if block.hash[:difficulty] == "0" * difficulty:
            return block
        block.nonce += 1
