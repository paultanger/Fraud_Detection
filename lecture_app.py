from flask import Flask, request, render_template
import json
from model import load_model
import requests
import socket
import time

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.3.35.54:5000/register"
DATA = []
TIMESTAMP = []


@app.route('/score', methods=['POST'])
def score():
    DATA.append(json.dumps(request.json))
    TIMESTAMP.append(time.time())
    return ""


@app.route('/check')
def check():
    if DATA and TIMESTAMP:
        return "%d\n\n%s" % (TIMESTAMP[-1], DATA[-1]), 200, {'Content-Type': 'text/css; charset=utf-8'}
    return "No data received"

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    # Register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)