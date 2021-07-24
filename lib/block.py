from typing import List
from lib.utils import hex_to_bin
from lib.utils import hash_sha256
from lib.transaction import Transaction, genesis_transaction
from dataclasses import dataclass


@dataclass
class Block:
    index: int
    bhash: str
    prev_bhash: str
    timestamp: int
    data: List[Transaction]
    difficulty: int
    nonce: int

    def valid(self, prev: 'Block') -> bool:
        """ Checks block's validity """
        return self.prev_bhash == prev.bhash and validate_hash_difficulty(
            self.bhash, self.difficulty) and hash_block_content(
                self.index, self.prev_bhash, self.timestamp, self.data,
                self.difficulty, self.nonce) == self.bhash


def hash_block_content(index: int, prev_bhash: str, timestamp: int,
                       data: List[Transaction], difficulty: int, nonce: int):
    return hash_sha256([index, prev_bhash, timestamp, data, difficulty, nonce])


def validate_hash_difficulty(bhash: str, difficulty: int) -> bool:
    """ Checks if hash has expected difficulty. """
    return hex_to_bin(bhash).startswith('0' * difficulty)


def build_block(index: int, prev_bhash: str, timestamp: int,
                data: List[Transaction], difficulty: int):
    """ Mines single block. """
    nonce: int = 0
    while True:
        bhash = hash_block_content(index, prev_bhash, timestamp, data,
                                   difficulty, nonce)
        if validate_hash_difficulty(bhash, difficulty):
            return Block(index, bhash, prev_bhash, timestamp, data, difficulty,
                         nonce)
        nonce += 1


def verify_block_hash(block: Block):
    return hash_block_content(block.index, block.prev_bhash, block.timestamp,
                              block.data, block.difficulty,
                              block.nonce) == block.bhash


genesis_block = Block(
    0, 'd55209070f5f82e8df80b8a386c3b02bacd12bd6e44ca9353744c7a046c1ec1a', '',
    1627135592, genesis_transaction, 0, 0)
