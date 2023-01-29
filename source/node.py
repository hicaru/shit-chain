from network import peer
from bootstrap import bootstrap_list


PORT = 5622
HOST = '127.0.0.1'

node = peer.Peer(HOST, PORT, bootstrap_list)

print(node)
