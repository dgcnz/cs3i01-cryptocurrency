from flask import Flask
from flask import render_template
from flask import Blueprint
from lib.p2p import P2P
from lib.blockchain import Blockchain
import argparse

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Full node.')
parser.add_argument('key', type=str, help='Signing key.')

args = parser.parse_args()

blockchain: Blockchain = Blockchain()


@app.route('/latest-block', methods=['GET'])
def get_latest_block():
    return blockchain.latest()


@app.route('/balance', methods=['GET'])
def get_balance():
    address = requests.args.get('address')
    return blockchain.balance(address)


@app.route('/difficulty', methods=['GET'])
def get_difficulty():
    return blockchain.difficulty()


@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return blockchain.blocks()


@app.route('/utxo-sum', methods=['GET'])
def get_utxo_sum():
    address = requests.args.get('address')
    amount = requests.args.get('amount')
    return blockchain.utxoset.utxo_sum(address, amount)


