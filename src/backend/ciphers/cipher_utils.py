
def sanitize_attr(generic_interface):
    return filter(lambda method: method[0] != "_",
                  generic_interface)