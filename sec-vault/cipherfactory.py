import re
import os
import csv
import stat
import copy
import util
import base64
import ciphers
import pkgutil
import logging
import tempfile

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
        self._yaml_configured = False
        self._parser_configured = False
        self._parser_cfg = {}

    def create_vault(self):
        if "vault_file" not in self._parser_cfg:
            raise Exception("cfg parser not loaded")
        vault_path = self._parser_cfg["vault_file"]
        elif not os.path.exists(vault_path):
            raise Exception("vault file already exists: {}".format(vault_path))
        elif not os.path.isabs(vault_path):
            util.safe_write(os.getcwd(), vault_path, "")
        else:
            util.safe_write("", vault_path, "")
        os.chmod(vault_path, 
            stat.S_IRUSR | stat.S_IWUSR | stat.S_ENFMT)

    def load_cmd_cfg(self, parse_obj):
        """Maintains command line arguments"""
        self._parser_cfg = vars(parse_obj)
        self._parser_configured = True
        
    def load_param_cfg(self, yaml_obj):
        """Maintains yaml config arguments"""
        self._yaml_configured = True
    
    def is_requested(self, operation):
        return self._parser_cfg[operation]

    @property
    def encryptor(self):
        """Returns an encryptor instance"""
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")
    
    @property
    def decryptor(self):
        """Returns a decryptor instance"""
        if not self._parser_configured or 'decrypt' not in self._cfg:
            raise Exception("Please provide appropriate CLI configs")