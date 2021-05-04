# https://pythonhosted.org/python-gnupg/#getting-started
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
        self.__recipients = arg_params.pop("recipients", [])
        self.encrypt_args = {}
        self.__encoding = "utf-8"
        self.__key_data = None
        if 'arg_params' in kwargs:
            
            self.__encoding = arg_params.pop("encoding", "utf-8")
            self.__key_data = arg_params.pop("key_data", None)
            self.encrypt_args = arg_params
        self.cipher = gnupg.GPG(**cipher_params)
        self.import_keys()
        
    def import_keys(self):
        if self.__key_data is not None and \
                not bool(self.cipher.import_keys(self.__key_data)):
            logging.error("import of key_data failed", self.__key_data)
        return
        
    def encrypt(self, plain_text):
        """Template method for encryption of a single message
        
        :param plain_text: input message for encryption
        :type str
        :returns: encrypted output for secure storage
        :rtype str
        """
        res = self.cipher.encrypt(plain_text, 
                    *self.__recipients, **self.encrypt_args
                    )
        return res.data.decode(self.__encoding)

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
        self.decrypt_args = arg_params
        self.__encoding = self.decrypt_args.pop("encoding", "utf-8")
        self.__key_data = self.decrypt_args.pop("key_data", None)
        self.cipher = gnupg.GPG(**cipher_params)
        self.import_keys()
    
    def import_keys(self):
        if self.__key_data is not None and \
                not bool(self.cipher.import_keys(self.__key_data)):
            logging.error("import of key_data failed", self.__key_data)
        return

    def decrypt(self, cipher_text):
        try:
            res = self.cipher.decrypt(cipher_text, **self.decrypt_args)
            return res.data.decode(self.__encoding)
        except Exception as e:
            logging.error("gpg decryption failure", exc_info=True)

if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_ARGS = {}
