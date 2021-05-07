import re
import os
import stat
import argparse
import ciphers
import core.view
import core.util
import core.config

class CipherFactory():
    """Factory wrapper for dispatching appropriate
    cipher-based encryptor/decryptor
    """
    def __init__(self):
        self._enc = None
        self._dec = None
        self._parser_cfg = {}
        self._cipher_obj = None
        self._cipher_configured = False
        self._parser_configured = False
        self._cfg_obj = core.config.CipherConfig()

    def create_vault(self):
        """Vault creation helper method"""
        if "vault_file" not in self._parser_cfg:
            raise Exception("vault file not specified in CLI")
        vault_path = self._parser_cfg["vault_file"]
        if os.path.exists(vault_path):
            raise Exception("vault file already exists: {}".format(vault_path))
        elif not os.path.isabs(vault_path):
            core.util.safe_write(os.getcwd(), vault_path, self.encryptor.encrypt("[]"))
        else:
            core.util.safe_write("", vault_path, self.encryptor.encrypt("[]"))
        os.chmod(vault_path, 
            stat.S_IRUSR | stat.S_IWUSR | stat.S_ENFMT)
        self.update_cfg_file()

    def load_cmd_cfg(self, parse_obj: argparse.Namespace):
        """Maintains command line arguments"""
        self._parser_cfg = vars(parse_obj)
        self._parser_configured = True
        
    def load_param_cfg(self, config_obj: core.config.CipherConfig):
        """Maintains yaml config arguments"""
        if not self._parser_configured:
            raise Exception("Please provide CLI arguments into factory")
        elif not self._parser_cfg["create_vault"]:
            del self._cfg_obj
        self._cfg_obj = config_obj
        self._cipher_configured = True
    
    def is_requested(self, operation):
        return bool(self._parser_cfg[operation])

    def update_cfg_file(self):
        """Flushes new content into the config file"""
        cfg_attr = vars(self._enc)
        arg_params = {k[12:]:v for k,v in cfg_attr.items() 
                        if bool(re.match("_Encryptor__+", k))}
        cipher_params = {k[1:]:v for k,v in cfg_attr.items() 
                        if bool(re.match("_+", k)) and 
                        not bool(re.match("_Encryptor__+", k))}
        orig_cfg_path = self._parser_cfg.get('cfg_path') or 'cfg.yaml'
        cfg_filename = orig_cfg_path if not os.path.isabs(orig_cfg_path) \
                        else os.path.basename(orig_cfg_path)
        cfg_dirname = os.path.dirname(orig_cfg_path) \
                    if os.path.isabs(orig_cfg_path) else os.getcwd()
        final_path = self._cfg_obj.store(cfg_filename = cfg_filename,
                                cfg_dirname = cfg_dirname,
                                arg_params = arg_params,
                                cipher_params = cipher_params)
        view_obj = core.view.View()
        view_obj.print("updated cipher configuration flushed to: " + final_path)

    def _load_cipher_module(self):
        if not self._parser_configured:
            raise Exception("Please provide appropriate CLI configs")
        if self._cipher_obj is None:
            self._cipher_obj = __import__("ciphers.{}".format(self._parser_cfg['cipher_suite']), fromlist=[ciphers])

    @property
    def encryptor(self):
        """Returns an encryptor instance"""
        self._load_cipher_module()
        if self._enc is None:
            self._enc = self._cipher_obj.Encryptor(**self._cfg_obj())
            #self.update_cfg_file()
        return self._enc
    
    @property
    def decryptor(self):
        """Returns a decryptor instance"""
        self._load_cipher_module()
        if self._dec is None:
            self._dec = self._cipher_obj.Decryptor(**self._cfg_obj())
        return self._dec
