#! /usr/bin/env python3
import string
import random

def gen_random_secret(secret_length: int):
    return "".join([random.choice(string.ascii_letters + string.digits) for i in range(secret_length)]).encode('utf-8')

def _sanitize_attr(generic_attrs):
    return filter(lambda method: method[0] != "_",
                  generic_attrs)

def expand_attrs(generic_interface):
    return list(_sanitize_attr(dir(generic_interface)))
