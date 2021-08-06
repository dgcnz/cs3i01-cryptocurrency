from lib.transaction import build_transaction
from lib.block import build_block
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from lib.wallet import Wallet
from lib.exceptions import KeysExist
from lib.utils import current_timestamp

GENESIS_COINS = 50

wallet = Wallet()

try:
    path = wallet.create_keys('genesis')
except KeysExist:
    pass

pub, prv = wallet.keys('genesis')
tx = build_transaction([], GENESIS_COINS, 0, pub, prv)
print(tx)

b = build_block(0, '', current_timestamp(), [tx], 0)
print(b)
