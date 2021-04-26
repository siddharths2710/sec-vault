import json
import glob
import util
import string

class Schema(type):
    """Metaclass for reserving schema blueprint
    """
    def __init__(cls, *args, **kwargs):
        self._field = \
        """
        {
            "name": ${name},
            "type": ${type},
            "required": ${required}
        }
        """
        self._model = \
        """
        {
            "$schema": $$schema,
            "$id": $$id,
            "Title": ${Title},
            "description": ${description},
            "fields": ${fields}
        }
        """
    
    @property
    def model_template(self):
        return string.Template(self._model)

    @property
    def field_template(self):
        return string.Template(self._field)

class Model:
    """Represents a data model for a credential record
    """
    def __init__(self, model):
        """Initializes a model object for the given schema
        """
        self._model = {}
        self.schema_file = util.get_abs_path(
                            util.join_path("models", 
                            "{}.json".format(model)))      
        self._load()
    
    def _load(self):
        if not util.is_valid_dir(util.get_abs_path("models")):
            raise Exception("unable to access schema directory")
        elif not util.is_valid_file(self.schema_file):
            raise Exception("schema file {} invalid".format(self.schema_file))
        try:
            self._model = self._validate_model(json.load(self.schema_file))
            return self._model
        except json.decoder.JSONDecodeError:
            raise Exception("invalid json format: " + 
                            self.schema_file)
        except Exception:
            traceback.print_exc()


    def _validate_model(self, schema):
        """Validator method for a chosen schema
        """
        try:
            model_val = self.model_template.substitute(**schema)
            for field in schema['fields']:
                field_val = self.field_template.substitute(**field)
            return schema
        except Exception:
            raise Exception("Invalid schema format provided")
