import flask
import sys
import os
import json
import requests
import time
from jinja2 import Template

from transmitter import run_transmitter
from scanner import run_scanner

if len(sys.argv) < 2:

    print('Please give a port.')

else:

    def scanner_thread(addr):

        now = time.time()
        service = {
            'url': 'http://%s:%s' % (addr[0], addr[1]), 'last_seen': now}
        try:
            r = requests.get(service['url'] + '/transmitter_info')
            if r.status_code == 200:
                info = json.loads(r.text)
                service['name'] = info['name']
                service['description'] = info['description']

                if not os.path.isfile('services.json'):
                    with open('services.json', 'w') as f:
                        f.write(json.dumps([]))

                with open('services.json', 'r') as f:
                    known_services = json.loads(f.read())

                known_services = [
                    old_service for old_service in known_services
                    if old_service['url'] != service['url'] and (20 * 60) > now - old_service['last_seen']
                ]

                if service not in known_services:
                    with open('services.json', 'w') as f:
                        f.write(json.dumps(known_services +
                                           [service]))
        except requests.exceptions.ConnectionError:
            pass

    run_scanner(scanner_thread)

    port = sys.argv[1]
    run_transmitter(port, 30)
    port = int(port)

    app = flask.Flask(__name__)

    @app.route('/transmitter_info', methods=['GET'])
    def get_transmitter_info():
        return json.dumps({
            'name': 'Transmitter Index',
            'description': 'A list of transmitters currently in the space.'
        })

    @app.route('/', methods=['GET'])
    def get_services():

        if os.path.isfile('services.json'):
            with open('services.json', 'r') as f:
                services = json.loads(f.read())
        else:
            services = []

        services.sort(key=lambda x: x['name'])

        with open('transmitter_index.html', 'r') as f:
            html = Template(f.read()).render({
                'stylesheet': flask.url_for('static', filename='pink_on_black.css'),
                'transmitters': services
            })

        return html

    app.run(host='0.0.0.0', port=port)
