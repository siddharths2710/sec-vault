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

def get_cipher_package():
    if 'Backend' in dir(cryptography.hazmat.backends.interfaces):
        return cryptography.hazmat.backends.interfaces.Backend
    else:
        return cryptography.hazmat.backends.openssl.backend

def get_supported_ciphers():
    return cipher_utils.sanitize_attr(Encryptor.cipher_package)

class Encryptor(cipher.Encryptor, backend=None):
    def __init__(self):
        self.__key = Fernet.generate_key()
        self._fernet = Fernet(self.__key, backend)

    def encrypt(self, plain_text: str, encoding="utf-8"):
        return self._fernet.encrypt(plain_text.encode(encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, key="", backend=None):
        self._fernet = Fernet(self.__key, backend)

    def decrypt(self, token):
        return self._fernet.decrypt(token)
