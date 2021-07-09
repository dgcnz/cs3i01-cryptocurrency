from nacl.hash import sha256
from nacl.encoding import HexEncoder
import pickle
from typing import List
from typing import Any


def hex_to_bin(hexstring: str) -> str:
    return bin(int(hexstring, 16))[2:]


def hash_sha256(args: List[Any]) -> str:
    return sha256(pickle.dumps(args), HexEncoder).decode()
