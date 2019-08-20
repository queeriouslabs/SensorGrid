import socket
import time
import re
import json
import time


def scan():
    socket.setdefaulttimeout(0.1)
    scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = 'sel-syn'.encode('utf-8') 
    
    start_time = time.time()
    known_transmitters = []
    
    while time.time() < start_time + 10:
        scanner.sendto(message, ('<broadcast>', 1337))
        for i in range(10):
            try:
                data, addr = scanner.recvfrom(1024)
                m = re.split('\s+', data.decode('utf-8'), 1)
                if m[0] == 'sel-ack':
                    known_transmitters += [(addr[0], json.loads(m[1]))]
            except socket.timeout: pass
    
    return known_transmitters        
