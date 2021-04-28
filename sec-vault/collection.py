import json
import record
import cipherfactory

class Collection:
    """Houses a collection of records"""
    def __init__(self):
        self._data = []
        self._cur_id = 0
    
    def from_vault(self, vault_file: str, factory: cipherfactory.CipherFactory):
        dec = factory.decryptor()
        with open(vault_file, "r") as f_obj:
            res = dec.decrypt(f_obj.read())
            self._update_index(res)
            self._data.extend(res)
    
    def add_record(rcrd: record.Record):
        if self._cur_id + 1 in map(lambda record: record['record_id'], self._data):
            raise Exception("conflicting record ids present in collection")
        content = {
            "record_id": self._cur_id + 1,
            "record": rcrd
        }
        self._data.append(content)
        self._cur_id += 1

    def _update_index(self, collection: list):
        if bool(self._cur_id):
            record_ids = set(map(lambda record: record['record_id'], collection))
            if bool(len(record_ids.intersection(set(range(1, self._cur_id + 1))))):
                raise Exception("Record id {} conflicts with another collection record".format(record_id))                   
            elif bool(len(record_ids - (set(range(min(record_ids), max(record_ids) + 1))))):
                raise Exception("Inconsistencies in record ids for the given collection")
            self._cur_id = max(self._cur_id, max(record_ids))