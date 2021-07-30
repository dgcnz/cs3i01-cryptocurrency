from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from lib.p2p import P2P
from lib.transaction import build_transaction
from nacl.signing import SigningKey
from pathlib import Path
from lib.wallet import Wallet
import logging

app = Flask(__name__)
api = Blueprint('api',
                __name__,
                template_folder='templates',
                url_prefix='/api')
p2p = P2P()
wallet = Wallet()


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


@api.route('/generate-keys', methods=['POST'])
def generate_keys():
    """ Generate private signing key. """
    name = request.args.get('name')
    logging.warning(name)
    keys_path = wallet.create_keys(name)
    return str(keys_path)


@api.route('/balance', methods=['GET'])
def balance():
    """ Ask peers for balance. """
    peer = p2p.get_k_best(1)[0]
    address = request.args.get('address')
    return {'balance': peer.balance(address)}


app.register_blueprint(api)
print(app.url_map)
