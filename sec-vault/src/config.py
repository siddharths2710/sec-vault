import os
import yaml
import logging

import ciphers

class CipherConfig:
    def __init__(self, cfg_path):
        self._cfg = {}
        self._path = cfg_path
        if not os.path.isfile(cfg_path):
            raise Exception("cfg path not found: {}".format(cfg_path))

    def _is_valid_suite(self, suite_name):
        try:
            __import__("ciphers.{}".format(suite_name), fromlist=[ciphers])
            return True
        except ImportError:
            return False

    def _gen_call_params(self, arg):
        _call_params = ("=".join(item) for item in \
                            self._cfg['argparam'][arg].items())
        _call_params = ",".join(_call_params)
        _call_params = _call_params.replace('=',"='").replace(",","',")
        _call_params = _call_params + "'"
        return _call_params

    def _is_valid_argparam(self, cipher, arg):
        if 'argparam' not in self._cfg: return True
        elif arg not in self._cfg['argparam']: return True
        try:
            arg_module = cipher.CIPHER_PKG[arg]
            method_params = self._gen_call_params(arg)
            obj=eval("arg_module.{}({})".format(
                            self._cfg['args'][arg], method_params))
            return True
        except:
            logging.error("invalid params {} configured for arg {}".format(
                        str(self._cfg['argparam'][arg]), arg),exc_info=True)

    def _is_valid_args(self):
        if 'args' not in self._cfg: return True
        cipher = importlib.import_module(
                        ".{}".format(self._cfg["cipher_suite"]), 
                        package="ciphers"
                        )
        for arg in self._cfg['args']:
            if self._cfg['args'][arg] not in cipher.CIPHER_SUITE[arg]:
                logging.error('{} not found in {} suite'.format(
                                    self._cfg['args'][arg], arg
                            ))
                return False
            elif not self._is_valid_argparam(cipher, arg):
                logging.error('Invalid params provided for arg:', arg)
                return False
        return True

    def load(self):
        with open(self._path) as cfg_file:
            self._cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        if 'cipher_suite' not in self._cfg:
            self._cfg['cipher_suite'] = 'crypto_backend'
        elif not self._is_valid_suite(self._cfg['cipher_suite']):
            raise Exception("unsupported cipher suite: {}".format(
                                        self._cfg['cipher_suite']))
        elif not self._is_valid_args():
            raise Exception(
                "Invalid arguments provided for cipher suite {}".format(
                    self._cfg['cipher_suite']))
        return self._cfg
