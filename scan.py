import json
import time

import scanner


print()
print('==========================================')
print('==========================================')
print('===                                    ===')
print('===   Serial Experiments LAN Scanner   ===')
print('===                                    ===')
print('==========================================')
print('==========================================')
print()

print('Scanning... Please wait...')

known_transmitters = scanner.scan()

print()
print('Scan complete. Found %i transmitter%s.' % (len(known_transmitters), '' if 1 == len(known_transmitters) else 's'))

for transmitter in known_transmitters:
    for service in transmitter[1]:
        time.sleep(0.2)
        print()
        print(service['name'])
        print('  Location:      http://%s:%i' % (transmitter[0], service['port']))
        print('  Description:   ' + service['desc'])

print()
