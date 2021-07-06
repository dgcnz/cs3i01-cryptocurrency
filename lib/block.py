from typing import List
from lib.transaction import Transaction


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
