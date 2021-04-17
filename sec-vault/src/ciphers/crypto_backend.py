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
    def __init__(self, algo=algorithms.AES, mode=modes.CBC, encoding='utf-8',
                                key_size=32, iv_size=16, *args,**kwargs):
        self.__key = os.urandom(key_size)
        self.__iv = os.urandom(iv_size)
        self.__encoding = encoding
        self.__pad_len = 0
        algo_params = {}
        mode_params = {}
        if 'params' in kwargs:
            if 'algorithm' in kwargs['params']:
                algo_params.update(kwargs['params']['algorithm'])
            if 'mode' in kwargs['params']:
                mode_params.update(kwargs['params']['mode'])
        self._cipher = Cipher(
                algo(self.__key, **algo_params),
                mode(self.__iv, **mode_params),
                default_backend()
            )


    def encrypt(self, plain_text):
        l = len(plain_text)
        self.__pad_len = (1<<(int(math.log2(l)) + 1)) - l
        ptext_padded =  plain_text + \
            (random.choice(string.printable) * self.__pad_len)
        enc = self._cipher.encryptor()
        cipher_text = enc.update(ptext_padded.encode(self.__encoding)) \
                      + enc.finalize()
        return cipher_text

class Decryptor(cipher.Decryptor):
    def __init__(self, input, algo=algorithms.AES, mode=modes.CBC, pad_len=0,
                encoding="utf-8", key=None, cipher_text=None, iv=None, **kwargs):
        if any([key, cipher_text, iv]) is None:
            raise Exception("invalid seed params provided for decryption")
        self.__key = key
        self.__iv = iv
        self.__encoding = encoding
        self.__pad_len = pad_len
        self._ctext = cipher_text
        algo_params = {}
        mode_params = {}
        if 'params' in kwargs:
            if 'algorithm' in kwargs['params']:
                algo_params.update(kwargs['params']['algorithm'])
            if 'mode' in kwargs['params']:
                mode_params.update(kwargs['params']['mode'])
        self._cipher = Cipher(
                algo(self.__key, **algo_params),
                mode(self.__iv, **mode_params),
                default_backend()
            )

    def decrypt(self):
        dec = self._cipher.decryptor()
        plain_text = dec.update(self._ctext) \
                    + dec.finalize()
        return plain_text.decode(encoding)[:-1*self.__pad_len]

if __name__ != "__main__":
    CIPHER_PKG = {'algorithms': algorithms, 'modes': modes}
    CIPHER_SUITE = {
                        k:cipher_utils.expand_attrs(v) \
                        for k,v in CIPHER_PKG.items()
                    }
