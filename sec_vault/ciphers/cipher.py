"""Base wrapper for cipher derivatives"""
import os
import base64
import logging
from . import cipher_utils

class Encryptor:
    """BaseClass template for Encryptor class inherited by CipherSuites.
    Essential parameters such as generated keys and cipher modes
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs: dict):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        param_dict = cipher_params
        param_dict.update(arg_params); param_dict.update(kwargs)
        for key in param_dict:
            setattr(self, "__{}".format(key),
                    param_dict.get(key, cipher_utils.gen_random_secret(32)))

    def encrypt(self, plain_text: str):
        """Template method for encryption of a single message

        :param plain_text: input message for encryption
        :type str
        :returns: encrypted output for secure storage
        :rtype str
        """
        return ""

class Decryptor:
    """BaseClass template for Decryptor class inherited by CipherSuites.
    Essential parameters such as generated keys and cipher modes
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, cipher_params={}, arg_params={}, **kwargs: dict):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        for key in dict(cipher_params.items() + arg_params.items() + kwargs.items()):
            setattr(self, "__{}".format(key), value)

    def decrypt(self, cipher_text: str):
        """Template method for decryption of a cipher text

        :param cipher_text: input message for decryption
        :type str
        :returns: decryption output access/modification
        :rtype str
        """
        return ""

if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_ARGS = {}

