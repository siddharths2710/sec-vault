import json
import setuptools

"""sec-vault packaging for distribution"""
if __name__ == "__main__":
    readme_file = open("README.md", "r", encoding="utf-8")
    cfg_file = open('config.json',)
    reqs_file = open('sec_vault/requirements/base.txt',)
    config = json.load(cfg_file)
    config['long_description'] = readme_file.read()
    reqs = [req.strip() for req in reqs_file.readlines()]
    config["install_requires"] = reqs
    setuptools.setup(**config)
    reqs_file.close()
    cfg_file.close()
    readme_file.close()
