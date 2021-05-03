# https://cryptography.io/en/latest/fernet
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
    """Encryptor class for symmetric encryption through Fernet module.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        backend = None
        cipher_params = kwargs.get("cipher_params", {})
        backend_val = cipher_params.pop("backend", None)
        if backend_val is not None:
            try:
                if backend_val not in CIPHER_ARGS['backend']:
                    raise Exception("")
                backend = vars(backend)[backend_val]
            except:
                raise Exception("backend {} not supported by Fernet".format(backend_val))
        self._key = cipher_params.get("key", Fernet.generate_key())
        self.__encoding = kwargs.get("arg_params", {}).get("encoding", "utf-8")
        self.fernet = Fernet(self._key, backend, **kwargs.get('cipher_params',{}))

    def encrypt(self, plain_text: str):
        """Template method for encryption of a single message
        
        :param plain_text: input message for encryption
        :type str
        :returns: encrypted output for secure storage
        :rtype str
        """
        return self.fernet.encrypt(plain_text.encode(self.__encoding))

class Decryptor(cipher.Decryptor):
    """Decryptor class for symmetric decryption through Fernet module.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        backend = None
        cipher_params = kwargs.get("cipher_params", {})
        backend_val = cipher_params.pop("backend", None)
        if "key" not in cipher_params:
            raise Exception("Fernet decryption requires a symmetric key as input")
        if backend_val is not None:
            try:
                if backend_val not in CIPHER_ARGS['backend']:
                    raise Exception("")
                backend = vars(backend)[backend_val]
            except:
                raise Exception("backend {} not supported by Fernet".format(backend_val))
        self._key = cipher_params.pop("key")
        self.__encoding = kwargs.get("arg_params", {}).get("encoding", "utf-8")
        self.fernet = Fernet(self._key, backend, **cipher_params)

    def decrypt(self, cipher_text):
        """Template method for decryption of a cipher text
        
        :param cipher_text: input message for decryption
        :type str
        :returns: decryption output access/modification
        :rtype str
        """
        return self.fernet.decrypt(cipher_text).decode(self.__encoding)

if __name__ != "__main__":
    CIPHER_PKG = {'backend': backend_package}
    CIPHER_ARGS = {k:cipher_utils.expand_attrs(v) \
                    for k,v in CIPHER_PKG.items()}
