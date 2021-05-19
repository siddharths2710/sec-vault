import os
import base64
import logging
from . import cipher, cipher_utils

import nacl.utils
from nacl.public import PrivateKey, Box

"""Libsodium wrapper using pyNaCl library"""

class Encryptor(cipher.Encryptor):
    """Wrapper for nacl encryption"""
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs):
        self.__key_size = arg_params.get("key_size", "32")
        self.__encoding = arg_params.get("encoding", "utf-8")
        self._private_key = cipher_params.get("private_key", cipher_utils.gen_random_secret(int(self.__key_size)))
        pkey_obj = PrivateKey(self._private_key.encode(self.__encoding))
        self.cipher = Box(pkey_obj, pkey_obj.public_key)

    def encrypt(self, plain_text: str):
        return self.cipher.encrypt(plain_text.encode('utf-8'))

class Decryptor(cipher.Decryptor):
    """Wrapper for nacl decryption"""
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs):
        if 'private_key' not in cipher_params:
            raise Exception("Missing private key in cipher param config for decryption.")
        self._private_key = cipher_params["private_key"]
        self.__encoding = arg_params.get("encoding", "utf-8")
        pkey_obj = PrivateKey(self._private_key.encode(self.__encoding))
        public_key = pkey_obj.public_key
        self.cipher = Box(pkey_obj, pkey_obj.public_key)

    def decrypt(self, cipher_text):
        return self.cipher.decrypt(cipher_text).decode(self.__encoding)

if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_ARGS = {}
