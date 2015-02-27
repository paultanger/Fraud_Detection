from flask import Flask,request
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
import logging
import pandas as pd

logging.basicConfig()

apps = {}


urls = []



def start_server():
    if 'apps' in apps:
        return
    try:
        apps['apps'] = Flask(__name__)
        api = restful.Api(apps['apps'])
        api.add_resource(Register, '/register')
        http_server = HTTPServer(WSGIContainer(apps['apps']))
        http_server.listen(5000,'0.0.0.0')
    except:
        pass

def get_object():
    random_json = data.loc[[random.randint(0,num_data_points)]].to_json()
    as_dict =  simplejson.loads(random_json)
    ret = {}
    first_key = None
    for key in as_dict.keys():
        if(first_key is None):
            first_key = as_dict.itervalues().next().keys()[0]
        ret[key] = as_dict[key][first_key]
    return ret


def ping():
    if 'apps' not in apps:
        start_server()
        thread = Thread(target = IOLoop.instance().start)
        thread.start()

    for url in urls:
        print 'url',url

        random_json = get_object()
        headers = {'Content-Type': 'application/json'}
        try:
            post(url + '/score',data=simplejson.dumps(random_json),headers=headers)
            print "sent to %s" % url
        except ConnectionError:
            print "%s not listening" % url



class Register(restful.Resource):

    def post(self):
        ip = request.form['ip']
        port = request.form['port']
        url = 'http://' + ip + ':' + port
        if url not in urls:
            urls.append(url)
        else:
            print 'Url ' + url + ' is already registered'
        return {'Message': 'Added url ' + url}

    def put(self):

        print  request.json
        return simplejson.dumps(request.json)




with open('data/test_new.json') as f:
    contents = f.read()
    data = pd.read_json('data/test_new.json')
    for column in data.columns:
        if column == 'acct_type':
              data.drop(column, axis=1, inplace=True)
    num_data_points = data.shape[0]
    print get_object()



if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=pytz.utc)

    #10 seconds from now
    scheduler.add_job(ping, 'interval', seconds=30, max_instances =100)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
