import os
import re
import glob
import string
import pkgutil
import ciphers
import tempfile

def is_valid_suite(suite_name):
        try:
            __import__("ciphers.{}".format(suite_name), fromlist=[ciphers])
            return True
        except ImportError:
            return False

def valid_encr_attr(attr):
    return attr[:12] == '_Encryptor__'

def safe_write(directory, name, content, overwrite=False):
        _name_prefix, _name_suffix = name.split(".")
        fd,  tmp_path = tempfile.mkstemp(
                        prefix = "{}_".format(_name_prefix),
                        suffix= ".{}".format(_name_suffix),
                        dir = directory
                    )
        with os.fdopen(fd, "wb") as tmp_file:
            tmp_file.write(content)
        _final_path = os.path.join(directory, name)
        if overwrite or not os.path.exists(_final_path):
            os.rename(tmp_path, _final_path)
        else:
            _final_path = tmp_path
        return _final_path

def join_path(parent_path, relative_path):
    return os.path.join(parent_path, relative_path)

def get_abs_path(relative_path):
    return join_path(os.getcwd(), relative_path)

def is_valid_file(abs_path):
    return os.path.exists(abs_path) and \
            os.path.isfile(abs_path)

def is_valid_dir(abs_path):
    return os.path.exists(abs_path) and \
            os.path.isdir(abs_path)

class CollectionMeta(type):
    """Metaclass for accrual of supported suites and models"""
    def __init__(cls, *args, **kwargs):
        pass

    @property
    def cipher_suites(self):
        cipher_modules = pkgutil.iter_modules(ciphers.__path__)
        cipher_names = map(lambda module: module.name, cipher_modules)
        return filter(lambda suite: suite[:6] != 'cipher', cipher_names)
    
    @property
    def model_collection(self):
        if not os.path.exists("models") or not os.path.isdir("models"):
            raise Exception("Please maintain models directory")
        return [ re.sub("models/|.json", "", mdl) for mdl in glob.glob("models/*")]

class Schema(type):
    """Metaclass for reserving the schema blueprint"""
    def __init__(self, *args, **kwargs):
        self._field = \
        """
        {
            "name": ${name},
            "type": ${type},
            "required": ${required}
        }
        """
        self._schema = \
        """
        {
            "Title": ${Title},
            "description": ${description},
            "fields": ${fields}
        }
        """
    
    @property
    def model_template(self):
        return string.Template(self._schema)

    @property
    def field_template(self):
        return string.Template(self._field)