import cipher
import gnupg

class Encryptor(cipher.Encryptor):
    def __init__(
            self, binary=None, homedir=None, keyring=None,
            secring=None, options=None,
            *recipients, **gpg_encr_args=None
            ):
        self.__recipients = recipients
        self.__encrypt_args = gpg_encr_args
        self.gpg = gnupg.GPG(
                        binary=binary, homedir=homedir, 
                        keyring=keyring, secring=secring, 
                        options=options
                    )
        
    def import_keys(key_data: str):
        if not bool(self.gpg.import_keys(key_data)):
            logging.error("import of key_data failed")
        return
        
    def encrypt(plain_text):
        res = self.gpg.encrypt(plain_text, 
                    self.__recipients, self.__encrypt_args
                    )
        if not res['ok']:
            logging.error(
                "gpg encryption error: ",
                res['stderr']
            )
        return res['data']

class Decryptor(cipher.Decryptor):
    def __init__(
            self, binary=None, homedir=None, keyring=None,
            secring=None, options=None, key_data=None,
            gpg_decr_args=None):
        self._decrypt_args = gpg_decr_args
        self.gpg = gnupg.GPG(
                        binary, homedir, keyring, 
                        secring, options
                    )
        if key_data is not None and 
        not bool(self.gpg.import_keys(key_data)):
            logging.error("import of key_data failed")
    
    def decrypt(cipher_text):
        res = self.gpg.decrypt(cipher_text, self._decrypt_args)
        if not res['ok']:
            logging.error(
                "gpg encryption error: ",
                res['stderr']
            )
        return res['data']

if __name__ != "__main__":
    pass