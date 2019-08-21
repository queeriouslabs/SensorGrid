import socket
import time
import sys
import threading

from valid_port import valid_port


def run_transmitter(port, delay):

    if valid_port(port):
        def transmitter_thread():
            transmitter = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = ('sel-transmitter %s' % port).encode('utf-8')

            while True:
                transmitter.sendto(message, ('<broadcast>', 1337))
                time.sleep(delay)

        threading.Thread(target=transmitter_thread).start()
