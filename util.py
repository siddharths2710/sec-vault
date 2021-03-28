import os
import re
import base64
import logging
import zipfile
import pickle
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

class Encryptor:
    def __init__(self, mode=modes.GCM):
        self._key = os.urandom(32)
        self._iv = os.urandom(64)
        self._cipher = Cipher(
                algorithms.AES(self._key),
                mode(self._iv),
                default_backend()
            )

    def encrypt(self, plain_text):
        enc = self._cipher.encryptor()
        cipher_text = enc.update(plain_text) \
                      + enc.finalize()
        return cipher_text

class Decryptor:
    def __init__(self, input, mode=modes.GCM, key="", cipher_text="", iv=""):
        self._key = base64.b64decode(key)
        self._iv = base64.b64decode(iv)
        self._cipher = Cipher(
                algorithms.AES(self._key),
                mode(self._iv),
                default_backend()
            )

    def decrypt(self):
        dec = self._cipher.decryptor()
        plain_text = dec.update(self._ctext) \
                    + dec.finalize()
        return plain_text

class PwdZipFile(zipfile.ZipFile):
    def __init__(self, infile='', outfile='', mode=' r'):
        self._file = infile if mode is 'r' else outfile
        self._tmp_dir = ".tmp"
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9, allowZip64=True)
        
    def _store_encrypted(self):
        enc = Encryptor()
        key = base64.b64encode(getattr(enc, "_key", ""))
        iv = base64.b64encode(getattr(enc, "_iv", ""))
        with open(self._file, 'r') as pwd_file:
            ctext = enc.encrypt(pwd_file.read())
            self.writestr("vault", ctext)
            self.writestr("{}/key".format(self._tmp_dir), key.decode('utf-8'))
            self.writestr("{}/iv".format(self._tmp_dir), iv.decode('utf-8'))
            if os.path.exists(self._file):
                os.unlink(self._file)
    
    def _retrieve_file(self):

class PwdFileHandler:
    def __init__(self, file_path):
        self._file_path = file_path
        self._df = pd.read_csv(file_path, sep="\t", index_col="Name")
        self._pattern_index = {}

    def find_record(self, name_pattern):
        pattern = re.compile(name_pattern)
        for record in self._df.iterrows():
            if pattern.search(record[0], 0, 5) is not None:
                print(record)

    def get_cred(self, name):
        return self._df.loc[name]

    def to_archive(file_path):
        zpf = PwdZipFile(outfile=file_path)
        zpf.write(self._file_path)
        
    def to_pickle(self):
        return pickle.dumps(self._df)

class StegFileHandler:
    def __init__(self, file_path):
        