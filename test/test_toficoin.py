from lib.wallet import Wallet
import jsonpickle
import unittest
import requests


class TestStringMethods(unittest.TestCase):
    def test_mining(self):
        BLOCKS = 4
        wallet = Wallet()
        miner_url = 'http://0.0.0.0:8000'
        wallet_url = 'http://0.0.0.0:8050'
        keynames = ['genesis', 'test']
        wallet.create_keys(keynames[1], overwrite=True)

        for i in range(BLOCKS):
            src = keynames[i % 2]
            dst = keynames[(i + 1) % 2]
            data = {
                'address': wallet.pkplus(dst),
                'amount': 20,
                'keyname': src
            }
            r = requests.post(wallet_url + '/api/transaction',
                              data=jsonpickle.encode(data))
            self.assertEqual(r.status_code, 200)
            r = requests.post(miner_url + '/api/mine')
            self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
