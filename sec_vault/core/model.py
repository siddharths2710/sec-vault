import os
import json
import glob
import logging
import traceback
import core.util

class Model(metaclass=core.util.Schema):
    """Represents a data model for a credential record"""
    def __init__(self, model, is_path=False):
        """Initializes a model object for the given schema"""
        self._schema = {}
        self._types = {"int", "float", "str"}
        self.schema_file = core.util.join_path(
                    core.util.get_models_path(), "{}.json".format(model)) \
                    if not is_path else model
        if not ( is_path or core.util.is_valid_dir(core.util.get_models_path())):
            raise Exception("unable to access schema directory")

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
        if not core.util.is_valid_file(self.schema_file):
            raise Exception("schema file {} invalid".format(self.schema_file))
        try:
            with open(self.schema_file, 'r') as file_obj:
                self._schema = self._validate_schema(json.load(file_obj))
        except json.decoder.JSONDecodeError:
            raise Exception("invalid json format: " + 
                            self.schema_file)
        except Exception:
            traceback.print_exc()
    def store(self):
        model_name = os.path.splitext(os.path.basename(self.schema_file))[0]
        final_path = core.util.join_path(core.util.get_models_path(), 
                                        "{}.json".format(model_name))
        core.util.copy(self.schema_file, final_path)
    
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
