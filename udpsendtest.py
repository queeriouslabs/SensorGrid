import socket
import time
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message = sys.argv[0].encode('utf-8') 

server.sendto(message, ('<broadcast>', 1337))
