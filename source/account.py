import hashlib
import ecdsa
import base58
from transaction import Transaction


class Account:
    def __init__(self):
        sha = hashlib.sha256()

        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

        sha.update(self.public_key.to_string())

        self.hex = sha.hexdigest()
        self.base58 = base58.b58encode(self.hex)

    def send(self, recipient: str, amount: int):
        transaction = Transaction(self.hex, self.public_key, recipient, amount)
        transaction.sign_transaction(self.private_key)

        return transaction

