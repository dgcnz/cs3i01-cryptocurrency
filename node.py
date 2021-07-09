from flask import Flask, render_template

app = Flask(__name__)


@app.route('/send-transaction', methods=['POST'])
def send_transaction():
    # Receive transaction from another peer
    pass


@app.route('/balance', methods=['GET'])
def balance():
    pass


@app.route('/add-peer', methods=['POST'])
def add_peer():
    # Add address of peer to list of peers
    pass


@app.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', balance=10)
