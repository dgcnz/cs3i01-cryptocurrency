from typing import List
from dataclasses import dataclass
from dataclasses import field
from lib.block import Block
from lib.transaction import Transaction
from lib.transaction import TxIn
from lib.transaction import TxOut


@dataclass
class UTXO:
    tx_id: str
    txout_index: int
    address: str
    amount: int

    def matches(self, txin: TxIn) -> bool:
        """ Check if transaction input refers to unspent transaction output. """
        return txin.tx_id == self.tx_id and txin.txout_index == self.txout_index


@dataclass
class UTXOSet:
    utxoset: List[UTXO] = field(default_factory=list)

    def add(self, transaction: Transaction):
        """ Updates utxoset with new transaction. """
        # Removing transactions outputs referred by inputs (spent)
        self.utxoset = list(
            filter(
                lambda utxo: not any(
                    utxo.matches(txin) for txin in transaction.txins),
                self.utxoset))

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

    def find_utxos(self, address: str, amount: int) -> List[UTXO]:
        """ Get list of unspent transactions from address with accumulated value greater or equal than amount. """

        ans: List[UTXO] = []
        accsum: int = 0
        for utxo in self.utxoset:
            if utxo.address != address:
                continue
            if accsum >= amount:
                break
            accsum += utxo.amount
            ans.append(utxo)
        if accsum < amount:
            return []
        return ans
