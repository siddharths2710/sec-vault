from . import cipher_utils

import os
import base64
import logging

class Encryptor:
    def __init__(self, **kwargs: dict):
        for key in kwargs:
            setattr(self, "__{}".format(key), value)
    
    def encrypt(self, plain_text: str):
        return ""

class Decryptor:
    def __init__(self, **kwargs: dict):
        for key in kwargs:
            setattr(self, "__{}".format(key), value)

    def decrypt(self, cipher_text: str):
        return ""

if __name__ != "__main__":
    pass
