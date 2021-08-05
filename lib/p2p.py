from typing import List
from dataclasses import dataclass
from dataclasses import field
from lib.utxoset import UTXO
from lib.block import Block
from lib.exceptions import UnsuccessfulPatch
from urllib.parse import urlparse
import requests
import jsonpickle
import logging
import json
import yaml
import os

logger = logging.getLogger(__name__)


@dataclass
class Peer:
    uri: str

    def get(self, api_endpoint: str, **kwargs):
        params = {k: str(v) for k, v in kwargs.items()}
        r = requests.get(self.uri + '/api' + api_endpoint, params=params)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error('Error: ' + str(e))
            return None
        logger.info(f'{api_endpoint} {kwargs} {r.text}')
        return jsonpickle.decode(r.text)

    def patch(self, api_endpoint: str, **kwargs):
        r = requests.patch(self.uri + '/api' + api_endpoint,
                           data=jsonpickle.dumps(kwargs))

        if r.status_code == 420:
            raise UnsuccessfulPatch()

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error('Error: ' + str(e))


class P2P:
    peers: List[Peer]

    def __init__(self):
        self.peers = list()
        raw_peers = os.environ.get('PEERS')
        if raw_peers is not None:
            for peer in raw_peers.split(' '):
                self.peers.append(Peer(peer))

    def get_peers(self) -> List[Peer]:
        self.sort()
        return self.peers

    def query(self, api_endpoint: str, **kwargs):
        self.sort()
        logger.info(f'Querying peer {self.peers[0]}')
        return self.peers[0].get(api_endpoint, **kwargs)

    def broadcast(self, api_endpoint: str, **kwargs):
        for peer in self.peers:
            peer.patch(api_endpoint, **kwargs)

    def sort(self):
        self.peers.sort(key=lambda peer: peer.get('/difficulty')['difficulty'],
                        reverse=True)
