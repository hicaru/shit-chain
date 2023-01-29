import hashlib
import ecdsa


class Transaction:
    def __init__(self, sender_address, sender_public_key, recipient_address, amount):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.signature = None
        self.block_number = None
        self.hash = None
        self.public_key = sender_public_key

    def assign_block(self, block_number: int):
        sha = hashlib.sha256()
        self.block_number = block_number

        sha.update(str(self.sender_address).encode('utf-8'))
        sha.update(str(self.recipient_address).encode('utf-8'))
        sha.update(str(self.amount).encode('utf-8'))
        sha.update(str(self.signature).encode('utf-8'))
        sha.update(str(self.block_number).encode('utf-8'))
        sha.update(str(self.public_key).encode('utf-8'))

        self.hash = sha.hexdigest()

    def sign_transaction(self, private_key):
        """
        Sign the transaction using the private key of the sender
        """
        transaction_hash = hashlib.sha256(str(self).encode()).hexdigest()
        self.signature = private_key.sign(transaction_hash.encode())
        self.public_key = private_key.get_verifying_key()

        return self.signature

    def verify_transaction(self):
        """
        Verify the transaction using the public key of the sender
        """
        transaction_hash = hashlib.sha256(str(self).encode()).hexdigest()
        try:
            self.public_key.verify(self.signature, transaction_hash.encode())
            return True
        except ecdsa.keys.BadSignatureError:
            return False
