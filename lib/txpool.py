from typing import List
from lib.transaction import Transaction
from lib.exceptions import NotEnoughTransactions
from dataclasses import dataclass
from dataclasses import field

TX_PER_BLOCK = 1


@dataclass
class TxPool:
    txpool: List[Transaction] = field(default_factory=list)

    def add(self, tx: Transaction):
        """ Add transaction tx to transaction pool. """
        self.txpool.append(tx)

    def pop_chunk(self) -> List[Transaction]:
        """ Take a chunk of transactions and remove it from the transaction pool. """
        if len(self.txpool) < TX_PER_BLOCK:
            raise NotEnoughTransactions()

        chunk = self.txpool[:TX_PER_BLOCK]
        self.txpool = self.txpool[TX_PER_BLOCK:]
        return chunk

    def __len__(self):
        return len(self.txpool)

    def all(self) -> List[Transaction]:
        """ Return all transactions in pool. """
        return self.txpool
