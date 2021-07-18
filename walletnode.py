from flask import Flask
from flask import render_template
from flask import Blueprint
from lib.p2p import P2P
from lib.utxo import build_transaction
from nacl.signing import SigningKey

app = Flask(__name__)
api = Blueprint('api', __name__, template_folder='templates')
p2p = P2P()


@api.route('/transaction', methods=['POST'])
def transaction():
    """ Broadcast transaction to peers. """
    peers = p2p.get_k_best(len(p2p.peers))
    address = request.args.get('address')
    amount = request.args.get('amount')
    tx_fee = request.args.get('tx_fee')
    private_key = request.args.get('private_key')

    my_balance = peers[0].balance(address)
    if my_balance <= amount + tx_fee:
        abort(404, description='Not enough funds.')

    my_utxo = peers[0].get_utxo_sum(address, amount + tx_fee)
    assert len(my_utxo) != 0

    tx = build_transaction(my_utxo, amount, tx_fee, address, private_key)
    for peer in peers:
        peer.send_transaction(tx)


@api.route('/generate-key', methods=['POST'])
def generate_key():
    """ Generate private signing key. """
    key = SigningKey.generate()
    # TODO: save on /.keys/ idk
    # TODO: v2. passphrase encryption
    return key.encode()


@api.route('/balance', methods=['GET'])
def balance():
    """ Ask peers for balance. """
    peer = p2p.get_k_best(1)[0]
    address = request.args.get('address')
    return peer.balance(address)
