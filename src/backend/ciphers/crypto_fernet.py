import cipher

import os
import base64
import typing
import logging

from cryptography.fernet import Fernet
from cryptography.hazmat.backends.interfaces import Backend

class Encryptor(cipher.Encryptor, backend=None):
    def __init__(self):
        self.__key = Fernet.generate_key()
        self._fernet = Fernet(self.__key, backend)

    def encrypt(self, plain_text: str, encoding="utf-8"):
        return self._fernet.encrypt(plain_text.encode(encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, key="", backend=None):
        self._fernet = Fernet(self.__key, backend=None)

    def decrypt(self, token):
        return self._fernet.decrypt(token)