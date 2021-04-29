import json
import record
import traceback
import ciphers.cipher

class Collection:
    """Houses a collection of records"""
    def __init__(self):
        self._data = []
        self._cur_id = 0
    
    def load_vault(self, vault_file: str, dec: ciphers.cipher.Decryptor):
        with open(vault_file, "r") as f_obj:
            res = dec.decrypt(f_obj.read())
            self._update_index(res)
            self._data.extend(json.loads(res))
    
    def get_collection(self, enc: ciphers.cipher.Encryptor):
        return enc.encrypt(json.dumps(self._data))

    def add_record(self, rcrd: record.Record):
        """Helper for record insertion
        
        :param record: The record object to insert
        :type Record
        """
        if self._cur_id + 1 in map(lambda record: record['record_id'], self._data):
            raise Exception("conflicting record ids present in collection")
        content = {
            "record_id": self._cur_id + 1,
            "record": rcrd
        }
        self._data.append(content)
        self._cur_id += 1

    def del_record(self, record_id):
        """Helper for record deletion
        
        :param record_id: The identifier of the record to delete
        :type int
        """
        tmp_id = self._data[record_id]['record_id']
        if tmp_id != record_id:
            try:
                tmp_id = [idx for idx, rcrd in 
                    enumerate(self._data) if record_id == rcrd['record_id']][0]
                self._data.remove(tmp_id)
            except Exception:
                raise Exception("Please enter valid record id")

    def modify_record(self, record_id, record):
        """Helper for record modification
        
        :param record_id: The identifier of the record to delete
        :type int
        
        :param record: The record object with modification
        :type Record
        """
        tmp_id = self._data[record_id]['record_id']
        if tmp_id != record_id:
            try:
                tmp_id = [idx for idx, rcrd in 
                    enumerate(self._data) if record_id == rcrd['record_id']][0]
                self._data[tmp_id]['record'] = record
            except Exception:
                raise Exception("Please enter valid record id")

    def modify_field(self, record_id, field, val):
        """Helper for field modification within a record
        
        :param record_id: The identifier of the record to delete
        :type int
        
        :param field: The field name within the record
        :type str

        :param value: The value of corresponding field
        :type str
        """
        tmp_id = self._data[record_id]['record_id']
        if tmp_id != record_id:
            try:
                tmp_id = [idx for idx, rcrd in 
                    enumerate(self._data) if record_id == rcrd['record_id']][0]
                if field not in self._data[tmp_id]:
                    raise Exception("{} not in record {}".format(field, tmp_id))
                self._data[tmp_id][field] = val
            except IndexError:
                raise Exception("Please enter valid record id")
            except Exception:
                traceback.print_exc()

    def _update_index(self, collection: list):
        if bool(self._cur_id):
            record_ids = set(map(lambda record: record['record_id'], collection))
            if bool(len(record_ids.intersection(set(range(1, self._cur_id + 1))))):
                raise Exception("Record id {} conflicts with another collection record".format(record_id))                   
            elif bool(len(record_ids - (set(range(min(record_ids), max(record_ids) + 1))))):
                raise Exception("Inconsistencies in record ids for the given collection")
            self._cur_id = max(self._cur_id, max(record_ids))
    
    def display(self):
        """Helper for displaying a collection"""
        view = view.View()
        view.print("Vault contents: ")
        view.print("--------------------")
        for record in self._data:
            view.print("Record id: ", record['record_id'])
            record['record'].display()