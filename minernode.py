from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from lib.p2p import P2P
from lib.blockchain import Blockchain
from lib.txpool import TxPool
from pathlib import Path
import yaml
import jsonpickle

app = Flask(__name__)
api = Blueprint('api',
                __name__,
                template_folder='templates',
                url_prefix='/api')

MINER_KEYNAME: str
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)
    MINER_KEYNAME = config['miner_keyname']

blockchain: Blockchain = Blockchain()
txpool: TxPool = TxPool()


@api.route('/latest-block', methods=['GET'])
def get_latest_block():
    block = blockchain.latest()
    return jsonpickle.encode(block)


@api.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    return {'balance': blockchain.balance(address)}


@api.route('/difficulty', methods=['GET'])
def get_difficulty():
    return {'difficulty': blockchain.difficulty()}


@api.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonpickle.encode(blockchain.blocks())


@api.route('/utxo-sum', methods=['GET'])
def get_utxo_sum():
    address = request.args.get('address')
    amount = request.args.get('amount')
    return jsonpickle.encode(blockchain.utxoset.utxo_sum(address, amount))


@api.route('/transaction-pool', methods=['GET', 'PUT'])
def transaction_pool():
    if request.method == 'GET':
        return jsonpickle.encode(txpool.all())
    elif request.method == 'PUT':
        tx = jsonpickle.decode(request.args.get('transaction'))
        txpool.add(tx)


@api.route('/mine', methods=['POST'])
def mine():
    # TODO: query peers to update txpool
    txchunk = txpool.pop_chunk()
    block = blockchain.create_block(txchunk)
    # TODO: broadcast
    blockchain.add_block(block)


app.register_blueprint(api)
print(app.url_map)
