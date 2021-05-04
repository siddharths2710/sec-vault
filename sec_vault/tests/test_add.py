import os
import pytest
import core.util
import core.config
import core.parser
import core.record
import core.cipherfactory
import core.collection

p=core.parser.CLIParser()
a=p.parse_args(["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend", "--cipher-config-path", "cfg.yaml", "--record-type", "identity", "--add-entry"])

@pytest.fixture
def credential_data():
    return {
        "first_name": "test",
    "middle_name": "middle",
    "last_name": "name",
    "title": "sometitle",
    "nick_name": "test",
    "SSN": "3554534677",
    "passport_number": "O2335512",
    "license_number": "QP44623A3",
    "phone": "303-515-616",
    "email": "a@b.com",
    "address": "sad",
    "city": "ad",
    "province": "e",
    "zip": "fe",
    "country": "eds",
    "company": "s",
    "designation": "c",
    "website": "",
    "handle": ""
}

def pending_test_add_and_retrieve():
    cfac=core.cipherfactory.CipherFactory()
    cfg = core.config.CipherConfig()
    #cfg.load(a.cfg_path)
    #cfac.load_cmd_cfg(a)
    cfac.load_param_cfg(cfg)
    c_obj = core.collection.Collection()
    with open(a.vault_file, 'rb') as f_obj:
        c_obj.load_vault(f_obj.read(), cfac.decryptor)
    c_obj.display()
    rcrd = record.Record(a.record_type)
    rcrd._content = identity_data
    c_obj.add_record(rcrd)
    content = c_obj.get_collection(cfac.encryptor)
    cfac.update_cfg_file()
    util.safe_write(os.getcwd(), a.vault_file , content)
