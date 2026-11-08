import os
import core.config

def test_store_dotted_cfg_filename(tmp_path):
    cfg = core.config.CipherConfig()
    cfg.overwrite = True
    final_path = cfg.store("cfg.test.yaml", str(tmp_path),
                           arg_params={"encoding": "utf-8"},
                           cipher_params={})
    assert final_path == os.path.join(str(tmp_path), "cfg.test.yaml")
    loaded = core.config.CipherConfig()
    loaded.load(final_path)
    assert loaded()["arg_params"]["encoding"] == "utf-8"

def test_store_overwrites_existing_cfg(tmp_path):
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text("arg_params: {}\n")
    cfg = core.config.CipherConfig()
    cfg.overwrite = True
    final_path = cfg.store("cfg.yaml", str(tmp_path),
                           arg_params={"encoding": "utf-8"},
                           cipher_params={})
    assert final_path == str(cfg_path)
    assert "encoding" in cfg_path.read_text()
