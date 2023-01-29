class Ledger:
    def __init__(self):
        self.balances = {}

    def update_balance(self, address: str, amount: int):
        if address in self.balances:
            self.balances[address] += amount
        else:
            self.balances[address] = amount

    def get_balance(self, address: str) -> int:
        if address in self.balances:
            return self.balances[address]
        else:
            return 0
