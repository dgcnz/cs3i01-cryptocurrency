# toficoin

## Wallet Node

### API
---
* **Endpoint**: `POST /api/transaction`
* **Description**: Build and broadcast transaction.
* **Args**:
    * `address`: public key of recipient, formatted as hexstring.
    * `amount`: amount of money to transfer to address.
    * `keyname`: Key_name from where to collect funds.

---

* **Endpoint**: `POST /api/keys`
* **Description**: Generate key pair and store in `/.tfc/`
* **Args**:
    * `keyname`: Unique name of keypair. Used for local storage.

---

* **Endpoint**: `GET /api/balance`
* **Description**: Ask peers for the balance of an address.
* **Args**:
    * `address`: public key of subject, formatted as hexstring.

---


## Miner Node

---

* **Endpoint**: `GET /api/latest-block`
* **Description**: Get latest block of node's blockchain.

---

* **Endpoint**: `GET /api/balance`
* **Description**: Get balance computed from node's blockchain.
* **Args**:
    * `address`: public key of subject, formatted as hexstring.

---

* **Endpoint**: `GET /api/difficulty`
* **Description**: Get accumulated difficulty from node's blockchain.

---

* **Endpoint**: `GET /api/blockchain`
* **Description**: Get blockchain (block list) of node..

---


## cloud todo:
- monitoring
    - cpu
- logging
- simulation for attack:
    - mining
