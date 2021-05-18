# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption
import math
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
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        self._algorithm = cipher_params.get("algorithm", "AES")
        self._mode = cipher_params.get("mode", "CBC")
        self.__key = arg_params.get("key", None) or cipher_utils.gen_random_secret(arg_params.get("key_size", 32)).encode('utf-8')
        self.__iv = arg_params.get("iv", None) or cipher_utils.gen_random_secret(arg_params.get("iv_size", 16)).encode('utf-8')
        self.__encoding = arg_params.get("encoding", "utf-8")
        self.__pad_len = 0
        self.__algorithm = arg_params.get("algorithm", {})
        self.__mode = arg_params.get("mode", {})
        if self._algorithm not in CIPHER_ARGS['algorithms']:
            raise Exception("Unsupported algo type {}".format(self._algorithm))
        if self._mode not in CIPHER_ARGS['modes']:
            raise Exception("Unsupported mode type {}".format(self._mode))
        algo_obj = vars(algorithms)[self._algorithm]
        mode_obj = vars(modes)[self._mode]
        self._cipher = Cipher(
                algo_obj(self.__key, **self.__algorithm),
                mode_obj(self.__iv, **self.__mode),
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
        self.__pad_len = (1<<(int(math.log2(l)) + 3)) - l
        ptext_padded =  plain_text + \
            cipher_utils.gen_random_secret(self.__pad_len)
        enc = self._cipher.encryptor()
        cipher_text = enc.update(ptext_padded.encode(self.__encoding)) \
                      + enc.finalize()
        return cipher_text

class Decryptor(cipher.Decryptor):
    """Decryptor class for symmetric decryption through Fernet module.
    Essential parameters such as generated keys and cipher modes 
    are dunder-prefixed for reuse while decrypting the message.
    """
    def __init__(self, cipher_params: dict, arg_params: dict, **kwargs):
        """Initializer for primitives and underlying cipher objects

        :param kwargs: Consolidation of parameters consumed by base cipher library
        :type dict
        """
        self.__key = arg_params.get("key", None)
        self.__iv = arg_params.get("iv", None)
        self.__encoding = arg_params.get("encoding", "utf-8")
        self.__pad_len = arg_params.get("pad_len", 0)
        if any([self.__key, self.__iv]) is None:
            raise Exception("invalid seed params provided for decryption")
        self._algorithm = cipher_params.get("algorithm", "AES")
        self._mode = cipher_params.get("mode", "CBC")
        self.__algorithm = arg_params.get("algorithm", {})
        self.__mode = arg_params.get("mode", {})
        if self._algorithm not in CIPHER_ARGS['algorithms']:
            raise Exception("Unsupported algo type {}".format(self._algorithm))
        if self._mode not in CIPHER_ARGS['modes']:
            raise Exception("Unsupported mode type {}".format(self._mode))
        algo_obj = eval("algorithms.{}".format(self._algorithm))
        mode_obj = eval("modes.{}".format(self._mode))
        self._cipher = Cipher(
                algo_obj(self.__key, **self.__algorithm),
                mode_obj(self.__iv, **self.__mode),
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
    CIPHER_ARGS = {k:cipher_utils.expand_attrs(v) \
                    for k,v in CIPHER_PKG.items()}
