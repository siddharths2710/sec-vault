import ciphers
import pkgutil
import argparse

class CLIParser(argparse.ArgumentParser):
    def __init__(self,*args, **kwargs):
        super(self, CLIParser).__init__(prog='sec-vault', description='Password management CLI tool', fromfile_prefix_chars='@')
        self._suite_parsers = self.add_subparsers()
        self._add_args()
        self._add_cipher_args()

    def _add_cipher_args(self):
        cipher_modules = pkgutil.iter_modules(ciphers.__path__)
        cipher_names = map(lambda module: module.name, cipher_modules)
        cipher_suites = filter(lambda suite: suite not in 'cipher', 'cipher_utils', cipher_names)
        for suite_name in cipher_suites:
            cipher = __import__("ciphers.{}".format(suite_name), fromlist=[ciphers])
            cipher_parser = self._suite_parsers.add_parser("--{}".format(suite_name),
                                                            type=bool, dest=suite_name)
            try:
                for suite_arg in cipher.CIPHER_SUITE:
                    cipher_parser.add_argument( "--{}".format(suite_arg), 
                            dest=suite_arg, help="Supported values are: {}".format(
                                ",".join(cipher.CIPHER_SUITE[suite_arg])), required=False)
            except:
                if "CIPHER_SUITE" not in dir(cipher):
                    logging.debug("no arguments and parameters required for ", suite_name)
                else:
                    logging.error("Argument parser error", exc_info=True)

    def _add_args(self):
        self.add_argument("-create", "--create-vault", action="store_true", type=bool, help="Create Vault file", dest="encrypt", required=False)
        self.add_argument("-add", "--add-entry", type=str, help="Add a new record for secure storage into the vault")
        self.add_argument("-del", "--del-entry", type=str, help="Delete a record in the vault")
        self.add_argument("-update", "--modify-entry", type=str, help="Modify a record in the vault")
        self.add_argument("-encr", "--encrypt", action="store_false", type=bool, help="Perform Vault encryption operation", dest="encrypt", required=False)
        self.add_argument("-decr", "--decrypt", action="store_false", type=bool, help="Perform Vault decryption operation", dest="decrypt", required=False)
        self.add_argument("-cfg", "--config-file", type=str, 
                help="Path to YAML-based config file", dest="cfg_path", required=False)
        #self.add_argument("-suite","--cipher-suite", action="store", type=str, \
        #                    help="Specify the cipher backend, one of" \
        #                    ",".join(self._get_cipher_suites()))
