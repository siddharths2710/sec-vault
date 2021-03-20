import os
import base64
import zipfile
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

class PwdZipFile(zipfile.ZipFile):
    def __init__(self, infile='', outfile='', mode='r'):
        self._file = infile if mode is 'r' else outfile
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED, 
                compresslevel=9, allowZip64=True)

class Encryptor:
    def __init__(self):
        self._key = os.urandom(32)
        self._iv = os.urandom(64)
        self._cipher = Cipher(
                algorithms.AES(self._key),
                modes.GCM(self._iv),
                default_backend()
            )

    def encrypt(self, plain_text):
        enc = self._cipher.encryptor()
        cipher_text = enc.update(plain_text) \
                      + enc.finalize()
        final_ctext = base64.b64encode(self._key)  + b'||' \
                    + cipher_text + b'||' \
                    + base64.b64encode(self._iv)
        return final_ctext

class Decryptor:
    def __init__(self, input):
        self._key, self._ctext, self._iv = input.split(b"||")
        self._key = base64.b64decode(self._key)
        self._iv = base64.b64decode(self._iv)
        self._cipher = Cipher(
                algorithms.AES(self._key),
                modes.GCM(self._iv),
                default_backend()
            )

    def decrypt(self):
        dec = self._cipher.decryptor()
        plain_text = dec.update(self._ctext) \ 
                    + dec.finalize()
        return plain_text