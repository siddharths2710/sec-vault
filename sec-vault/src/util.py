import os
import pkgutil
import tempfile

import ciphers

def valid_encr_attr(attr):
    return attr[:12] == '_Encryptor__'

def safe_write(directory, name, content):
        fd,  tmp_path = tempfile.mkstemp(
                        prefix = "{}_".format(name),
                        dir = directory
                    )
        with os.fdopen(fd, "w") as tmp_file:
            tmp_file.write(content)
        final_path = os.path.join(directory, name)
        if not os.path.isfile(final_path):
            os.rename(tmp_file, final_path)
        else:
            final_path = tmp_path
        return final_path

class CipherMeta(type):
    def __init__(cls, *args, **kwargs):
        pass

    @property
    def cipher_suites(self):
        cipher_modules = pkgutil.iter_modules(ciphers.__path__)
        cipher_names = map(lambda module: module.name, cipher_modules)
        return filter(lambda suite: suite[:6] != 'cipher', cipher_names)