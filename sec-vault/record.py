import json
import view
import model

class Record:
    """Wrapper for an individual record maintained in the vault file"""
    def __init__(self, model_type: str):
        self._model_type = model_type
        self._model = model.Model(model_type)
        self._content = {}
    
    def load(self, content):
        """Populates record content from existing data"""
        if self._model.validate_record(content):
            self._content = content
        else:
            raise Exception("the record obtained is invalid")
    
    def create_interactive(self):
        """Populates record content interactively via end user"""
        if bool(self._content):
            raise Exception("creating record: content already exists")
        view_obj = view.View()
        view_obj.print("Please enter your details associated with", self._model_type)
        for field in self._model.get_fields():
            self._content[field['name']] = view_obj.prompt_read(field['name'])
        if not self._model.validate_record(self._content):
            raise Exception("details entered for the given record are invalid")
    
    def display(self):
        """Displays contents of a record"""
        view_obj = view.View()
        for field in self._content:
            view_obj.print("\t {} : {}", field, self._content[field])