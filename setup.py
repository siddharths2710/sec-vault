import json

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":
    cfg_file = open('config.json',)
    reqs_file = open('src/requirements.txt',)
    config = json.load(cfg_file)
    reqs = [req.strip() for req in reqs_file.readlines()]
    config["install_requires"] = reqs
    setup(**config)
    reqs_file.close()
    cfg_file.close()