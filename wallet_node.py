from flask import Flask
from flask import render_template
from flask import Blueprint
from lib.p2p import P2P
from nacl.signing import SigningKey

app = Flask(__name__)
api = Blueprint('api', __name__, template_folder='templates')
p2p = P2P()


@api.route('/transaction', methods=['POST'])
def transaction():
    """ Broadcast transaction to peers. """
    peers = p2p.peers
    address = request.args.get('address')
    amount = request.args.get('amount')
    for peer in peers:
        peer.transaction(address, amount)


@api.route('/generate-key', methods=['POST'])
def generate_key():
    """ Generate private signing key. """
    key = SigningKey.generate()
    return key.encode()


@api.route('/balance', methods=['GET'])
def balance():
    """ Ask peers for balance. """
    peer = p2p.get_k_best(1)[0]
    address = request.args.get('address')
    return peer.balance(address)
