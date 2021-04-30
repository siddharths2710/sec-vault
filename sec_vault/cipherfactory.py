import re
import os
import csv
import stat
import copy
import util
import config
import base64
import pkgutil
import tempfile

import view
import ciphers
import ciphers.cipher
import ciphers.cipher_utils

class CipherMeta(type):
    """Metaclass for accrual of supported suites"""
    def __init__(cls, *args, **kwargs):
        pass

    @property
    def cipher_suites(self):
        cipher_modules = pkgutil.iter_modules(ciphers.__path__)
        cipher_names = map(lambda module: module.name, cipher_modules)
        return filter(lambda suite: suite[:6] != 'cipher', cipher_names)

class CipherFactory(metaclass=CipherMeta):
    """Factory wrapper for dispatching appropriate
    cipher-based encryptor/decryptor
    """
    def __init__(self):
        self._cipher_configured = False
        self._parser_configured = False
        self._parser_cfg = {}
        self._cipher_cfg = config.CipherConfig()

    def create_vault(self):
        """Vault creation helper method"""
        if "vault_file" not in self._parser_cfg:
            raise Exception("vault file not specified in CLI")
        vault_path = self._parser_cfg["vault_file"]
        elif not os.path.exists(vault_path):
            raise Exception("vault file already exists: {}".format(vault_path))
        elif not os.path.isabs(vault_path):
            util.safe_write(os.getcwd(), vault_path, factory.encryptor.encrypt("[]"))
        else:
            util.safe_write("", vault_path, factory.encryptor.encrypt("[]"))
        os.chmod(vault_path, 
            stat.S_IRUSR | stat.S_IWUSR | stat.S_ENFMT)

    def load_cmd_cfg(self, parse_obj):
        """Maintains command line arguments"""
        self._parser_cfg = vars(parse_obj)
        self._parser_configured = True
        
    def load_param_cfg(self, yaml_obj):
        """Maintains yaml config arguments"""
        if not self._parser_configured:
            raise Exception("Please provide CLI arguments into factory")
        elif not self._parser_cfg["create_vault"]:
            self._cipher_cfg.load(self._parser_cfg["cfg_path"])
            self._cipher_configured = True
    
    def is_requested(self, operation):
        return bool(self._parser_cfg[operation])

    def _update_cfg_file(self):
        """Flushes new content into the config file"""
        cfg_attr = vars(self.encryptor)
        arg_params = {k:v for k,v in cfg_attr.items() 
                        if bool(re.match("_Encryptor__+", k))}
        cipher_params = {k:v for k,v in cfg_attr.items() 
                        if bool(re.match("_+", k)) and 
                        k not in arg_params}
        orig_cfg_path = self._parser_cfg['cfg_path']
        cfg_filename = os.path.basename(orig_cfg_path)
        cfg_dirname = os.path.dirname(orig_cfg_path) \
                    if os.path.isabs(orig_cfg_path) else os.getcwd()
        final_path = self._cipher_cfg.store(cfg_filename = cfg_filename,
                                cfg_dirname = cfg_dirname,
                                arg_params = arg_params,
                                cipher_params = cipher_params)
        view_obj = view.View()
        view_obj.print("updated cipher configuration flushed to: " + final_path)

    @property
    def encryptor(self):
        """Returns an encryptor instance"""
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")
        if self._parser_cfg["create_vault"]:
            self._update_cfg_file()
    
    @property
    def decryptor(self):
        """Returns a decryptor instance"""
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")