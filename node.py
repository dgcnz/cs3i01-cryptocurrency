from flask import Flask

app = Flask(__name__)


@app.route('/mineblock', methods=['POST'])
def mineblock():
    # TODO
    pass


@app.route('/balance', methods=['GET'])
def balance():
    # compute balance
    pass
