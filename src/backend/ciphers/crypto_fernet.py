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

class Encryptor(cipher.Encryptor, backend=None):
    def __init__(self):
        self.__key = Fernet.generate_key()
        self._fernet = Fernet(self.__key, backend)
    
    @staticmethod
    def get_supported_ciphers():
        if 'Backend' in dir(cryptography.hazmat.backends.interfaces):
            return cipher_utils.sanitize_attr(cryptography.hazmat.backends.interfaces.Backend)
        else:
            return cipher_utils.sanitize_attr(cryptography.hazmat.backends.openssl.backend)

    def encrypt(self, plain_text: str, encoding="utf-8"):
        return self._fernet.encrypt(plain_text.encode(encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, key="", backend=None):
        self._fernet = Fernet(self.__key, backend=None)

    def decrypt(self, token):
        return self._fernet.decrypt(token)