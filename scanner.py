import socket
import time
import sys
import re
import json
import time


socket.setdefaulttimeout(0.1)
scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = 'sel-syn'.encode('utf-8') 

start_time = time.time()
known_transmitters = []

try:
    sys.stdout.write('\nScanning')
    sys.stdout.flush()
    while time.time() < start_time + 10:
        sys.stdout.write('.')
        sys.stdout.flush()
        scanner.sendto(message, ('<broadcast>', 1337))
        for i in range(10):
            try:
                data, addr = scanner.recvfrom(1024)
                m = re.split('\s+', data.decode('utf-8'), 1)
                if m[0] == 'sel-ack':
                    known_transmitters += [(addr[0], json.loads(m[1]))]
            except socket.timeout: pass
except KeyboardInterrupt:
    print()
    print('Scan exiting early.')

print('\n')
print('Scan complete. Found %i transmitters:' % len(known_transmitters))

for transmitter in known_transmitters:
    for service in transmitter[1]:
        time.sleep(0.2)
        print()
        print('Name: ' + service['name'])
        print('Location: http://%s:%i' % (transmitter[0], service['port']))
        print('Description: ' + service['desc'])

print()
