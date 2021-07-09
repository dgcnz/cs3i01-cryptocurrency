from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from lib.p2p import P2P
from lib.blockchain import Blockchain
from lib.txpool import TxPool
from pathlib import Path
import argparse

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Full node.')
parser.add_argument('key_path', type=str, help='Signing key path.')

args = parser.parse_args()
KEY_PATH = Path(args.key_path)

blockchain: Blockchain = Blockchain()
txpool: TxPool = TxPool()


@app.route('/latest-block', methods=['GET'])
def get_latest_block():
    return blockchain.latest()


@app.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    return blockchain.balance(address)


@app.route('/difficulty', methods=['GET'])
def get_difficulty():
    return blockchain.difficulty()


@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return blockchain.blocks()


@app.route('/utxo-sum', methods=['GET'])
def get_utxo_sum():
    address = request.args.get('address')
    amount = request.args.get('amount')
    return blockchain.utxoset.utxo_sum(address, amount)


@app.route('/transaction-pool', methods=['GET', 'PUT'])
def transaction_pool():
    if request.method == 'GET':
        return txpool.all()
    elif request.method == 'PUT':
        # TODO: unpickle
        tx = jsonpickle.decode(request.args.get('transaction'))
        txpool.add(tx)


@app.route('/mine', methods=['POST'])
def mine():
    # TODO: query peers to update txpool
    txchunk = txpool.pop_chunk()
    block = blockchain.create_block(txchunk)
    # TODO: broadcast
    blockchain.add_block(block)
