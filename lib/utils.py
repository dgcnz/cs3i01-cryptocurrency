from nacl.hash import sha256
from nacl.encoding import HexEncoder
import pickle
from typing import List
import time
from typing import Any


def hex_to_bin(hexstring: str) -> str:
    hsize = len(hexstring) * 4
    return (bin(int(hexstring, 16))[2:]).zfill(hsize)


def hash_sha256(args: List[Any]) -> str:
    return sha256(pickle.dumps(args), HexEncoder).decode()


def current_timestamp():
    return int(time.time())
