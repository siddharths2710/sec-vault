import os
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
    def encrypt(self, content):
        enc = self._cipher.encryptor()
        plain_text = self._key + b"||" \
                     + content + b"||" \
                     + self._iv
        cipher_text = enc.update(plain_text) \
                      + enc.finalize()
        return cipher_text