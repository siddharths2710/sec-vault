class View:
    """Wrapper for the stdout messages directed to the end-user"""
    def prompt_read(self, field):
        return input("Enter the {}: ".format(field))
    
    def print(self, *args, **kwargs):
        print(*args, sep=" ", end="\r\n", **kwargs)