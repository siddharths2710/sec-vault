class PwdZipFile(zipfile.ZipFile):
    def __init__(self, infile='', outfile='', mode='r'):
        self._file = infile if mode is 'r' else outfile
        self._tmp_dir = ".tmp"
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9, allowZip64=True)
        
    def _store_encrypted(self, plain_text):
        enc = Encryptor()
        key = base64.b64encode(getattr(enc, "_key", ""))
        iv = base64.b64encode(getattr(enc, "_iv", ""))
        ctext = enc.encrypt(plain_text)
        self.writestr("vault", ctext)
        self.writestr("{}/key".format(self._tmp_dir), key.decode('utf-8'))
        self.writestr("{}/iv".format(self._tmp_dir), iv.decode('utf-8'))
        if os.path.exists(self._file):
            os.unlink(self._file)
    
    def _retrieve_file(self):
        key_f = self.open("{}/key".format(self._tmp_dir))
        iv_f = self.open("{}/iv".format(self._tmp_dir))
        key, iv = key_f.read(), iv_f.read()
        key_f.close(); iv_f.close()