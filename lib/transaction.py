from typing import List
from dataclasses import dataclass
from lib.utils import hash_sha256
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
"""
TODO:
    * genesis transaction
    * coinbase transactions
    * txin signature
    * transaction id
"""


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


def build_transaction(user_utxos: List['UTXO'], amount: int, tx_fee: int,
                      address: str, private_key: str) -> Transaction:
    txouts: List[TxOut] = [TxOut(address, amount)]
    signingkey = SigningKey(private_key.encode('utf-8'), HexEncoder)
    tx_id = hash_sha256([(utxo.tx_id, utxo.txout_index)
                         for utxo in user_utxos] +
                        [(txout.address, txout.amount) for txout in txouts])
    signature: str = signingkey.sign(tx_id.encode('utf-8'), HexEncoder)
    txins: List[TxIn] = [(utxo.tx_id, utxo.txout_index, signature)
                         for utxo in user_utxos]
    tx = Transaction(tx_id, txins, txouts)
    return tx


genesis_transaction = Transaction(
    'd9930a7f780de3cea556a0a56b10f010e8350c83cab5574c7ec1fe7db3f4c6af', [], [
        TxOut(
            'f958c48a98c63dba40281f7cf446afb9802d74ec276d06cf62ff6ac92fd3921c',
            50)
    ])
