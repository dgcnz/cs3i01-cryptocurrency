from typing import List
from dataclasses import dataclass
from lib.utils import hash_sha256
from lib.utxoset import UTXO
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
"""
TODO:
    * genesis transaction
    * coinbase transactions
    * txin signature
    * transaction id
"""

GENESIS_COINS = 50.0
genesis_transaction = Transaction('', [], [TxOut('', GENESIS_COINS)])


@dataclass
class TxIn:
    tx_id: str
    txout_index: int
    signature: str


@dataclass
class TxOut:
    address: str
    amount: float


@dataclass
class Transaction:
    id: str
    txins: List[TxIn]
    txouts: List[TxOut]

    def valid(self) -> bool:
        pass


def build_transaction(user_utxos: List[UTXO], amount: float, tx_fee: float,
                      address: str, private_key: str) -> Transaction:
    txouts: List[TxOut] = [TxOut(address, amount)]
    signingkey = SigningKey(private_key, HexEncoder)
    tx_id = hash_sha256([(utxo.tx_id, utxo.txout_index)
                         for utxo in user_utxos] +
                        [(txout.address, txout.amount) for txout in txouts])
    signature: str = signingkey.sign(tx_id, HexEncoder)
    txins: List[TxIn] = [(utxo.tx_id, utxo.txout_index, signature)
                         for utxo in user_utxos]
    tx = Transaction(tx_id, txins, txouts)
    return tx
