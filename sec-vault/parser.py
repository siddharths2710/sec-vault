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
        self.add_argument("--vault-file", type=str, 
                help="Path to secure vault file", dest="vault_file", required=True)
        self.add_argument("--cipher-suite", action="store", type=str, \
                        dest="suite", required=True, help="Specify the cipher backend, one of {}".format(
                                    ", ".join(cipherfactory.CipherFactory.cipher_suites)))
        self.add_argument("--add-entry", type=str, help="Add a new record for secure storage into the vault")
        self.add_argument("--del-entry", type=str, help="Delete a record in the vault")
        self.add_argument("--modify-entry", type=str, help="Modify a record in the vault")
        self.add_argument("--search-vault", type=str, help="Query vault records for a search term")
        self.add_argument("--cipher-config-path", type=str, 
                help="Path to YAML-based parameter file", dest="cfg_path", required=False)