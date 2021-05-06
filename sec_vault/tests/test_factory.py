import os
import pytest

import core.parser
import core.cipherfactory

@pytest.fixture
def create_args():
    return ["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend",  "--record-type", "login", "--create-vault"]

def test_create_vault(create_args):
    p = core.parser.CLIParser()
    args = p.parse_args(create_args)
    c = core.cipherfactory.CipherFactory()
    c.load_cmd_cfg(parse_obj=args)
    c.create_vault()
    assert os.path.exists("sec.vault")
