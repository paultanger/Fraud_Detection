from flask import Flask,request
import flask_restful as restful
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from requests import post,put
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


white_list = [
    "body_length",
    "event_end",
    "ip",
    "venue_latitude",
    "event_published",
    "channels",
    "currency",
    "org_desc",
    "name_length",
    "event_created",
    "approx_payout_date",
    "has_logo",
    "email_domain",
    "payout_type",
    "show_map",
    "has_header",
    "venue_state",
    "venue_country",
    "has_analytics",
    "delivery_method",
    "country",
    "name",
    "num_payouts",
    "sale_duration",
    "previous_payouts",
    "fb_published",
    "venue_longitude",
    "description",
    "org_name",
    "user_age",
    "org_facebook",
    "listed",
    "org_twitter",
    "event_start",
    "venue_address",
    "sale_duration2",
    "venue_name"
]


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
        post(url + '/score',data=simplejson.dumps(random_json),headers=headers)



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




with open('test.json') as f:
    contents = f.read()
    data = pd.read_json('test.json')
    for column in data.columns:
        if column not in white_list:
              data.drop(column, axis=1, inplace=True)
    num_data_points = data.shape[0]
    print get_object()




if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=pytz.utc)

    scheduler.add_executor('processpool')
    #10 seconds from now
    #scheduler.add_job(start_api,'date',run_date=datetime.datetime.now(),timezone=pytz.utc)
    scheduler.add_job(ping, 'interval', seconds=1)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
