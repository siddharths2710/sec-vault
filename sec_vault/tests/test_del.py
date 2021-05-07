import os
import core.util
import core.config
import core.parser
import core.record
import core.cipherfactory
import core.collection

def pending_test_del():
    p=core.parser.CLIParser()
    a=p.parse_args(["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend", "--cipher-config-path", "cfg.yaml", "--record-type", "login", "--del-entry"])
    cfac=core.cipherfactory.CipherFactory()
    cfg = core.config.CipherConfig()
    cfg.load(a.cfg_path)
    cfac.load_cmd_cfg(a)
    cfac.load_param_cfg(cfg)
    c_obj = core.collection.Collection()
    with open(a.vault_file, 'rb') as f_obj:
        c_obj.load_vault(f_obj.read(), cfac.decryptor)
    rcrd_id = '1'
    if not rcrd_id.isnumeric():
        raise Exception("Please enter a valid record id")
    c_obj.del_record(int(rcrd_id))
    content = c_obj.get_collection(cfac.encryptor)
    cfac.update_cfg_file()
    core.util.safe_write(os.getcwd(), a.vault_file , content)
