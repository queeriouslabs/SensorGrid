import socket
import time
import sys




def flush_old_requests(reqs):
    now = time.time()
    return [
      req for req in reqs
          if req['time'] >= now - 11
    ]

def find_request(reqs, addr):
  for req in reqs:
    if req["addr"] == addr: return True
  return False



if sys.argv[1] is not None:
  port = int(sys.argv[1])
else:
  port = 1337

transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
transmitter.bind(('', port))

print('SensorGrid transmitter running.')

recent_requests = []

try:
    while True:
        recent_requests = flush_old_requests(recent_requests)
        data, addr = transmitter.recvfrom(1024)
        if data.decode('utf-8') == 'sensorgrid-scanner-syn':
            if find_request(recent_requests, addr):
                print('Received repeat ping. Ignoring.')
            else:
                print('Received new ping from %s. responding.' % str(addr))
                transmitter.sendto(b'sensorgrid-transmitter-ack', addr)
                recent_requests += [{ 'time': time.time(), 'addr': addr }]
        else:
            print('received other message: %s' % str(data))
except KeyboardInterrupt:
    print('SensorGrid transmitter shutting down.')
