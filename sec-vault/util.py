import os
import ciphers
import tempfile
import cipherfactory

def is_valid_suite(self, suite_name):
        try:
            __import__("ciphers.{}".format(suite_name), fromlist=[ciphers])
            return True
        except ImportError:
            return False

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