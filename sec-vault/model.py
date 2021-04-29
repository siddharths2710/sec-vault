import json
import glob
import util
import string
import logging
import traceback

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

class Model(metaclass=Schema):
    """Represents a data model for a credential record"""
    def __init__(self, model):
        """Initializes a model object for the given schema"""
        self._schema = {}
        self._types = {"int", "float", "str"}
        self.schema_file = util.get_abs_path(
                            util.join_path("models", 
                            "{}.json".format(model)))
        if not util.is_valid_dir(util.get_abs_path("models")):
            raise Exception("unable to access schema directory")
    
    @staticmethod
    def get_models():
        if not os.path.exists("models") or not os.path.isdir("models"):
            raise Exception("Please maintain models directory")
        return [ re.sub("models/|.json", mdl) for mdl in glob.glob("models/*")]

    def _validate_schema(self, schema):
        """Validator method for a chosen schema"""
        try:
            model_val = Model.model_template.substitute(**schema)
            for field in schema['fields']:
                field_val = Model.field_template.substitute(**field)
                if field['type'] not in self._types:
                    raise Exception("invalid field type: {}".format(field['type']))
            return schema
        except Exception:
            raise Exception("Invalid schema format provided")

    def load(self):
        """Loads model from schema file"""
        if not util.is_valid_file(self.schema_file):
            raise Exception("schema file {} invalid".format(self.schema_file))
        try:
            with open(self.schema_file, 'r') as file_obj:
                self._schema = self._validate_schema(json.load(file_obj))
        except json.decoder.JSONDecodeError:
            raise Exception("invalid json format: " + 
                            self.schema_file)
        except Exception:
            traceback.print_exc()
    
    def get_fields(self):
        if not bool(self._schema):
            self.load()
        return self._schema['fields']
    
    def validate_record(self, content: dict):
        """Validator method for a given record

        :param record content
        :returntype bool
        """
        if not bool(self._schema):
            self.load()
        for field in self._schema['fields']:
            if field['name'] not in content:
                logging.error("required attribute missing: ", field['name'])
            elif not content[field['name']].isascii():
                logging.error(" value of {} is invalid".format(field['name']))
            try:
                res = eval("{}('{}')".format(field['type'], content[field['name']]))
                return True
            except Exception:
                logging.error("Invalid value for {}: {}".format(field['name'], content[field['name']]))
                return False