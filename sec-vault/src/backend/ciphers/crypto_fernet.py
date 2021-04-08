import cipher
import cipher_utils

import os
import re
import base64
import typing
import logging

from cryptography.fernet import Fernet
import cryptography.hazmat.backends.interfaces
import cryptography.hazmat.backends.openssl.backend

class Encryptor(cipher.Encryptor, backend=None, **kwargs):
    def __init__(self):
        self.__key = Fernet.generate_key()
        self._fernet = Fernet(self.__key, backend, **kwargs)

    def encrypt(self, plain_text: str, encoding="utf-8"):
        return self._fernet.encrypt(plain_text.encode(encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, key="", backend=None, **kwargs):
        self._fernet = Fernet(self.__key, backend, **kwargs)

    def decrypt(self, token):
        return self._fernet.decrypt(token)

if __name__ != "__main__":
    cipher_package = cryptography.hazmat.backends.interfaces.Backend \
    if 'Backend' in dir(cryptography.hazmat.backends.interfaces) else \
                    cryptography.hazmat.backends.openssl.backend
    cipher_suite = cipher_utils.sanitize_attr(cipher_package)
