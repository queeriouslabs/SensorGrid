import socket
import time
import sys

socket.setdefaulttimeout(10)
scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = 'sensorgrid-scanner-syn'.encode('utf-8') 

scanner.sendto(message, ('<broadcast>', 1337))

print('Scanning...')
start_time = time.time()
known_transmitters = []
while time.time() < start_time + 10:
    try:
        data, addr = scanner.recvfrom(1024)
        if data.decode('utf-8') == 'sensorgrid-transmitter-ack':
            print('received ack from: %s' % str(addr))
            known_transmitters += [addr]
    except socket.timeout: continue
    continue

print('Scan complete. Found %i transmitters.' % len(known_transmitters))

