import socket
import time
import sys
import re
import threading
import json




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

def transmitter_thread(name, desc, port):
    
    def run_transmitter():
        service_info = { 'name': name, 'desc': desc, 'port': port }
        known_services = [service_info]
        
        transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            transmitter.bind(('', 1337))
        except OSError:
            transmitter.sendto(('sel-register %s' % json.dumps(service_info)).encode('utf-8'), ('127.0.0.1', 1337))
    
        print('SensorGrid transmitter running.')
    
        recent_requests = []
    
        try:
            while True:
                recent_requests = flush_old_requests(recent_requests)
                data, addr = transmitter.recvfrom(1024)
                message = data.decode('utf-8')
                if message == 'sel-syn':
                    if find_request(recent_requests, addr):
                        pass
                    else:
                        print()
                        print('Received new ping from %s.' % str(addr))
                        transmitter.sendto(('sel-ack %s' % json.dumps(known_services)).encode('utf-8'), addr)
                        recent_requests += [{ 'time': time.time(), 'addr': addr }]
                elif message[0:19] == 'sel-register':
                    info = json.loads(message[20:])
                    if 0 == len([ 1 for s in known_services if s['port'] == info['port']]):
                        print()
                        print('Registering other service:')
                        print()
                        print('  Name: ' + info['name'])
                        print('  Port: %i' % info['port'])
                        print('  Description: ' + info['desc'])
                        known_services += [info]
                else:
                    print('received other message: %s' % str(data))
        except KeyboardInterrupt:
            print('SensorGrid transmitter shutting down.')



    t = threading.Thread(target = lambda: run_transmitter())
    t.start()




