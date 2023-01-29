from blockchain import Blockchain

class Peer:
    def __init__(self, host: str, port: int, bootstrap: list[str]):
        self.host = host
        self.port = port
        self.blockchain = Blockchain()

        for host in bootstrap:
            self.blockchain.network.addPear(host)

    def start(self):
        # Function to start the P2P server
        pass

    def handle_client(self, client):
        # Function to handle incoming connections
        pass
    
    def receive_block(self, block_data):
        # Function to receive a new block from a peer
        pass
    
    def validate_block(self, block_data):
        # Function to validate a received block
        pass
