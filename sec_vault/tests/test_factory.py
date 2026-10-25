import os
import pytest
import glob
import yaml

import core.view
import core.parser
import core.collection
import core.cipherfactory
import core.config
import core.__main__ as sec_vault_main

@pytest.fixture
def create_args():
    return ["--vault-file", "sec.vault", "--cipher-suite", "crypto_backend",  "--record-type", "login", "--create-vault", "--overwrite-cfg"]

def test_create_vault(create_args):
    p = core.parser.CLIParser()
    args = p.parse_args(create_args)
    c = core.cipherfactory.CipherFactory()
    c.load_cmd_cfg(parse_obj=args)
    c.create_vault()
    assert os.path.exists("sec.vault")
    os.unlink("sec.vault")
    os.unlink(glob.glob("cfg*.yaml")[0])

def _load_config(cfg_path):
    cfg = core.config.CipherConfig()
    cfg.load(cfg_path)
    return cfg

def test_pqcrypto_vault_roundtrip(tmp_path, monkeypatch, mocker):
    """Vault created with post-quantum keys stays readable across runs"""
    monkeypatch.chdir(tmp_path)
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.dump({"arg_params": {"encoding": "utf-8"}}))
    vault_args = ["--vault-file", "sec.vault", "--cipher-suite", "pqcrypto",
                  "--cipher-config-path", "cfg.yaml", "--record-type", "login"]

    create_args = core.parser.CLIParser().parse_args(
        vault_args + ["--create-vault", "--overwrite-cfg"])
    factory = core.cipherfactory.CipherFactory()
    factory.load_cmd_cfg(parse_obj=create_args)
    factory.load_param_cfg(_load_config(create_args.cfg_path))
    factory.create_vault()
    assert os.path.exists("sec.vault")
    flushed = yaml.safe_load(cfg_path.read_text())["arg_params"]
    assert {"mlkem_private_key", "x25519_private_key", "mldsa_private_key"} \
        <= set(flushed)

    add_args = core.parser.CLIParser().parse_args(
        vault_args + ["--add-entry", "--overwrite-cfg", "--overwrite-vault"])
    add_factory = core.cipherfactory.CipherFactory()
    add_factory.load_cmd_cfg(parse_obj=add_args)
    add_factory.load_param_cfg(_load_config(add_args.cfg_path))
    mocker.patch.object(core.view.View, "prompt_read", return_value="test-value")
    sec_vault_main._add_record_to_vault(vault_args=add_args, factory=add_factory)

    read_args = core.parser.CLIParser().parse_args(
        vault_args + ["--display-vault"])
    read_factory = core.cipherfactory.CipherFactory()
    read_factory.load_cmd_cfg(parse_obj=read_args)
    read_factory.load_param_cfg(_load_config(read_args.cfg_path))
    collection = core.collection.Collection()
    with open(read_args.vault_file, "rb") as vault_file:
        collection.load_vault(vault_file.read(), read_factory.decryptor)
    assert collection._data[0]["record"]["user_name"] == "test-value"
