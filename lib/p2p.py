from typing import List
from dataclasses import dataclass
from lib.utxoset import UTXO
import requests


@dataclass
class Peer:
    hostname: str
    port: int

    def address(self) -> str:
        return f'{self.hostname}:{self.port}'

    def difficulty(self) -> int:
        """ Get cummulative difficulty of peer's blockchain. """
        r = requests.get(self.address() + '/difficulty')
        if r.status_code == requests.codes.ok:
            return int(r.text)
        return 0

    def transaction(self, address: str, amount: int):
        """ Send transaction to peer. """
        pass

    def balance(self, address: str) -> float:
        """ Get address' balance from peer. """
        pass

    def utxo_sum(self, address: str, amount: float) -> List[UTXO]:
        """ Get list of unspent transactions from address with accumulated value greater or equal than amount from peer. """
        pass


class P2P:
    peers: List[Peer] = []

    def __init__(self):
        # query iptables
        pass

    def get_k_best(self, k: int) -> List[Peer]:
        """ Get k best peers """
        self.peers.sort(key=lambda peer: peer.difficulty(), reverse=True)
        return self.peers[:k]
