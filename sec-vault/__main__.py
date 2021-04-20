#! /usr/bin/env python3

import parser
import config
import ciphers

import util
import cipherfactory

def encrypt_and_store(fc: cipherfactory.CipherFactory, plain_text: str, 
                                    outfile: str, key_store: str, **kwargs):
    enc = fc.encryptor(kwargs)
    seeds = filter(util.valid_encr_attr, dir(enc))
    ctext = enc.encrypt(plain_text)
    

def retrieve_msg(fc: cipherfactory.CipherFactory, key_store: str, **kwargs):
    return ""

if __name__ == "__main__":
    vault_parser = parser.CLIParser()
    factory = cipherfactory.CipherFactory()
    vault_args = vault_parser.parse_args()
    cfg = {}
    if vault_args.cfg_file is not None:
        cfg = config.CipherConfig(vault_args.cfg_file).load()
    factory.load_cmd_cfg(parser.__dict__)
    factory.load_param_cfg(cfg)