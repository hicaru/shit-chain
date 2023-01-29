import hashlib
import json
import time
from transaction import Transaction


class Block:

    @property
    def json(self):
        def tx_to_str(tx: Transaction):
            return {
                "amount": str(tx.amount),
                "block_number": tx.block_number,
                "hash": str(tx.hash),
                "public_key": tx.public_key.to_string().hex(),
                "recipient_address": str(tx.recipient_address),
                "sender_address": str(tx.sender_address),
                "signature": tx.signature.hex()
            }

        return json.dumps({
            "block_number": self.block_number,
            "previous_hash": self.previous_hash,
            "transactions": [tx_to_str(tx) for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }).encode()

    def __init__(self, block_number: int, previous_hash: str, transactions: list[Transaction] = []):
        self.block_number: int = block_number
        self.previous_hash: str = previous_hash
        self.transactions: list[Transaction] = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def appen_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        return transaction

    def calculate_hash(self):
        sha = hashlib.sha256()

        sha.update(self.previous_hash.encode('utf-8'))
        sha.update(str(self.block_number).encode('utf-8'))
        sha.update(str(self.timestamp).encode('utf-8'))
        sha.update(str(self.nonce).encode('utf-8'))

        for tx in self.transactions:
            tx.assign_block(self.block_number)
            sha.update(str(tx.hash).encode('utf-8'))

        return sha.hexdigest()
