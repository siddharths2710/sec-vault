
import os
import pytest
import sec_vault.ciphers.crypto_openssl as crypto_openssl
    
def test_cipher():
    test_message = "test: crypto_openssl"
    enc = crypto_openssl.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt(test_message)
    key = vars(enc)['_key']
    dec = crypto_openssl.Decryptor(cipher_params={"key": key}, arg_params={})
    plain_text = dec.decrypt(cipher_text)
    assert plain_text == test_message