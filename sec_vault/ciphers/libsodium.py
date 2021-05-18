import os
import base64
import logging
from . import cipher_utils

import nacl.utils
from nacl.public import PrivateKey, Box

"""Libsodium wrapper using pyNaCl library"""

class Encryptor:
    """Wrapper for nacl encryption"""
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs: dict):
        pkey_obj = PrivateKey.generate()
        self._private_key = pkey_obj._private_key
        self.cipher = Box(pkey_obj, pkey_obj.public_key)

    def encrypt(self, plain_text: str):
        return self.cipher.encrypt(plain_text.encode('utf-8'))

class Decryptor:
    """Wrapper for nacl decryption"""
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs: dict):
        if 'private_key' not in cipher_params:
            raise Exception("Missing private key in cipher param config for decryption.")
        self._private_key = cipher_params.get["private_key"]
        pkey_obj = PrivateKey(self._private_key)
        public_key = pkey_obj.public_key
        self.cipher = Box(pkey_obj, pkey_obj.public_key)

    def decrypt(self, cipher_text):
        return self.cipher.decrypt(cipher_text).decode('utf-8')

if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_ARGS = {}
