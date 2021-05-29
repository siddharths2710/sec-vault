import os
import re
import string
import shutil
import pkgutil
import tempfile
import ciphers

def is_valid_suite(suite_name: str):
        """Cipher suite validity checker

        :param  suite_name: Name of the cipher suite
        :type   suite_name: str
        :rtype: bool
        """
        try:
            __import__("ciphers.{}".format(suite_name), fromlist=[ciphers])
            return True
        except ImportError:
            return False

def valid_encr_attr(attr):
    """Filter for arg_param attributes for a cipher suite

    :param  attr: Argument field to be validated for a given cipher
    :type   attr: str
    :rtype: bool
    """
    return attr[:12] == '_Encryptor__'

def copy(src: str, dst: str):
    if os.path.isfile(src):
        shutil.copyfile(src, dst)
    else:
        shutil.copy(src, dst)

def safe_write(directory, name, content, overwrite=False):
        """Writes content in a temporary location and renames/overwrites the file accordingly

        :param  directory: The dir hosting the final file
        :type   directory: str
        :param  name: propogated name of the regular file
        :type   name: str
        :param  content: Data to be written onto the file
        :type   content: str
        :param  overwrite: Overwrite file if existing
        :type   overwrite: bool
        """
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
    """Abstracts file path concatenation

    :param  parent_path: The path housing the relative path
    :type   parent_path: str
    :param  relative_path: The current path referenced from the base location
    :type   relative_path: str
    :rtype: str
    """
    return os.path.join(parent_path, relative_path)

def get_abs_path(relative_path):
    """Abstracts absolute path
    
    :param  relative_path: The current path relative to a reference
    :type   relative_path: str
    :rtype: str
    """
    return join_path(os.path.abspath(__file__), relative_path)

def get_models_path():
    return join_path(
        os.path.dirname(os.path.abspath(__file__)), 
        "models")

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
        return [ re.sub("models/|.json", "", mdl) \
                for mdl in os.listdir(get_models_path())]

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
