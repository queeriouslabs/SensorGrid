import flask
import sys
import os
import json

from transmitter import transmitter_thread

if len(sys.argv) < 2:

    print('Please give a port.')

else:

    port = int(sys.argv[1])

    transmitter_thread('Queirdos', 'A list of folx who come to the space.', port)

    app = flask.Flask(__name__)

    @app.route('/', methods = ['GET'])
    def get_queirdos():

      if not os.path.isfile('profiles.json'):
        with open('profiles.json', 'w') as f:
          f.write(json.dumps([]))
      
      with open('profiles.json', 'r') as f:
        profs = json.loads(f.read())
      
      html = '<html><body><form method="post">Name: <input type="text" name="name"/><br/>Info: <input type="text" name="info"/><br/><input type="submit"/></form><ul>'
      for prof in profs:
        html += '<li>%s: %s</li>' % (prof['name'], prof['info'],)
      html += '</ul></body></html>'
      
      return html

    @app.route('/', methods = ['POST'])
    def post_queirdos():
      
      if not os.path.isfile('profiles.json'):
        with open('profiles.json', 'w') as f:
          f.write(json.dumps([]))

      with open('profiles.json', 'r') as f:
        profs = json.loads(f.read())

      profs += [{ 'name': flask.request.form['name'], 'info': flask.request.form['info'] }]
      print(profs)     
      with open('profiles.json', 'w') as f:
        f.write(json.dumps(profs))
      
      return flask.redirect('/')

    app.run(host = '0.0.0.0', port = port)
