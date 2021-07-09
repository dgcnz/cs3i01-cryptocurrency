from lib.block import Block
from lib.block import genesis_block
from lib.block import make_block
from lib.transaction import Transaction
from lib.transaction import TxIn
from lib.transaction import UTXO
from lib.transaction import UTXOSet
from lib.exceptions import InvalidBlock
from lib.exceptions import InvalidTransaction
from lib.exceptions import InvalidBlockchain
from lib.exceptions import WorseBlockchain
from flask import Blueprint
from typing import List
import time

# choose exceptions over booleans, if misses check, program fails


class Blockchain:
    blockchain: List[Block] = [genesis_block]
    utxoset = UTXOSet()

    def create_block(self, transactions: List[Transaction]) -> Block:
        """ Wraps transactions as new block. """
        if any(not tx.valid()
               for tx in transactions) or not self.are_txins_unspent(
                   [txin for tx in transactions for txin in tx.txins]):
            raise InvalidTransaction()

        last: Block = self.blockchain[-1]
        # TODO: could casting time.time lead to some attack?
        timestamp: int = int(time.time())
        # TODO: implement dynamic difficulty
        difficulty: int = 4
        new_block: Block = make_block(last.index + 1, last.bhash, timestamp,
                                      transactions, difficulty)
        return new_block

    def add_block(self, block: Block):
        """ Adds new block to blockchain. """
        if not block.valid() or not self.is_block_consistent(block):
            raise InvalidBlock()

        self.blockchain.append(block)
        for tx in block.data:
            self.utxoset.add(tx)

    def is_block_consistent(self, block: Block) -> bool:
        """ Checks block's consistency with blockchain. """
        pass

    def are_txins_unspent(self, txins: List[TxIn]) -> bool:
        """ Check if transaction's inputs are unspent. """
        for block in self.blockchain:
            for tx in block.data:
                if any(txin in tx.txins for txin in txins):
                    return False
        return True

    def is_chain_valid(self) -> bool:
        """ Checks blockchain's validity. """
        pass

    def cost(self) -> int:
        """ Checks total cost of a blockchain. """
        return sum(map(lambda block: block.difficulty, self.blockchain))

    def replace(self, other: Blockchain):
        """ Replace current blockchain with other one. """
        if not other.is_chain_valid():
            raise InvalidBlockchain()
        if self.cost() >= other.cost():
            raise WorseBlockchain()
        self.blockchain = other.blockchain

    def balance(self, address: str) -> float:
        """ Get balance of address. """
        pass
