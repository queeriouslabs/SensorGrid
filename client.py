import socket
import time
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = sys.argv[1].encode('utf-8') 

server.sendto(message, ('<broadcast>', 1337))

while True:
    data, addr = client.recvfrom(1024)
    print('received message: %s / %s' % (data.decode('utf-8'), str(addr)))
