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
    'e79aa8c007b3b7d83d731e288adaba91156fba44e1ce3c95e8976abac7e875ea', [], [
        TxOut(
            'd92b1fa5cd87f44f4d7de989b455e9047a1d987eebe8d1248384338f4a756962',
            50)
    ])
