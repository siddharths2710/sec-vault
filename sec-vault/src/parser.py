import ciphers
import pkgutil
import argparse
import logging

import cipherfactory

class CLIParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(prog='sec-vault', description='Password management CLI tool', fromfile_prefix_chars='@')
        self._populated_args = False

    def parse_args(self,*args):
        if not self._populated_args:
            self._load_args()
            self._populated_args = True
        return super().parse_args(*args)

    def _load_args(self):
        self.add_argument("--create-vault", action="store_true", help="Create Vault file", dest="create_vault", required=False)
        self.add_argument("--add-entry", type=str, help="Add a new record for secure storage into the vault")
        self.add_argument("--del-entry", type=str, help="Delete a record in the vault")
        self.add_argument("--modify-entry", type=str, help="Modify a record in the vault")
        self.add_argument("--encrypt", action="store_true", help="Perform Vault encryption operation", dest="encrypt", required=False)
        self.add_argument("--decrypt", action="store_true", help="Perform Vault decryption operation", dest="decrypt", required=False)
        self.add_argument("--cipher-suite", action="store", type=str, \
                        dest="suite", help="Specify the cipher backend, one of {}".format(
                                    ", ".join(cipherfactory.CipherFactory.cipher_suites)))
        self.add_argument("--cipher-config-file", type=str, 
                help="Path to YAML-based parameter file", dest="cfg_path", required=False)