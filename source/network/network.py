from block import Block


class Network:
    def __init__(self):
        self.peers = set()

    def addPear(self, host: str):
        pass

    def broadcast_block(self, block: Block):
        # Function to broadcast a new block to all connected peers
        for peer in self.peers:
            if block.hash:
                try:
                    peer.send(block.json)
                except:
                    self.peers.remove(peer)
