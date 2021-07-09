from lib.block import Block
from lib.block import genesis_block
from lib.block import build_block
from lib.utxoset import UTXO
from lib.utxoset import UTXOSet
from lib.transaction import Transaction
from lib.transaction import TxIn
from lib.exceptions import InvalidBlock
from lib.exceptions import InvalidTransaction
from lib.exceptions import InvalidBlockchain
from lib.exceptions import WorseBlockchain
from flask import Blueprint
from typing import List
import time
"""
TODO:
    * dynamic difficulty
    * type checking
TOREAD:
    * int casting unix time security consequences
"""


class Blockchain:
    blockchain: List[Block] = [genesis_block]
    utxoset = UTXOSet()

    def create_block(self, transactions: List[Transaction]) -> Block:
        """ Wraps transactions as new block. """
        if self.utxoset.validate(transactions):
            raise InvalidTransaction()

        last: Block = self.blockchain[-1]
        timestamp: int = int(time.time())
        difficulty: int = 4
        new_block: Block = build_block(last.index + 1, last.bhash, timestamp,
                                       transactions, difficulty)
        return new_block

    def add_block(self, block: Block):
        """ Adds new block to blockchain. """
        if not block.valid(self.blockchain[-1]):
            raise InvalidBlock()

        self.blockchain.append(block)
        for tx in block.data:
            self.utxoset.add(tx)

    def latest(self) -> Block:
        """ Get latest blockhain block. """
        return self.blockchain[-1]

    def blocks(self) -> List[Block]:
        """ Get all blockchain blocks. """
        return self.blockchain

    def is_chain_valid(self) -> bool:
        """ Checks blockchain's validity. """
        pass

    def difficulty(self) -> int:
        """ Checks total difficulty of a blockchain. """
        return sum(map(lambda block: block.difficulty, self.blockchain))

    def replace(self, other: Blockchain):
        """ Replace current blockchain with other one. """
        if not other.is_chain_valid():
            raise InvalidBlockchain()
        if self.difficulty() >= other.difficulty():
            raise WorseBlockchain()
        self.blockchain = other.blockchain
        self.utxoset.build(other.blockchain)

    def balance(self, address: str) -> float:
        """ Get balance of address. """
        return sum(utxo.amount for utxo in self.utxoset.get(address))
