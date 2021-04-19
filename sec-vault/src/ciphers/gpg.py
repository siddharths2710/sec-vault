import gnupg
import logging
from . import cipher

class Encryptor(cipher.Encryptor):
    def __init__(self, **kwargs):
        self.__recipients = []
        self._encrypt_args = {}
        self.__encoding = "utf-8"
        self.__key_data = None
        if 'arg_params' in kwargs:
            self.__recipients = kwargs['arg_params'].pop("recipients", [])
            self._encoding = kwargs['arg_params'].pop("encoding", "utf-8")
            self._key_data = kwargs['arg_params'].pop("key_data", None)
            self._encrypt_args = kwargs['arg_params']
        self.gpg = gnupg.GPG(**kwargs.get('cipher_params',{}))
        self._import_keys()
        
    def _import_keys(self):
        if self._key_data is not None and \
                not bool(self.gpg.import_keys(self._key_data)):
            logging.error("import of key_data failed", self._key_data)
        return
        
    def encrypt(self, plain_text):
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
    def __init__(self, **kwargs):
        self._decrypt_args = kwargs.get("arg_params", {})
        self._encoding = self._decrypt_args.pop("encoding", "utf-8")
        self._key_data = self._decrypt_args.pop("key_data", None)
        self.gpg = gnupg.GPG(**kwargs.get('cipher_params',{}))
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
