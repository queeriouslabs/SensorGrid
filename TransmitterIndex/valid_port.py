import re


def valid_port(p):
    m = re.match('\\d+', p)
    return m is not None and int(p) in range(1024, 65536)
