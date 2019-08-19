import socket

transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
transmitter.bind(('', 1337))

while True:
    data, addr = transmitter.recvfrom(1024)
    if data.decode('utf-8') == 'sensorgrid-scanner-syn':
        print('received ping from %s. responding.' % str(addr))
        transmitter.sendto(b'sensorgrid-transmitter-ack', addr)
    else:
        print('received other message: %s' % str(data))
