import socket
import time
import sys


if len(sys.argv) > 1:
  port = int(sys.argv[0])
else:
  port = 1337

socket.setdefaulttimeout(0.1)
scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = 'sensorgrid scanner-syn'.encode('utf-8') 

start_time = time.time()
known_transmitters = []

try:
    while time.time() < start_time + 10:
        print('Scanning...')
        scanner.sendto(message, ('<broadcast>', port))
        for i in range(10):
            try:
                data, addr = scanner.recvfrom(1024)
                if data.decode('utf-8') == 'sensorgrid-transmitter-ack':
                    known_transmitters += [addr]
            except socket.timeout: pass
except KeyboardInterrupt:
    print('Scan exiting early.')

print('Scan complete. Found %i transmitters.' % len(known_transmitters))

for transmitter in known_transmitters:
  try:
    scanner.sendto('sensorgrid service foo', transmitter['address'])
  except: pass
