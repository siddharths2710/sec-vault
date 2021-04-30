import os
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

    def load(self, cfg_path):
        """Template method for loading yaml file

        :returns config object associated with cfg_path
        :returntype dict
        """
        if not os.path.isfile(cfg_path):
            raise Exception("unable to find cfg path for loading: {}".format(cfg_path))
        try:
            with open(cfg_path, 'r') as cfg_file:
                self._cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        except:
            raise Exception("Invalid config file format")
        return self._cfg
        
    def store(self, cfg_filename, cfg_dirname, **config):
        """Template method for dumping config into yaml file
        """
        cfg_fd, cfg_path = tempfile.mkstemp(
             prefix = cfg_filename + "_", dir = cfg_dirname, 
             text = True
             )
        try:
            with os.fdopen(cfg_fd, 'w') as cfg_file:
                yaml.dump(config, cfg_file)
            return cfg_path
        except:
            raise Exception("Invalid config file format")