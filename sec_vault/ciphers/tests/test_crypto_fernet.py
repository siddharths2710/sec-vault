
import os
import pytest
import ciphers.crypto_fernet as crypto_fernet
    
def test_cipher():
    test_message = "test: crypto_fernet"
    enc = crypto_fernet.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt(test_message)
    key = vars(enc)['_key']
    dec = crypto_fernet.Decryptor(cipher_params={"key": key}, arg_params={})
    plain_text = dec.decrypt(cipher_text)
    assert plain_text == test_message
