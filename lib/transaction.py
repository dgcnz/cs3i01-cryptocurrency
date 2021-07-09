from typing import List
from dataclasses import dataclass

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
    pass


@dataclass
class UTXO:
    tx_id: str
    txout_index: int
    address: str
    amount: int


class UTXOSet:
    utxoset: List[UTXO] = []  # genesis transaction?

    def add(self, transaction: Transaction):
        # Removing transactions outputs referred by inputs (spent)
        filter(
            lambda utxo: not any(txin.tx_id == utxo.tx_id and txin.txout_index
                                 == utxo.txout_index
                                 for txin in transaction.txins), self.utxoset)

        # Adding new unspent transaction outputs
        self.utxoset.extend([
            UTXO(transaction.id, txout_index, txOut.address, txOut.amount)
            for txout_index, txOut in enumerate(transaction.txouts)
        ])


