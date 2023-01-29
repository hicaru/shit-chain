import logging
import random
from block import Block
from ledger import Ledger
from transaction import Transaction
from account import Account
from consensus import consensus
from network import network


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.transactions: list[Transaction] = []
        self.ledger = Ledger()
        self.difficulty = 4  # The number of leading zeroes in the hash
        self.network = network.Network()

    def create_genesis_block(self):
        return Block(0, bytearray(32).hex())

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        logging.info(
            'Send: %i, recipient: %s, sender: %s, pool: %i',
            transaction.amount,
            transaction.recipient_address,
            transaction.sender_address,
            len(self.transactions)
        )

    def mine(self):
        block = Block(len(self.chain), self.chain[-1].hash, self.transactions)
        self.chain.append(block)
        self.transactions = []

        for transaction in block.transactions:
            if transaction.verify_transaction():
                sender = transaction.sender_address
                recipient = transaction.recipient_address
                amount = transaction.amount

                self.ledger.update_balance(sender, -amount)
                self.ledger.update_balance(recipient, amount)
            else:
                logging.error(
                    'invalid sig: %s',
                    transaction.sender_address
                )

        block = consensus.pow(block, self.difficulty)

        self.chain.append(block)
        self.network.broadcast_block(block)

        logging.info(
            'block_number: %i, block_hash: %s, nonce: %i, transactions: %i, difficulty: %i',
            block.block_number,
            block.hash,
            block.nonce,
            len(block.transactions),
            self.difficulty
        )


if __name__ == "__main__":
    blockchain = Blockchain()
    account0 = Account()
    account1 = Account()
    account2 = Account()
    account3 = Account()

    blockchain.ledger.update_balance(account0.hex, 1000)
    blockchain.ledger.update_balance(account1.hex, 1000)
    blockchain.ledger.update_balance(account2.hex, 1000)
    blockchain.ledger.update_balance(account3.hex, 1000)

    tx0 = account0.send(
        account1.hex,
        random.uniform(1, blockchain.ledger.get_balance(account0.hex))
    )
    tx1 = account1.send(
        account2.hex,
        random.uniform(1, blockchain.ledger.get_balance(account1.hex) // 2)
    )
    tx2 = account2.send(
        account3.hex,
        random.uniform(1, blockchain.ledger.get_balance(account2.hex) // 2)
    )
    tx3 = account3.send(
        account0.hex,
        random.uniform(1, blockchain.ledger.get_balance(account3.hex) // 2)
    )

    blockchain.add_transaction(tx0)
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    blockchain.add_transaction(tx3)

    blockchain.mine()
