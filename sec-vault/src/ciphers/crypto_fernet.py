import os
import re
import base64
import typing

from cryptography.fernet import Fernet
import cryptography.hazmat.backends.interfaces
import cryptography.hazmat.backends.openssl.backend

from . import cipher, cipher_utils

class Encryptor(cipher.Encryptor, backend=None, kwargs):
    def __init__(self):
        self.__key = Fernet.generate_key()
        fernet_params = {}
        if 'params' in kwargs:
            if 'fernet' in kwargs['params']:
                fernet_params.update(kwargs['params']['fernet'])
        self._fernet = Fernet(self.__key, backend, **fernet_params)

    def encrypt(self, plain_text: str, encoding="utf-8"):
        return self._fernet.encrypt(plain_text.encode(encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, key="", backend=None, **kwargs):
        fernet_params = {}
        if 'params' in kwargs:
            if 'fernet' in kwargs['params']:
                fernet_params.update(kwargs['params']['fernet'])
        self._fernet = Fernet(self.__key, backend, **fernet_params)

    def decrypt(self, token):
        return self._fernet.decrypt(token)

if __name__ != "__main__":
    backend_package = cryptography.hazmat.backends.interfaces.Backend \
    if 'Backend' in dir(cryptography.hazmat.backends.interfaces) else \
                    cryptography.hazmat.backends.openssl.backend
    CIPHER_PKG = {'backend': backend_package}
    CIPHER_SUITE = {
                        k:cipher_utils.expand_attrs(v) \
                        for k,v in CIPHER_PKG
                   }
