import socket
import time
import sys

socket.setdefaulttimeout(1)
scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = 'sensorgrid-scanner-syn'.encode('utf-8') 

start_time = time.time()
known_transmitters = []

try:
    while time.time() < start_time + 10:
        try:
            print('Scanning...')
            scanner.sendto(message, ('<broadcast>', 1337))
            data, addr = scanner.recvfrom(1024)
            if data.decode('utf-8') == 'sensorgrid-transmitter-ack':
                print('received ack from: %s' % str(addr))
                known_transmitters += [addr]
        except socket.timeout: continue
        continue
except KeyboardInterrupt:
    print('Scan exiting early.')

print('Scan complete. Found %i transmitters.' % len(known_transmitters))

