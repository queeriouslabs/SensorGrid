import socket
import time
import sys
import re




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

def parse_message(message):
    m = re.split('\s+', message)
    if m and m[0] == 'sensorgrid':
        return (m[1], m[2] if 2 in m else None)
    else:
        return None

def run_transmitter(port, callback):
    transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    transmitter.bind(('', port))

    print('SensorGrid transmitter running.')

    recent_requests = []

    try:
        while True:
            recent_requests = flush_old_requests(recent_requests)
            data, addr = transmitter.recvfrom(1024)
            
            message = parse_message(data.decode('utf-8'))
            if message:
                print(message)
                message_name, message_content = message
                if message_name == 'scanner-syn':
                    if find_request(recent_requests, addr):
                        print('Received repeat ping. Ignoring.')
                    else:
                        print('Received new ping from %s. responding.' % str(addr))
                        transmitter.sendto(b'sensorgrid-transmitter-ack', addr)
                        recent_requests += [{ 'time': time.time(), 'addr': addr }]
                elif message_name == 'service':
                    callback(message_content)
                else:
                    print('received other message: %s' % str(data))
    except KeyboardInterrupt:
        print('SensorGrid transmitter shutting down.')

def main(arg):
  print('Doing Thing: ' + arg)

run_transmitter(1337, main)
