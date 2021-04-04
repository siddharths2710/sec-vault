import os
import copy
import glob
import logging
import zipfile
import tempfile

class PwdZipFile(zipfile.ZipFile):
    def __init__(
                self, infile='', outfile='', mode='r', 
                compresslevel=9, allowZip64=True,
                tmp_dir=None, **cipher_args={}):
        self._mode = mode
        self._cparams = cipher_args
        self._tmp_dir = tmp_dir or ".tmp"
        self._file = infile if mode is 'r' else outfile
        self._valid_attr = lambda attr: attr[:2] == "__" \
                            and attr[-2:] != "__"
        super(PwdZipFile, self).__init__(
                file = self._file, mode=mode, 
                compression=zipfile.ZIP_DEFLATED,
                compresslevel, allowZip64)
        
    def _store_encrypted(self, plain_text):
        if self._mode not in {'w', 'a'}:
            logging.error('wrong mode set for zipfile')
            return False
        enc1, enc2 = Encryptor(self._cparams), 
                     Encryptor(self._cparams)
        seeds1 = filter(self._valid_attr, dir(enc1))
        seeds2 = filter(self._valid_attr, dir(enc2))
        ctext = enc1.encrypt(plain_text)
        enc_seeds1 = map(lambda seed: 
            { seed[2:]: enc2.encrypt(getattr(enc1, seed, ""))},
            seeds1)
        self.writestr("vault", ctext)
        for seed in enc_seeds1:
            self.writestr(
                "{}/{}".format(self._tmp_dir, seed), 
                enc_seeds1[seed]
            )
        if not os.path.isdir(self._tmp_dir):
            os.mkdir(self._tmp_dir)
        for seed in seeds2:
            val = getattr(enc2, seed, "")
            fd,  tmp_path = tempfile.mkstemp(
                            prefix = "{}_".format(seed),
                            dir = self._tmp_dir
                        )
            with os.fdopen(fd, "w") as tmp_file:
                tmp_file.write("{}:{}".format(seed, val))
            else:
                os.rename(tmp_file, final_path)
            logging.info("seed: {} flushed to: {}".format(
                seed, final_path
            ))
        logging.info("Please maintain above files securely"
                    "for vault decryption")
        return True
    def _retrieve_msg(self, **kwargs):
        if self._mode[0] != 'r':
            logging.error("zipfile operation requires write mode")
            return ""
        seed_args = copy.deepcopy(kwargs)
        if 'seed-dir' in kwargs:
            if not os.path.isdir(kwargs['seed-dir']):
                logging.error("seed directory does not exist")
                return ""
            for seed_file in glob.glob(kwargs['seed-dir']):
                f = open(seed_file, 'r')
                try:
                    seed, value = f.read().split(
                                    kwargs.get("seed-delim",":")
                                    )
                    seed_args.update({seed: value})
                except Exception as e:
                    logging.error("invalid seed file format", exc_info=True)
                finally:
                    f.close()
        else:
            if not os.path.isdir(self._tmp_dir):
                break
            for seed_path in glob.glob(self._tmp_dir):
                seed_file = open(seed_path, 'r')
                try:
                    seed, value = seed_file.read().split(':')
                    seed_args.update({seed: value})
                except Exception as e:
                    logging.error("invalid seed file format", exc_info=True)
                finally:
                    seed_file.close()

        dec1 = Decryptor(**seed_args)
        root = zipfile.Path(self)
        if not (root / 'vault').exists():
            logging.error(
                "vault missing in zipfile", 
                exc_info=True
                )
            return ""
        elif not (root / self._tmp_dir).exists():
            logging.error(
                "temp directory missing in zipfile", 
                exc_info=True
                )
            return ""
        for arg_path in (root / self._tmp_dir).iterdir():
            try:
                kwargs.update({
                    arg_path.name:
                    dec1.decrypt(arg_path.read_text()) 
                })
            except Exception:
                logging.error(
                        "fetching decrypt params failed", 
                        exc_info=True
                    )
        try:
            dec2 = Decryptor(**kwargs)
            plain_text = dec2.decrypt((root / 'vault').read_text)
        except Exception:
            logging.error('decrypting vault failed', exc_info=True)
            return ""
        return plain_text