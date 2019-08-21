import json
import time

from scanner import run_scanner


print()
print('==========================================')
print('==========================================')
print('===                                    ===')
print('===   Serial Experiments LAN Scanner   ===')
print('===                                    ===')
print('==========================================')
print('==========================================')
print()


def printer(x): print(x)


run_scanner(printer)
