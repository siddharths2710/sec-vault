import json
import core.view
import core.model

class Record:
    """Wrapper for an individual record maintained in the vault file"""
    def __init__(self, model_type: str):
        self._model_type = model_type
        self._model = core.model.Model(model_type)
        self._content = {}
    
    def __call__(self):
        return self._content

    def load(self, content: dict):
        """Populates record content from existing data
        
        :param  content: Indexed record contents
        :type   content: dict
        """
        if self._model.validate_record(content):
            self._content = content
        else:
            raise Exception("the record obtained is invalid")
    
    def create_interactive(self):
        """Populates record content interactively via end user"""
        if bool(self._content):
            raise Exception("creating record: content already exists")
        view_obj = core.view.View()
        view_obj.print("Please enter your details associated with", self._model_type)
        for field in self._model.get_fields():
            self._content[field['name']] = view_obj.prompt_read(field['name'])
        if not self._model.validate_record(self._content):
            raise Exception("details entered for the given record are invalid")
    
    def display(self, mode="table", indent = 1):
        """Displays contents of a record
        
        :param  mode: The display format
        :type   mode: str (json, yaml, table)
        """
        view_obj = core.view.View()
        if mode == "json":
            view_obj.print(json.dumps(self._content, indent = indent))
        elif mode == "yaml":
            view_obj.print(yaml.dump(self._content, indent = indent))
        else:
            for field in self._content:
                view_obj.print("\t {} : {}", field, self._content[field])
    
    def modify_field(self, key: str, val: str):
        """Modifies content of the given field
        
        :param  key
        :type   key: str

        :param  val
        :type   val: str
        """
        if key not in self._content:
            raise Exception("field {} missing in record".format(key))
        self._content[key] = val
