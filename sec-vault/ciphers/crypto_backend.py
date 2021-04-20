import os
import math
import random
import string
import base64
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

from . import cipher, cipher_utils

class Encryptor(cipher.Encryptor):
    """Encryptor class for symmetric encryption through Fernet module.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, cipher_params={}, arg_params={}, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        self.__key = os.urandom(arg_params.get("key_size", 32))
        self.__iv = os.urandom(arg_params.get("iv_size", 16))
        self.__encoding = arg_params.get("encoding", "utf-8")
        self.__pad_len = 0
        algo_val = cipher_params.get("algorithm", "AES")
        mode_val = cipher_params.get("mode", "CBC")
        algo_params = arg_params.get("algorithm", {})
        mode_params = arg_params.get("mode", {})
        if algo_val not in CIPHER_SUITE['algorithms']:
            raise Exception("Unsupported algo type {}".format(algo_val))
        if mode_val not in CIPHER_SUITE['modes']:
            raise Exception("Unsupported mode type {}".format(mode_val))
        algo_obj = eval("algorithms.{}".format(algo_val))
        mode_obj = eval("modes.{}".format(mode_val))    
        self._cipher = Cipher(
                algo_obj(self.__key, **algo_params),
                mode_obj(self.__iv, **mode_params),
                default_backend()
            )

    def encrypt(self, plain_text):
        """Template method for encryption of a single message
        
        :param plain_text: input message for encryption
        :type str
        :returns: encrypted output for secure storage
        :rtype str
        """
        l = len(plain_text)
        self.__pad_len = (1<<(int(math.log2(l)) + 2)) - l
        ptext_padded =  plain_text + \
            (random.choice(string.printable) * self.__pad_len)
        enc = self._cipher.encryptor()
        cipher_text = enc.update(ptext_padded.encode(self.__encoding)) \
                      + enc.finalize()
        return cipher_text

class Decryptor(cipher.Decryptor):
    """Decryptor class for symmetric decryption through Fernet module.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, cipher_params={}, arg_params={}, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        self.__key = kwargs.get("key", None)
        self.__iv = kwargs.get("iv", None)
        self.__encoding = arg_params.get("encoding", "utf-8")
        self.__pad_len = kwargs.get("pad_len", 0)
        if any([self.__key, self.__iv]) is None:
            raise Exception("invalid seed params provided for decryption")
        algo_val = cipher_params.get("algorithm", "AES")
        mode_val = cipher_params.get("mode", "CBC")
        algo_params = arg_params.get("algorithm", {})
        mode_params = arg_params.get("mode", {})
        if algo_val not in CIPHER_SUITE['algorithms']:
            raise Exception("Unsupported algo type {}".format(algo_val))
        if mode_val not in CIPHER_SUITE['modes']:
            raise Exception("Unsupported mode type {}".format(mode_val))
        algo_obj = eval("algorithms.{}".format(algo_val))
        mode_obj = eval("modes.{}".format(mode_val))    
        self._cipher = Cipher(
                algo_obj(self.__key, **algo_params),
                mode_obj(self.__iv, **mode_params),
                default_backend()
            )

    def decrypt(self, cipher_text):
        """Template method for decryption of a cipher text
        
        :param cipher_text: input message for decryption
        :type str
        :returns: decryption output access/modification
        :rtype str
        """
        dec = self._cipher.decryptor()
        plain_text = dec.update(cipher_text) \
                    + dec.finalize()
        return plain_text.decode(self.__encoding)[:-1*self.__pad_len]

if __name__ != "__main__":
    CIPHER_PKG = {'algorithms': algorithms, 'modes': modes}
    CIPHER_SUITE = {k:cipher_utils.expand_attrs(v) \
                    for k,v in CIPHER_PKG.items()}