import os
import copy
import glob
import logging
import zipfile
import tempfile

class PwdZipFile(zipfile.ZipFile):
    def __init__(
                self, infile='', outfile='', mode='r', 
                compresslevel=9, allowZip64=True):
        self._mode = mode
        self._cparams = cipher_args
        self._file = infile if mode == 'r' else outfile
        super(PwdZipFile, self).__init__(
                file=self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=compresslevel, allowZip64=allowZip64)
