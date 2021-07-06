from typing import List

class Transaction:
    id: str
    txIns: List[TxIn]
    txOuts: List[txOut]
