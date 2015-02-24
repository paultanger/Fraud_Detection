from flask import Flask, request
import flask_restful as restful
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from requests import post, ConnectionError
import simplejson
import random
import pytz
from threading import Thread
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import pandas as pd
import sys


class Register(restful.Resource):
    def post(self):
        ip = request.form['ip']
        port = request.form['port']
        url = 'http://%s:%s' % (ip, port)
        Server.urls.add(url)
        return {'Message': 'Added url %s' % url}

    def put(self):
        print request.json
        return simplejson.dumps(request.json)


class Server(object):
    urls = set()

    def __init__(self):
        self.scheduler = None
        self.data = None
        self.app = None

    def load_data(self, filename, label='acct_type'):
        data = pd.read_json(filename)
        data.drop(label, axis=1, inplace=True)
        return data

    def start_server(self):
        try:
            app = Flask(__name__)
            api = restful.Api(app)
            api.add_resource(Register, '/register')
            http_server = HTTPServer(WSGIContainer(app))
            http_server.listen(5000, '0.0.0.0')
            return app
        except Exception as e:
            print e.message

    def get_random_datapoint(self):
        index = random.randint(0, len(self.data))
        datapoint = self.data.loc[[index]].to_dict()
        for key, value in datapoint.iteritems():
            datapoint[key] = value.values()[0]
        return index, datapoint

    def ping(self):
        if not self.app:
            self.app = self.start_server()
            thread = Thread(target=IOLoop.instance().start)
            thread.start()
            print "Server started. Ready to receive posts."
        index, datapoint = self.get_random_datapoint()
        print "sending datapoint %d" % index
        for url in self.urls:
            headers = {'Content-Type': 'application/json'}
            try:
                post(url + '/score',
                     data=simplejson.dumps(datapoint),
                     headers=headers)
                print "sent to %s" % url
            except ConnectionError as e:
                print "%s not listening." % url

    def run(self, filename='test.json'):
        self.data = self.load_data(filename)
        self.scheduler = BlockingScheduler(timezone=pytz.utc)
        self.scheduler.add_job(self.ping, trigger='interval', seconds=5)
        print 'Press Ctrl+C to exit'
        try:
            self.scheduler.start()
        except:
            print "\nGoodbye."


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python register.py filename.json"
        exit()
    filename = sys.argv[1]
    server = Server()
    server.run(filename)
