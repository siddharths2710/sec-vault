
import os
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)
import sec_vault.ciphers.crypto_backend as crypto_backend
    

@pytest.fixture
def cipher_params():
    return {
        "algorithm": "AES",
        "mode": "CBC"
    }

@pytest.fixture
def arg_params():
    return {
        "key": os.urandom(32),
        "iv": os.urandom(16)
    }

def test_cipher(cipher_params, arg_params):
    test_message = "test: crypto_backend"
    enc = crypto_backend.Encryptor(cipher_params=cipher_params, arg_params=arg_params)
    cipher_text = enc.encrypt(test_message)
    pad_len = vars(enc)['_Encryptor__pad_len']
    arg_params["pad_len"] = pad_len
    dec = crypto_backend.Decryptor(cipher_params=cipher_params, arg_params=arg_params)
    plain_text = dec.decrypt(cipher_text)
    assert plain_text == test_message