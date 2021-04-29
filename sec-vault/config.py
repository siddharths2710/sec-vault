import os
import yaml
import logging

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
            logging.error("Invalid config file format", exc_info=True)
        return self._cfg
    
    def store(self, config: dict, cfg_path: str):
        """Template method for dumping config into yaml file
        """
        try:
            with open(cfg_path, 'w') as cfg_file:
                self._cfg = yaml.dump(cfg_file, sort_keys=True)
        except:
            logging.error("Invalid config file format", exc_info=True)