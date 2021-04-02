import os
import logging
import zipfile
import tempfile

class PwdZipFile(zipfile.ZipFile):
    def __init__(self, infile='', outfile='', mode='r'):
        self._file = infile if mode is 'r' else outfile
        self._tmp_dir = ".tmp"
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9, allowZip64=True)
        
    def _store_encrypted(self, plain_text):
        enc1, enc2 = Encryptor(), Encryptor()
        seeds1 = filter(lambda attr: attr[:2] == "__", dir(enc1))
        seeds2 = filter(lambda attr: attr[:2] == "__", dir(enc2))
        ctext = enc1.encrypt(plain_text)
        enc_seeds1 = map(
            lambda seed: 
            { seed[2:]: enc2.encrypt(
                            getattr(enc1, seed, "")
                            )},
            seeds1
            )
        self.writestr("vault", ctext)
        for seed in enc_seeds1:
            self.writestr(
                "{}/{}".format(self._tmp_dir, seed), 
                enc_seeds1[seed]
            )
        private_dir = "/".join(os.getcwd(), ".private")
        if not os.path.isdir(private_dir):
            os.mkdir(private_dir)
        for seed in seeds2:
            val = getattr(enc2, seed, "")
            fd,  tmp_path = tempfile.mkstemp(
                            prefix = "{}_".format(seed),
                            dir = private_dir
                        )
            with os.fdopen(fd, "w") as tmp_file:
                
    def _retrieve_file(self):
        key_f = self.open("{}/ke
        y".format(self._tmp_dir))
        iv_f = self.open("{}/iv".format(self._tmp_dir))
        key, iv = key_f.read(), iv_f.read()
        key_f.close(); iv_f.close()