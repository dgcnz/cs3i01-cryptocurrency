from typing import List
from dataclasses import dataclass
from lib.block import Block

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

    def matches(self, txin: TxIn) -> bool:
        """ Check if transaction input refers to unspent transaction output. """
        return txin.tx_id == self.tx_id and txin.txout_index == self.txout_index


class UTXOSet:
    utxoset: List[UTXO] = []  # genesis transaction?

    def add(self, transaction: Transaction):
        """ Updates utxoset with new transaction. """
        # Removing transactions outputs referred by inputs (spent)
        filter(
            lambda utxo: not any(
                utxo.matches(txin) for txin in transaction.txins),
            self.utxoset)

        # Adding new unspent transaction outputs
        self.utxoset.extend([
            UTXO(transaction.id, txout_index, txOut.address, txOut.amount)
            for txout_index, txOut in enumerate(transaction.txouts)
        ])

    def get(self, address: str) -> List[UTXO]:
        """ Get addresses unspent transactions. """
        return list(filter(lambda utxo: utxo.address == address, self.utxoset))

    def validate(self, transactions: List[Transaction]) -> bool:
        """ Validate list of transactions. """
        for tx in transactions:
            if not tx.valid() or not all(
                    self.is_txin_unspent(txin) for txin in tx.txins):
                return False
        return True

    def is_txin_unspent(self, txin: TxIn) -> bool:
        """ Check if txin is unspent. """
        return any(utxo.matches(txin) for utxo in self.utxoset)

    def clear(self):
        """ Erases all unspent transactions. """
        # TODO: check for genesis transaction
        self.utxoset.clear()

    def build(self, blockchain: List[Block]):
        """ Build UTXOSet from scratch using blockchain. """
        self.clear()
        for block in blockchain:
            for tx in block.data:
                self.add(tx)
