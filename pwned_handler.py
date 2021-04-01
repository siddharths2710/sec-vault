class PwdHandler:
    def __init__(self):
        self._query_index = {}
        self._cache = []

    def _find_record(self, name_pattern):
        if name_pattern in self._query_index:
            return self._query_index[name_pattern]
        pattern = re.compile(name_pattern)
        locations = []
        for idx, record in enumerate(self._cache):
            if pattern.search(record['service']) is not None:
                locations.append(idx)
        self._query_index = locations
        return locations
    
    def get_entries(self, search_term):
        indexes = self._find_record(search_term)
        print("service\tlogin_id\tcredential")
        for idx in indexes:
            print("{service}\t{login_id}\t{credential}".format(**self._cache[idx]))

    def add_record(**pwd_record):
        svc_pattern = re.compile(svc_name)
        for pattern in self._query_index:
            if svc_pattern.search(pattern) is not None:
                self._query_index[pattern].append(len(self._cache))
            else:
                self._query_index[pattern] = len(self._cache)
        self._cache.append(pwd_record)
    
    def update_record(**pwd_record):
        if pwd_record['service_name'] in self._query_index:
            for idx in self._query_index[pwd_record['service_name']]:
                _oldentry = self._cache[idx][:]
                self._cache[idx] = pwd_record

class PwdFileHandler(PwdHandler):
    def __init__(self, file_path):
        super(PwdFileHandler, self).__init__()
        self._file_path = file_path
        
    def __build_cache(self):
        with open(self._file_path, 'r') as pwd_file:
            pwd_reader = csv.DictReader(pwd_file)
            self._cache = list(pwd_reader)
            self._query_index.update({ 
                                        record['service']: idx 
                                        for idx, record in 
                                        enumerate(self._cache) 
                                    })
        
    def save_file(self):
        fd, tmp_path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, 'w+') as tmp_file:
            fields = ["service","login_id","credential"]
            writer = csv.DictWriter(tmp_file, fieldnames=fields)
            writer.writeheader()
            for entry in self._cache:
                writer.writerow(entry)