import os
import re
import base64
import pickle
import logging
import zipfile
import pandas as pd
from crypto_backend import Encryptor, Decryptor

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
        