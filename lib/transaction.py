from typing import List


class TxIn:
    txOutId: str
    txOutIndex: int
    signature: str


class TxOut:
    address: str
    amount: int


class Transaction:
    id: str
    txIns: List[TxIn]
    txOuts: List[TxOut]

    def __bytes__(self):
        pass
