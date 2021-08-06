from flask import Blueprint
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from lib.constants import SUCCESSFUL_PATCH
from lib.p2p import P2P
from lib.transaction import build_transaction
from lib.wallet import Wallet
from nacl.signing import SigningKey
from pathlib import Path
import jsonpickle
import logging
import os

app = Flask(__name__)
api = Blueprint("api",
                __name__,
                template_folder="templates",
                url_prefix="/api")
p2p = P2P()
wallet = Wallet()


@api.route("/transaction", methods=["POST"])
def transaction():
    """Broadcast transaction to peers."""
    data = jsonpickle.decode(request.get_data())
    address = data["address"]
    amount = data["amount"]
    keyname = data["keyname"]

    pkplus, pkminus = wallet.keys(keyname)

    my_balance = p2p.query("/balance", address=pkplus)["balance"]
    if my_balance < amount:
        abort(404, description="Not enough funds.")

    my_utxo = p2p.query("/find-utxos", address=pkplus, amount=amount)["utxos"]
    rem = sum(utxo.amount for utxo in my_utxo) - amount
    address_amount = [(address, amount)]

    assert rem >= 0

    if rem > 0:
        address_amount.append((pkplus, rem))

    tx = build_transaction(my_utxo, address_amount, pkminus)
    try:
        p2p.broadcast("/transaction-pool", transaction=tx)
        return SUCCESSFUL_PATCH
    except UnsuccessfulPatch:
        payload = jsonpickle.encode(
            {"message": "Transaction wasn't accepted by the network."})
        return payload, 420, {"ContentType": "application/json"}


@api.route("/keys", methods=["GET", "POST"])
def keys():
    if request.method == "GET":
        data = [{
            "keyname": keyname,
            "address": wallet.pkplus(keyname)
        } for keyname in wallet.keynames()]
        payload = jsonpickle.encode({"keys": data})
        return payload, 200, {"Content-Type": "application/json"}
    elif request.method == "POST":
        data = request.get_data()
        keyname = jsonpickle.decode(data)["keyname"]
        keypath = wallet.create_keys(keyname)
        # TODO: handle duplicated keys
        payload = jsonpickle.encode({"keypath": str(keypath)})
        return payload, 200, {"Content-Type": "application/json"}


@api.route("/balance", methods=["GET"])
def balance():
    """Ask peers for balance."""
    address = request.args.get("address")
    balance = p2p.query("/balance", address=address)["balance"]
    payload = jsonpickle.encode({"balance": balance})
    return payload, 200, {"Content-Type": "application/json"}


app.register_blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
