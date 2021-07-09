from typing import List
from dataclasses import dataclass
from lib.utils import hash_sha256
"""
TODO:
    * genesis transaction
    * coinbase transactions
    * txin signature
    * transaction id
"""

GENESIS_COINS = 50
genesis_transaction = Transaction('', [], [TxOut('', GENESIS_COINS)])


@dataclass
class TxIn:
    tx_id: str
    txout_index: int
    signature: str


@dataclass
class TxOut:
    address: str
    amount: int


@dataclass
class Transaction:
    id: str
    txins: List[TxIn]
    txouts: List[TxOut]

    def valid(self) -> bool:
        pass


def get_transaction_id(txins: List[TxIn], txouts: List[TxOut]) -> str:
    txins_content = [(txin.tx_id, txin.txout_index) for txin in txins]
    txouts_content = [(txout.address, txout.amount) for txout in txouts]
    return hash_sha256([txins_content] + [txouts_content])
