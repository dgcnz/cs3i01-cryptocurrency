from typing import List
from lib.transaction import Transaction

TX_PER_BLOCK = 1


class TxPool:
    txpool: List[Transaction]

    def add(self, tx: Transaction):
        """ Add transaction tx to transaction pool. """
        self.txpool.append(tx)

    def pop_chunk(self) -> List[Transaction]:
        """ Take a chunk of transactions and remove it from the transaction pool. """
        if len(self.txpool) < TX_PER_BLOCK:
            return []

        chunk = self.txpool[:TX_PER_BLOCK]
        self.txpool = self.txpool[TX_PER_BLOCK:]
        return chunk

    def all(self) -> List[Transaction]:
        """ Return all transactions in pool. """
        return self.txpool
