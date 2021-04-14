#! /usr/bin/env python3

# User create vault file
# User add credential
# User modify/delete credential
# User view credential
import parser
import config
import ciphers

if __name__ == "__main__":
    vault_parser = parser.CLIParser()
    vault_args = vault_parser.parse_args()
    cfg = {}
    if vault_args.cfg_file is not None:
        cfg = config.CipherConfig(vault_args.cfg_file).load()
