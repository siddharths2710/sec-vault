#! /usr/bin/env python3

def _sanitize_attr(generic_attrs):
    return filter(lambda method: method[0] != "_",
                  generic_attrs)

def expand_attrs(generic_interface):
    return list(_sanitize_attr(dir(generic_interface)))
