import core.config
import core.parser
import core.cipherfactory
import core.collection

def pending_test_flow():
    p=parser.CLIParser()
    a=p.parse_args(["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend", "--cipher-config-path", "cfg.yaml", "--record-type", "login", "--display-vault"])
    cfac=cipherfactory.CipherFactory()
    cfg = config.CipherConfig()
    cfg.load(a.cfg_path)
    cfac.load_cmd_cfg(a)
    cfac.load_param_cfg(cfg)
    c_obj = collection.Collection()
    with open(a.vault_file, 'rb') as f_obj:
        c_obj.load_vault(f_obj.read(), cfac.decryptor)
    c_obj.display()
