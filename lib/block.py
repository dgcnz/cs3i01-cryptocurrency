from typing import List
from lib.transaction import Transaction
from nacl.hash import sha256
from nacl.encoding import HexEncoder


class Block:
    index: int
    bhash: str
    prev_bhash: str
    timestamp: int
    data: List[Transaction]
    difficulty: int
    nonce: int

    def __init__(self, index: int, bhash: str, prev_bhash: str, timestamp: int,
                 data: List[Transaction], difficulty: int, nonce: int):
        self.index = index
        self.bhash = bhash
        self.prev_bhash = prev_bhash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty

    def __bytes__(self):
        return bytes(index) + bytes(bhash, 'utf-8') + bytes(timestamp) + bytes(
            data) + bytes(difficulty) + bytes(nonce)

    def __hash__(self):
        sha256(self.__bytes__())


def compute_block(index: int, prev_bhash: str, timestamp: int,
                  data: List[Transaction], difficulty: int):
    nonce = 0
