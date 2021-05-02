import os
import pytest


#>>> import cipherfactory
#>>> import parser
#>>> p=parser.CLIParser()
#>>> a=p.parse_args()>>> c=cipherfactory.CipherFactory()
#>>> c.load_cmd_cfg(parse_obj=a)>>> c.create_vault()

@pytest.fixture
def create_args():
    return ["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend",  "--record-type", "login", "--create-vault"]

def test_create_vault(create_args):
