import os
import pytest
import parser

@pytest.fixture
def valid_create_args():
    return ["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend",  "--record-type", "login", "--create-vault"]

@pytest.fixture
def valid_add_args(valid_create_args):
    return valid_create_args[:-1] + ["--add-entry"]

@pytest.fixture
def invalid_record_args(valid_create_args):
    return valid_create_args[:-2] + ["invalid"]

@pytest.fixture
def invalid_cipher_args(valid_create_args):
    return ["--vault-file","sec.vault","--cipher-suite","invalid","--record-type", "login", "--add-entry"]

@pytest.fixture
def missing_record_args(valid_create_args):
    return valid_create_args[:-3]

@pytest.fixture
def missing_suite_args(valid_add_args):
    return ["--create-vault", "--vault-file", "sec.vault", "--record-type", "login"]

valid_fixtures = (valid_create_args, valid_add_args)
invalid_fixtures = (invalid_cipher_args, invalid_record_args)
missing_fixtures = (missing_record_args, missing_suite_args)
all_fixtures = valid_fixtures + invalid_fixtures + missing_fixtures

def test_cli_parser(*all_fixtures):
    for args in all_fixtures:
        ret = os.fork()
        if ret == 0:
            parser = parser.CLIParser()
            res = parser.parse_args(args)
        elif ret == -1:
            print("Child wasn't able to run")
            assert False
        else:
            child, err = os.wait()[1]
            assert not bool(err) if args in valid_fixtures else bool(err)
