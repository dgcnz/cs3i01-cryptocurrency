from pathlib import Path
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from lib.exceptions import KeysExist
from typing import Tuple
import yaml

TFC_PATH: Path

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)
    TFC_PATH = Path(config['tfc_path']).expanduser()


class Wallet:
    def create_keys(self, name: str) -> Path:
        # TODO passphrase encryption
        pkminus = SigningKey.generate()
        pkplus = pkminus.verify_key
        key_path = TFC_PATH / name
        if key_path.is_file():
            raise KeysExist()

        key_path.write_text(pkminus.encode(encoder=HexEncoder).decode())
        key_path.with_suffix('.pub').write_text(
            pkplus.encode(encoder=HexEncoder).decode())

        return key_path

    def pkplus(self, name) -> str:
        key_path = TFC_PATH / name
        return key_path.read_text()

    def pkminus(self, name) -> str:
        key_path = (TFC_PATH / name).with_suffix('.pub')
        return key_path.read_text()

    def keys(self, name) -> Tuple[str, str]:
        return (self.pkplus(name), self.pkminus(name))
