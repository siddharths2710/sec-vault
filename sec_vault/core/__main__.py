#! /usr/bin/env python3

import os
import sys
import logging
import traceback
import ciphers
import core.util
import core.view
import core.parser
import core.config
import core.record
import core.collection
import core.cipherfactory

def _show_params(vault_args, factory, **kwargs):
    view_obj = core.view.View()
    view_obj.print("------Supported parameter values for {}---------".format(vault_args.cipher_suite) )
    for param in factory.cipher_args:
        view_obj.print("{}: {}".format(param, ", ".join(factory.cipher_args[param])))

def _create_vault(factory, **kwargs):
    factory.create_vault()

def _populate_from_vault(vault_args, factory, **kwargs):
    c_obj = core.collection.Collection()
    if not os.path.exists(vault_args.vault_file):
        if vault_args.create_vault:
            factory.create_vault()
        else:
            logging.error("Unable to locate vault file {}".format(vault_args.vault_file))
            sys.exit(1)
    with open(vault_args.vault_file, 'rb') as f_obj:
        c_obj.load_vault(f_obj.read(), factory.decryptor)
    return c_obj

def _store_in_vault(c_obj: core.collection.Collection, vault_args, factory):
    if not os.path.exists(vault_args.vault_file):
        factory.create_vault()
    content = c_obj.get_collection(factory.encryptor)
    factory.update_cfg_file()
    vault_path = core.util.safe_write(os.getcwd(), vault_args.vault_file , content, vault_args.overwrite_vault)
    view_obj = core.view.View()
    view_obj.print("vault file residing in {}".format(vault_path))
    view_obj.print()
    
def _add_record_to_vault(vault_args, factory, **kwargs):    
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    record_type = vault_args.record_type
    if record_type is None:
        raise Exception("please provide a valid record type in CLI")
    rcrd = core.record.Record(record_type)
    rcrd.create_interactive()
    content_wrapper.add_record(rcrd)
    _store_in_vault(content_wrapper, vault_args, factory)

def _del_entry_from_vault(vault_args, factory, **kwargs):
    view_obj = core.view.View()
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    rcrd_id = view_obj.prompt_read("Enter the record id you wish to delete:")
    if not rcrd_id.isnumeric():
        raise Exception("Please enter a valid record id")
    content_wrapper.del_record(int(rcrd_id))
    _store_in_vault(content_wrapper, vault_args, factory)

def _modify_vault_entry(vault_args, factory, **kwargs):
    view_obj = core.view.View()
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    record_type = vault_args.record_type
    if record_type is None:
        raise Exception("please provide a valid record type in CLI")
    rcrd = core.record.Record(record_type)
    rcrd_id = view_obj.prompt_read("Enter id of the record you wish to modify:")
    if not rcrd_id.isnumeric():
        raise Exception("Please enter a valid record id")
    rcrd.create_interactive()
    content_wrapper.modify_record(int(rcrd_id), rcrd)
    _store_in_vault(content_wrapper, vault_args, factory)

def _modify_record_field(vault_args, factory, **kwargs):
    view_obj = core.view.View()
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    rcrd_id = view_obj.prompt_read("Enter id of the record you wish to modify:")
    if not rcrd_id.isnumeric():
        raise Exception("Please enter a valid record id")
    field = view_obj.prompt_read("Enter field of the record you wish to modify:")
    if not field.isalpha():
        raise Exception("Please enter a valid field")
    val = view_obj.prompt_read("Enter corresponding value for {}:".format(field))
    content_wrapper.modify_field(int(rcrd_id), field, val)
    _store_in_vault(content_wrapper, vault_args, factory)

def _display_vault(vault_args, factory, **kwargs):
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    content_wrapper.display()

def _search_vault(vault_args, factory, **kwargs):
    view_obj = core.view.View()
    content_wrapper = _populate_from_vault(vault_args, factory, **kwargs)
    rcrd_id = view_obj.prompt_read("Enter id of the record you wish to modify:")
    if not rcrd_id.isnumeric():
        raise Exception("Please enter a valid record id")
    rcrd = core.collection.get_record(int(rcrd_id))
    rcrd.display()

def _prepare_config(vault_args, cipher_config):
    cipher_config.overwrite = vault_args.overwrite_cfg
    if vault_args.cfg_path is not None:
            cipher_config.load(vault_args.cfg_path)
    elif vault_args.create_vault:
        vault_args.cfg_path = "cfg.yaml"
    else:
        logging.error("Please provide a cipher config file")
        sys.exit(1)

operation_callback = {
    "show_params": _show_params,
    "create_vault": _create_vault,
    "add_entry": _add_record_to_vault,
    "del_entry": _del_entry_from_vault,
    "modify_entry": _modify_vault_entry,
    "modify_field": _modify_record_field,
    "display_vault": _display_vault,
    "search_vault": _search_vault
}

def main():
    stage = os.environ.get("STAGE", "debug")
    vault_parser = core.parser.CLIParser()
    vault_args = vault_parser.parse_args()
    factory = core.cipherfactory.CipherFactory()
    cfg = core.config.CipherConfig()
    try:
        _prepare_config(vault_args, cfg)
        factory.load_cmd_cfg(vault_args)
        factory.load_param_cfg(cfg)
        for operation in operation_callback:
            if factory.is_requested(operation):
                operation_callback[operation](vault_args=vault_args, factory=factory, cfg=cfg)
    except Exception as e:
        if stage == "debug":
            traceback.print_exc()
        else:
            logging.error(e)

if __name__ == "__main__":
    main()
