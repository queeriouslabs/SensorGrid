import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = 'foo'.encode('utf-8') 
while True:
    server.sendto(message, ('<broadcast>', 1337))
    print("message sent!")
    time.sleep(1)
