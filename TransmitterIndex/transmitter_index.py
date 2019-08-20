import flask
import sys
import os
import json
import threading
import time

from transmitter import transmitter_thread
from scanner import scan

if len(sys.argv) < 2:

    print('Please give a port.')

else:

    port = int(sys.argv[1])

    transmitter_thread('Transmitter Index', 'A list of services the space.', port)
    
    def scanner_thread():
        
        while True:
            known_transmitters = scan()
            known_services = []
            for transmitter in known_transmitters:
              ip = transmitter[0]
              services = transmitter[1]
              for service in services:
                known_services += [{
                  'name': service['name'],
                  'desc': service['desc'],
                  'addr': 'http://%s:%i' % (ip, service['port'])
                }]
            
            with open('services.json', 'w') as f:
                f.write(json.dumps(known_services))
            
            time.sleep(10)
    
    threading.Thread(target = scanner_thread).start()
    
    

    app = flask.Flask(__name__)

    @app.route('/', methods = ['GET'])
    def get_services():

        if os.path.isfile('services.json'):
            with open('services.json', 'r') as f:
                services = json.loads(f.read())
        else:
            services = []
        
        html = '''
<html>
  <body>
    <dl>'''
      
        if 0 == len(services):
            html += '      <dt>No services.</dt>'
        else:
            for service in services:
                html += '      <dt><a href="%s">%s</a></dt>' % (service['url'],service['name'])
                html += '      <dd>%s</dd>' % service['desc']
      
        html += '''
    </dl>
  </body>
</html>'''
      
        return html

    app.run(host = '0.0.0.0', port = port)
