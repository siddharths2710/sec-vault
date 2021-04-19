from . import cipher_utils

import os
import base64
import logging

class Encryptor:
    """BaseClass template for Encryptor class inherited by CipherSuites.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, **kwargs: dict):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        for key in kwargs:
            setattr(self, "__{}".format(key), value)
    
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
    def __init__(self, **kwargs: dict):
        for key in kwargs:
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
    CIPHER_SUITE = {}