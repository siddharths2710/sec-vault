import zipfile

class PwdZipFile(zipfile.ZipFile):
    def __init__(self, infile='', outfile='', mode='r'):
        self._file = infile if mode is 'r' else outfile
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED, 
                compresslevel=9, allowZip64=True)