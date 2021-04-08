import cipher
import cipher_utils

import os
import base64
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

def get_cipher_package():
    return modes

class Encryptor(cipher.Encryptor):
    def __init__(self, algo=algorithms.AES, mode=modes.GCM, encoding='utf-8', 
                                    key=None, iv=None, key_size=32, iv_size=16, **kwargs):
        self.__key = key or os.urandom(key_size)
        self.__iv = iv or os.urandom(iv_size)
        self._cipher = Cipher(
                algo(self.__key, **kwargs.get("algo_params", None)),
                mode(self.__iv, **kwargs.get("mode_params", None)),
                default_backend()
            )


    def encrypt(self, plain_text):
        enc = self._cipher.encryptor()
        cipher_text = enc.update(plain_text.encode(encoding)) \
                      + enc.finalize()
        return cipher_text

class Decryptor(cipher.Decryptor):
    def __init__(self, input, algo=algorithms.AES, mode=modes.CBC, 
                encoding="utf-8", key=None, cipher_text=None, iv=None, **kwargs):
        if any([key, cipher_text, iv]) is None:
            raise Exception("invalid seed params provided for decryption")
        self.__key = base64.b64decode(key)
        self.__iv = base64.b64decode(iv)
        self._ctext = cipher_text
        self._cipher = Cipher(
                algo(self.__key, **kwargs.get('algo_params', None)),
                mode(self.__iv, **kwargs.get('mode_params', None)),
                default_backend()
            )

    def decrypt(self):
        dec = self._cipher.decryptor()
        plain_text = dec.update(self._ctext) \
                    + dec.finalize()
        return plain_text.decode(encoding)

if __name__ != "__main__":
    cipher_package = modes
    cipher_suite = cipher_utils.sanitize_attr(modes)
