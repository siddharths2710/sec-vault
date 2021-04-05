import cipher_utils

import os
import base64
import logging

class Encryptor:
    def __init__(self, **kwargs: dict):
        for key in kwargs:
            setattr(self, "__{}".format(key), value)
    
    @staticmethod
    def get_supported_ciphers():
        return []

    def encrypt(self, plain_text: str)             
        return ""

class Decryptor:
    def __init__(self, cipher_text: str, **kwargs: dict):
        self.__key = base64.b64decode(key)
        self.__iv = base64.b64decode(iv)
        self._ctext = cipher_text
        self._cipher = Cipher(
                algorithms.AES(self.__key),
                mode(self.__iv),
                default_backend()
            )

    def decrypt(self, cipher_text: str):
        return ""