import os
import base64
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

class Encryptor:
    def __init__(self, mode=modes.GCM):
        self.__key = os.urandom(32)
        self.__iv = os.urandom(64)
        self._cipher = Cipher(
                algorithms.AES(self.__key),
                mode(self.__iv),
                default_backend()
            )

    def encrypt(self, plain_text):
        enc = self._ciphe   r.encryptor()
        cipher_text = enc.update(plain_text) \
                      + enc.finalize()
        return cipher_text

class Decryptor:
    def __init__(self, input, mode=modes.GCM, key="", cipher_text="", iv=""):
        self.__key = base64.b64decode(key)
        self.__iv = base64.b64decode(iv)
        self._ctext = cipher_text
        self._cipher = Cipher(
                algorithms.AES(self.__key),
                mode(self.__iv),
                default_backend()
            )

    def decrypt(self):
        dec = self._cipher.decryptor()
        plain_text = dec.update(self._ctext) \
                    + dec.finalize()
        return plain_text