#! /usr/bin/env python3

import util
import parser
import config
import ciphers
import traceback
import cipherfactory

vault_parser = parser.CLIParser()
factory = cipherfactory.CipherFactory()
cfg = config.CipherConfig(vault_args.cfg_file)
vault_args = vault_parser.parse_args()
cfg_data = {}

operation_callback = {
    "create_vault": _create_vault,
    "add_entry": _add_entry_to_vault,
    "del_entry": _del_entry_from_vault,
    "modify_entry": _modify_vault_entry,
    "display_vault": _display_vault,
    "search_vault": _search_vault
}

def _create_vault():
    pass

def _add_entry_to_vault():
    pass

def _del_entry_from_vault():
    pass

def _modify_vault_entry():
    pass

def _display_vault():
    pass

def _search_vault():
    pass

if __name__ == "__main__":
    if vault_args.cfg_file is not None:
        cfg_data = cfg.load()
    factory.load_cmd_cfg(parser)
    factory.load_param_cfg(cfg_data)
    try:
        for operation in operation_callback:
            if factory.is_requested(operation):
                operation_callback[operation]()
    except Exception:
        traceback.print_exc()