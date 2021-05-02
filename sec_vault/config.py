import os
import re
import yaml
import logging
import tempfile

import ciphers

class CipherConfig:
    """Wrapper for handling yaml-based parameter configs
    """
    def __init__(self):
        """Propagate config path parameter and default cfg object

        :param cfg_path: Absolute path of YAML config
        :type str
        """
        self._cfg = {}
        self._overwrite_cfg = False

    def load(self, cfg_path):
        """Template method for loading yaml file

        :returns config object associated with cfg_path
        :returntype dict
        """
        if not os.path.isfile(cfg_path):
            raise Exception("unable to find cfg path for loading: {}".format(cfg_path))
        try:
            with open(cfg_path, 'r') as cfg_file:
                cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
                for param in cfg:
                    self._cfg[param] = {}
                    for key in cfg[param]:
                        if re.match("^.+_bytes$", key) is not None:
                            self._cfg[param][key[:-6]] = cfg[param][key].encode('utf-8')
                        else:
                            self._cfg[param][key] = cfg[param][key]
        except:
            raise Exception("Invalid config file format")
    
    def __call__(self):
        return self._cfg
    
    def _update_cfg(self, config):
        config_serial = {}
        for param in config:
            param_serial = {}
            for field in config[param]:
                if isinstance(config[param][field], bytes):
                    param_serial["{}_bytes".format(field)] = config[param][field].decode('utf-8')
                elif isinstance(config[param][field], int) or \
                     isinstance(config[param][field], float) or \
                     isinstance(config[param][field], str):
                    param_serial[field] = config[param][field]
            config_serial[param] = param_serial
        self._cfg.update(config_serial)
        
    def store(self, cfg_filename, cfg_dirname, **config):
        """Template method for dumping config into yaml file
        """
        _name_prefix, _name_suffix = cfg_filename.rsplit(".")
        self._update_cfg(config)
        cfg_fd, cfg_path = tempfile.mkstemp(
             prefix = _name_prefix + "_", suffix= "." + _name_suffix,
             dir = cfg_dirname, text = True
             )
        try:
            with os.fdopen(cfg_fd, 'w') as cfg_file:
                yaml.dump(self._cfg, cfg_file)
            
            if self.overwrite:
                orig_cfg_path = os.path.join(cfg_dirname, cfg_filename)
                os.rename(cfg_path, orig_cfg_path)
                cfg_path = orig_cfg_path

            return cfg_path
        except:
            raise Exception("Invalid config file format")
    
    @property
    def overwrite(self):
        return self._overwrite_cfg
    
    @overwrite.setter
    def overwrite(self, val):
        if isinstance(val, bool):
            self._overwrite_cfg = val
        else:
            raise Exception("Invalid cfg overwrite option")