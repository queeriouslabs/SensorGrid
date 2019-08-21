import flask
import sys
import os
import random
import json
from jinja2 import Template

from transmitter import run_transmitter

if len(sys.argv) < 2:

    print('Please give a port.')

else:

    port = sys.argv[1]
    run_transmitter(port, 10)
    port = int(port)

    app = flask.Flask(__name__)

    @app.route('/', methods=['GET'])
    def get_queirdos():

        if not os.path.isfile('profiles.json'):
            with open('profiles.json', 'w') as f:
                f.write(json.dumps([]))

        with open('profiles.json', 'r') as f:
            profs = json.loads(f.read())

        profs.sort(key=lambda prof: prof['name'])

        with open('queirdos.html', 'r') as f:
            html = Template(f.read()).render({
                'stylesheet': flask.url_for('static', filename='pink_on_black.css'),
                'profiles': profs
            })

        return html

    @app.route('/transmitter_info', methods=['GET'])
    def get_transmitter_info():
        return json.dumps({
            'name': 'Queirdos',
            'description': 'A list of people who come to the space.'
        })

    @app.route('/', methods=['POST'])
    def post_queirdos():

        if not os.path.isfile('profiles.json'):
            with open('profiles.json', 'w') as f:
                f.write(json.dumps([]))

        with open('profiles.json', 'r') as f:
            profs = json.loads(f.read())

        profs += [{'name': flask.request.form['name'],
                   'info': flask.request.form['info'],
                   'uid': ''.join([random.choice('0123456789abcdef')
                                   for _ in range(32)])
                   }]

        with open('profiles.json', 'w') as f:
            f.write(json.dumps(profs))

        return flask.redirect('/')

    @app.route('/delete/<uid>', methods=['GET'])
    def delete_quierdo(uid):

        with open('profiles.json', 'r') as f:
            profs = json.loads(f.read())

        with open('profiles.json', 'w') as f:
            f.write(json.dumps([
                prof for prof in profs
                if prof['uid'] != uid
            ]))

        return flask.redirect('/')

    app.run(host='0.0.0.0', port=port)
