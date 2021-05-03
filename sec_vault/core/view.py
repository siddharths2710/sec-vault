class View:
    """Wrapper for the stdout messages directed to the end-user"""
    def prompt_read(self, field):
        return input("Enter the {}: ".format(field))
    
    def print(self, *args, **kwargs):
        print(*args, sep=" ", end="\r\n", **kwargs)
    
    def tabulate(self, *args):
        if len(args) < 2:
            print(args)
        mid_len = len(args) - 2
        fmt="{left}{mid}{right}".format(left="{:<8}\t", mid=" {} "* mid_len, right="\t{:>10}")
        print(fmt.format(*args))