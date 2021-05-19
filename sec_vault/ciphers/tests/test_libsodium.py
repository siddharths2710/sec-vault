
import os
import pytest
import ciphers.libsodium as libsodium

def test_cipher():
    test_message = "test: pyNaCl"
    enc = libsodium.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt(test_message)
    dec = libsodium.Decryptor(cipher_params={"private_key": enc._private_key}, arg_params={})
    plain_text = dec.decrypt(cipher_text)
    assert plain_text == test_message
