import re
import csv
import copy
import util
import base64
import ciphers
import pkgutil
import logging
import tempfile

class CipherMeta(type):
    """Metaclass for accrual of supported suites
    """
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
        """
        """
        self._yaml_configured = False
        self._parser_configured = False
        self._kwargs = {}

    def load_cmd_cfg(self, parse_obj):
        self._parser_configured = True
        
    def load_param_cfg(self, yaml_obj):
        self._yaml_configured = True

    @property
    def encryptor(self):
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")
    
    @property
    def decryptor(self):
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")