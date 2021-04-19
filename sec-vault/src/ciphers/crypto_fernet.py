import os
import re
import base64
import typing

from cryptography.fernet import Fernet
import cryptography.hazmat.backends.interfaces
import cryptography.hazmat.backends.openssl.backend

from . import cipher, cipher_utils


backend_package = cryptography.hazmat.backends.interfaces.Backend \
if 'Backend' in dir(cryptography.hazmat.backends.interfaces) else \
                cryptography.hazmat.backends.openssl.backend

class Encryptor(cipher.Encryptor):
    def __init__(self, *args, **kwargs):
        backend = None
        cipher_params = kwargs.get("cipher_params", {})
        backend_val = cipher_params.pop("backend", None)
        if backend_val is not None:
            try:
                if backend_val not in CIPHER_SUITE['backend']:
                    raise Exception("")
                backend = eval("backend.{}".format(backend_val))
            except:
                raise Exception("backend {} not supported by Fernet".format(backend_val))
        self.__key = Fernet.generate_key()
        self.__encoding = kwargs.get("arg_params", {}).get("encoding", "utf-8")
        self._fernet = Fernet(self.__key, backend, **kwargs.get('cipher_params',{}))

    def encrypt(self, plain_text: str):
        return self._fernet.encrypt(plain_text.encode(self.__encoding))

class Decryptor(cipher.Decryptor):
    def __init__(self, **kwargs):
        backend = None
        cipher_params = kwargs.get("cipher_params", {})
        backend_val = cipher_params.pop("backend", None)
        if "key" not in cipher_params:
            raise Exception("Fernet decryption requires a symmetric key as input")
        if backend_val is not None:
            try:
                if backend_val not in CIPHER_SUITE['backend']:
                    raise Exception("")
                backend = eval("backend.{}".format(backend_val))
            except:
                raise Exception("backend {} not supported by Fernet".format(backend_val))
        self.__key = cipher_params.pop("key")
        self.__encoding = kwargs.get("arg_params", {}).get("encoding", "utf-8")
        self._fernet = Fernet(self.__key, backend, **cipher_params)

    def decrypt(self, cipher_text):
        return self._fernet.decrypt(cipher_text).decode(self.__encoding)

if __name__ != "__main__":
    CIPHER_PKG = {'backend': backend_package}
    CIPHER_SUITE = {k:cipher_utils.expand_attrs(v) \
                    for k,v in CIPHER_PKG.items()}