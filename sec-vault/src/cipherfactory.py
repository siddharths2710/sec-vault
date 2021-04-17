import re
import csv
import copy
import base64
import logging
import tempfile
import pwdzipfile

import ciphers
import ciphers.cipher

def _valid_encr_attr(attr):
    return attr[:12] == '_Encryptor__'

def _safe_write(directory, name, content):
        fd,  tmp_path = tempfile.mkstemp(
                        prefix = "{}_".format(name),
                        dir = directory
                    )
        with os.fdopen(fd, "w") as tmp_file:
            tmp_file.write(content)
        final_path = os.path.join(directory, name)
        if not os.path.isfile(final_path):
            os.rename(tmp_file, final_path)
        else:
            final_path = tmp_path
        return final_path

class CipherMeta(type):
    def __init__(cls, *args, **kwargs):
        pass

    @property
    def cipher_suites(self):
        cipher_modules = pkgutil.iter_modules(ciphers.__path__)
        cipher_names = map(lambda module: module.name, cipher_modules)
        return filter(lambda suite: suite[:6] != 'cipher', cipher_names)

class CipherFactory(metaclass=CipherMeta):
    def __init__(self):
        pass
    
    def load_parser_cfg(self, parse_obj):
        pass
    
    def load_yaml_cfg(self, yaml_obj):
        pass

    @property
    def encryptor(self):
        pass
    
    @property
    def decryptor(self):
        pass

def encrypt_and_store(enc1, enc2, plain_text, outfile, key_store):
    if not ( isinstance(enc1, ciphers.cipher.Encryptor) and isinstance(enc2, ciphers.cipher.Encryptor)):
        raise Exception("Encryptor object does not conform to base class")
    zip_obj = pwdzipfile.PwdZipFile(outfile=outfile, mode='w')
    seeds1 = filter(_valid_encr_attr, dir(enc1))
    seeds2 = filter(_valid_encr_attr, dir(enc2))
    ctext = enc1.encrypt(plain_text)
    enc_seeds1 = map(lambda seed: 
        { seed[12:]: enc2.encrypt(getattr(enc1, seed, ""))},
        seeds1)
    zip_obj.writestr("vault", ctext)
    for seed in enc_seeds1:
        zip_obj.writestr(
            "{}/{}".format(key_store, seed), 
            enc_seeds1[seed]
        )
    if not os.path.isdir(key_store):
        os.mkdir(key_store)
    for seed in seeds2:
        val = getattr(enc2, seed, "")
        final_path = _safe_write(seed[12:],val)
        logging.info("seed: {} flushed to: {}".format(
            seed[12:], final_path
        ))
    logging.info("Please maintain above files securely"
                "for vault decryption")
    return True

def retrieve_msg(zip_obj: pwdzipfile.PwdZipFile, key_store: str, **kwargs):
    if zip_obj._mode[0] != 'r':
        logging.error("zipfile operation requires write mode")
        return ""
        if not isinstance(seed_decr, ciphers.cipher.Decryptor):
    root = zipfile.Path(zip_obj)
    if not (root / 'vault').exists():
        logging.error(
            "vault missing in zipfile", 
            exc_info=True
            )
        return ""
    elif not (root / key_store).exists():
        logging.error(
            "temp directory missing in zipfile", 
            exc_info=True
            )
        return ""
    for arg_path in (root / key_store).iterdir():
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
