from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from lib.blockchain import Blockchain
from lib.constants import SUCCESSFUL_PATCH
from lib.constants import UNSUCCESSFUL_PATCH
from lib.exceptions import NotEnoughTransactions
from lib.exceptions import UnsuccessfulPatch
from lib.p2p import P2P
from lib.transaction import build_transaction
from lib.txpool import TxPool
from lib.wallet import Wallet
from pathlib import Path
import jsonpickle
import logging
import os
import yaml

app = Flask(__name__)
api = Blueprint("api", __name__, template_folder="templates", url_prefix="/api")

logger = logging.getLogger(__name__)
MINER_KEYNAME: str
COINBASE_AMOUNT: int = 10

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    MINER_KEYNAME = config["miner_keyname"]

blockchain: Blockchain = Blockchain()
txpool: TxPool = TxPool()
wallet = Wallet()
p2p = P2P()


@api.route("/latest-block", methods=["GET"])
def latest_block():
    payload = jsonpickle.encode({"block": blockchain.latest()})
    return payload, 200, {"Content-Type": "application/json"}


@api.route("/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    payload = jsonpickle.encode({"balance": blockchain.balance(address)})
    return payload, 200, {"Content-Type": "application/json"}


@api.route("/difficulty", methods=["GET"])
def get_difficulty():
    payload = jsonpickle.encode({"difficulty": blockchain.difficulty()})
    return payload, 200, {"Content-Type": "application/json"}


@api.route("/blockchain", methods=["GET", "PATCH"])
def get_blockchain():
    if request.method == "GET":
        payload = jsonpickle.encode({"blockchain": blockchain.blocks()})
        return payload, 200, {"Content-Type": "application/json"}
    elif request.method == "PATCH":
        new_blockchain = Blockchain()
        new_blockchain.blockchain = jsonpickle.decode(request.get_data())["blockchain"]
        try:
            blockchain.replace(new_blockchain)
            return SUCCESSFUL_PATCH
        except (InvalidBlockchain, WorseBlockchain):
            return UNSUCCESSFUL_PATCH


@api.route("/find-utxos", methods=["GET"])
def find_utxo():
    address = request.args.get("address")
    amount = int(request.args.get("amount"))
    utxos = blockchain.utxoset.find_utxos(address, amount)
    payload = jsonpickle.encode({"utxos": utxos})
    return payload, 200, {"Content-Type": "application/json"}


@api.route("/transaction-pool", methods=["GET", "PATCH"])
def transaction_pool():
    if request.method == "GET":
        payload = jsonpickle.encode({"txpool": txpool.all()})
        return payload, 200, {"Content-Type": "application/json"}
    elif request.method == "PATCH":
        tx = jsonpickle.decode(request.get_data())["transaction"]
        # TODO: validation
        txpool.add(tx)
        return SUCCESSFUL_PATCH


@api.route("/mine", methods=["POST"])
def mine():
    pkplus, pkminus = wallet.keys(MINER_KEYNAME)
    txchunk = [build_transaction([], [(pkplus, COINBASE_AMOUNT)], pkminus)]

    try:
        txchunk += txpool.pop_chunk()
    except NotEnoughTransactions as e:
        payload = jsonpickle.encode({"message": e.msg})
        return payload, 420, {"Content-Type": "application/json"}

    block = blockchain.create_block(txchunk)
    try:
        # TODO: check validity before broadcast?
        peers = p2p.broadcast("/blockchain", blockchain=blockchain.blocks() + [block])
        blockchain.add_block(block)
        return SUCCESSFUL_PATCH
    except UnsuccessfulPatch:
        payload = jsonpickle.encode(
            {"message": "Mined block wasn't accepted by the network."}
        )
        return payload, 420, {"Content-Type": "application/json"}


app.register_blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
