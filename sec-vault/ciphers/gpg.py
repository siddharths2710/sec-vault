import gnupg
import logging
from . import cipher

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
        self.__recipients = []
        self._encrypt_args = {}
        self.__encoding = "utf-8"
        self.__key_data = None
        if 'arg_params' in kwargs:
            self.__recipients = kwargs['arg_params'].pop("recipients", [])
            self._encoding = kwargs['arg_params'].pop("encoding", "utf-8")
            self._key_data = kwargs['arg_params'].pop("key_data", None)
            self._encrypt_args = kwargs['arg_params']
        self.gpg = gnupg.GPG(**cipher_params)
        self._import_keys()
        
    def _import_keys(self):
        if self._key_data is not None and \
                not bool(self.gpg.import_keys(self._key_data)):
            logging.error("import of key_data failed", self._key_data)
        return
        
    def encrypt(self, plain_text):
        """Template method for encryption of a single message
        
        :param plain_text: input message for encryption
        :type str
        :returns: encrypted output for secure storage
        :rtype str
        """
        res = self.gpg.encrypt(plain_text, 
                    *self.__recipients, **self._encrypt_args
                    )
        if not res.ok:
            logging.error(
                "gpg encryption error: ",
                res.stderr
            )
        return res.data.encode(self._encoding)

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
        self._decrypt_args = arg_params
        self._encoding = self._decrypt_args.pop("encoding", "utf-8")
        self._key_data = self._decrypt_args.pop("key_data", None)
        self.gpg = gnupg.GPG(**cipher_params)
        self._import_keys()
    
    def _import_keys(self):
        if self._key_data is not None and \
                not bool(self.gpg.import_keys(self._key_data)):
            logging.error("import of key_data failed", self._key_data)
        return

    def decrypt(self, cipher_text):
        try:
            res = self.gpg.decrypt(cipher_text, **self._decrypt_args)
            if not res.ok:
                logging.error(
                    "gpg encryption error: ",
                    res.stderr
                )
            return res.data.decode(self._encoding)
        except Exception as e:
            logging.error("gpg decryption failure", exc_info=True)

if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_SUITE = {}
