import os
import re
import csv
import pickle
import base64
import logging
import zipfile
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
        pass

class PwdFileHandler:
    def __init__(self, file_path):
        self._file_path = file_path
        self._query_index = {}
        self._cache = []

    def __build_cache(self):
        with open(self._file_path, 'r') as pwd_file:
            pwd_reader = csv.reader(pwd_file)
            self._cache = list(pwd_reader)


    def _find_record(self, name_pattern):
        if name_pattern in self._query_index:
            return self._query_index[name_pattern]
        pattern = re.compile(name_pattern)
        locations = []
        for idx, record in enumerate(self._cache):
            if pattern.search(record[0]) is not None:
                locations.append(idx)
        self._query_index = locations
        return locations
    
    def get_entries(self, search_term):
        indexes = self._find_record(search_term)
        print("service\tlogin_id\tcredential")
        for idx in indexes:
            print("{}\t{}\t{}".format(*self._cache[idx]))

    def to_archive(self, file_path):
        zpf = PwdZipFile(outfile=file_path)
        zpf.write(self._file_path)
        
    def to_pickle(self):
        return pickle.dumps(self._cache)

class StegFileHandler:
    def __init__(self, file_path):
        pass