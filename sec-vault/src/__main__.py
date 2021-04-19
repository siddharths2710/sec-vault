#! /usr/bin/env python3

# User create vault file
# User add credential
# User modify/delete credential
# User view credential
import parser
import config
import ciphers

import util
from .pwdzipfile import PwdZipFile
from .cipherfactory import CipherFactory

def encrypt_and_store(fc1: CipherFactory, fc2: CipherFactory, 
                        plain_text: str, outfile: str, key_store: str):
    zip_obj = PwdZipFile(outfile=outfile, mode='w')
    enc1, enc2 = fc1.encryptor(), fc2.encryptor()
    seeds1 = filter(util.valid_encr_attr, dir(enc1))
    seeds2 = filter(util.valid_encr_attr, dir(enc2))
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
        final_path = util.safe_write(key_store, seed[12:], val)
        logging.info("seed: {} flushed to: {}".format(
            seed[12:], final_path
        ))
    logging.info("Please maintain above files securely"
                "for vault decryption")
    return True

def retrieve_msg(fc: CipherFactory, zip_obj: pwdzipfile.PwdZipFile, key_store: str, **kwargs):
    if zip_obj._mode[0] != 'r':
        logging.error("zipfile operation requires write mode")
        return ""
        if not isinstance(seed_decr, ciphers.cipher.Decryptor):
    root = zipfile.Path(zip_obj)
    dec1 = fc.decryptor()
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

if __name__ == "__main__":
    vault_parser = parser.CLIParser()
    vault_args = vault_parser.parse_args()
    cfg = {}
    if vault_args.cfg_file is not None:
        cfg = config.CipherConfig(vault_args.cfg_file).load()
