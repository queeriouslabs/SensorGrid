import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(('', 1337))

while True:
    data, addr = server.recvfrom(1024)
    print('received message: %s / %s' % (data.decode('utf-8'), str(addr)))
    print('responding.')
    server.sendto(b'acknowledged!', addr)
    break
