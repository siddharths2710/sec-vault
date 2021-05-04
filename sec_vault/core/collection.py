import json
import yaml
import traceback
import core.view
import core.record
import ciphers.cipher

class Collection:
    """Houses a collection of records"""
    def __init__(self):
        self._data = []
        self._cur_id = 0
    
    def load_vault(self, vault_content: str, dec: ciphers.cipher.Decryptor):
        res = "[]"
        try:
            res = dec.decrypt(vault_content)
        except TypeError:
            res = dec.decrypt(str(vault_content)[2:-1])
        except Exception:
            traceback.print_exc()
        finally:
            res = res[: res.index("]") + 1]
            fetched_records = json.loads(res)
            self._update_index(fetched_records)
            self._data.extend(fetched_records)
    
    def get_collection(self, enc: ciphers.cipher.Encryptor):
        return enc.encrypt(json.dumps(self._data))

    def get_record(self, record_id: int):
        return self._data[self._calc_record_index(record_id)]

    def add_record(self, rcrd: core.record.Record):
        """Helper for record insertion
        
        :param record: The record object to insert
        :type Record
        """
        if self._cur_id + 1 in map(lambda record: record['record_id'], self._data):
            raise Exception("conflicting record ids present in collection")
        content = {
            "record_id": self._cur_id + 1,
            "record": rcrd()
        }
        self._data.append(content)
        self._cur_id += 1

    def del_record(self, record_id):
        """Helper for record deletion
        
        :param record_id: The identifier of the record to delete
        :type int
        """
        if len(self._data) <= record_id or self._data[record_id]['record_id'] != record_id:
            try:
                tmp_id = [idx for idx, rcrd in 
                    enumerate(self._data) if record_id == rcrd['record_id']][0]
            except Exception:
                raise Exception("Please enter valid record id")
        self._data.pop(tmp_id)

    def modify_record(self, record_id, record):
        """Helper for record modification
        
        :param record_id: The identifier of the record to delete
        :type int
        
        :param record: The record object with modification
        :type Record
        """
        res_id = self._calc_record_index(record_id)
        self._data[res_id]['record'] = record

    def modify_field(self, record_id, field, val):
        """Helper for field modification within a record
        
        :param record_id: The identifier of the record to delete
        :type int
        
        :param field: The field name within the record
        :type str

        :param value: The value of corresponding field
        :type str
        """
        res_id = self._calc_record_index(record_id)
        self._data[res_id]['record'].modify_field(field, val)

    def _calc_record_index(self, record_id):
        if self._data[record_id]['record_id'] != record_id:
            try:
                return [idx for idx, rcrd in 
                    enumerate(self._data) if record_id == rcrd['record_id']][0]
            except IndexError:
                raise Exception("Please enter valid record id")
            except Exception:
                traceback.print_exc()

    def _update_index(self, collection: list):
        if not bool(len(collection)):
            return
        record_ids = set(map(lambda record: record['record_id'], collection))
        if bool(len(record_ids.intersection(set(range(1, self._cur_id + 1))))):
            raise Exception("Record id {} conflicts with another collection record".format(record_id))                   
        elif bool(len(record_ids - (set(range(min(record_ids), max(record_ids) + 1))))):
            raise Exception("Inconsistencies in record ids for the given collection")
        self._cur_id = max(self._cur_id, max(record_ids))
    
    def display(self, mode="table", indent=1):
        """Helper for displaying a collection"""
        view_obj = core.view.View()
        view_obj.print()
        if mode == "json":
            view_obj.print(json.dumps(self._data, indent=indent))
        elif mode == "yaml":
            view_obj.print(yaml.dump(self._data, indent=indent))
        else:
            view_obj.print("============VAULT CONTENTS==================")
            for record in self._data:
                view_obj.print("#", record['record_id'])
                for field in record['record']:
                    view_obj.tabulate(field, record['record'][field])
                view_obj.print("--------------------------------------------")
