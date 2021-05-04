import os
import util
import config
import parser
import record
import cipherfactory
import collection
p=parser.CLIParser()
a=p.parse_args(["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend", "--cipher-config-path", "cfg.yaml", "--record-type", "bank_card", "--add-entry"])
cfac=cipherfactory.CipherFactory()
cfg = config.CipherConfig()
cfg.load(a.cfg_path)
cfac.load_cmd_cfg(a)
cfac.load_param_cfg(cfg)
c_obj = collection.Collection()
with open(a.vault_file, 'rb') as f_obj:
    c_obj.load_vault(f_obj.read(), cfac.decryptor)
c_obj.display()
rcrd = record.Record(a.record_type)
rcrd.create_interactive()
c_obj.add_record(rcrd)
content = c_obj.get_collection(cfac.encryptor)
cfac.update_cfg_file()
util.safe_write(os.getcwd(), a.vault_file , content)