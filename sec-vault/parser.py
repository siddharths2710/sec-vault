import logging
import ciphers
import pkgutil
import argparse

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
                        dest="cipher_suite", required=True, help="Specify the cipher backend, one of {}".format(
                                    ", ".join(cipherfactory.CipherFactory.cipher_suites)))
        self.add_argument("--add-entry", action="store_true", help="Add a new record for secure storage into the vault")
        self.add_argument("--del-entry", action="store_true", help="Delete a record in the vault")
        self.add_argument("--modify-entry", action="store_true", help="Modify a record in the vault")
        self.add_argument("--modify-field", action="store_true", help="Modify a field of a record in the vault")
        self.add_argument("--display-vault", action="store_true", help="View entire vault contents")
        self.add_argument("--search-vault", action="store_true", help="Query vault records for a search term")
        self.add_argument('--record-type', action="store", type=str, \
                        dest="record_type", required=True, 
                        help="Specify the record type, one of" + ", ".join(model.Model.get_models()))
        self.add_argument("--cipher-config-path", type=str, 
                help="Path to YAML-based parameter file", dest="cfg_path", required=False)