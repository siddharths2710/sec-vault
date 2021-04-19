import re
import csv
import copy
import util
import base64
import logging
import tempfile
import pwdzipfile


class CipherFactory(metaclass=util.CipherMeta):
    def __init__(self):
        self._yaml_configured = False
        self._parser_configured = False
        self._kwargs = {}

    def load_parser_cfg(self, parse_obj):
        self._parser_configured = True
        
    def load_yaml_cfg(self, yaml_obj):
        self._yaml_configured = True

    @property
    def encryptor(self):
        if not ( self._parser_configured or self._yaml_configured):
            raise Exception("Please provide cipher parameter configs")
    
    @property
    def decryptor(self):
        if not ( self._parser_configured or self._yaml_configured):
            raise Exception("Please provide cipher parameter configs")