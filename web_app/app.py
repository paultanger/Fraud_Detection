from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass
import sys

################################
### ANYTHING HERE LOADS ONCE ###
################################

def setup_db(db_details):
    return create_engine(db_details)

# setup db for queries
db_details = f'postgresql://postgres:{getpass()}@3.128.75.60:5432/fraud_data'
engine = setup_db(db_details)

app = Flask(__name__, root_path='./') # template_folder = 'templates/')

# load processed api data from this table in db: api_data_processed
query = 'SELECT * FROM api_data_processed;'
api_data = pd.read_sql(query, con=engine)

#######################################
### EACH OF THESE LOAD WITH EACH PAGE #
#######################################

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

# display most recent 10 from api
@app.route('/recent10')
def recent10():
    query = "SELECT body_length, channels, country, currency, delivery_method, description, email_domain, \
                fb_published, has_analytics, name, org_name, \
                sale_duration, user_age, venue_country, venue_name, created_at \
                FROM api_data WHERE created_at IS NOT NULL ORDER BY created_at DESC LIMIT 10;"
    try:
        rows = pd.read_sql(query, con=engine)
    except:
        return f"""something is broken"""
    return render_template('recent10.html', data=rows.to_html(classes=["table","text-right", "table-hover"], border=0, index=False))
    

# let user choose some parameters on what to query
@app.route('/query', methods=['GET', 'POST'])
def query_form():
    return render_template("query.html")

# return results
@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        n_records = int(request.form['n_records'])
        fraud_cutoff = float(request.form['fraud_cutoff'])
        # query = f"SELECT body_length, channels, country, currency, delivery_method, description, email_domain, \
        #         fb_published, has_analytics, name, org_name, \
        #         sale_duration, user_age, venue_country, venue_name, created_at \
        #         FROM api_data WHERE created_at IS NOT NULL ORDER BY created_at DESC LIMIT {n_records};"
        # result = pd.read_sql(query, con=engine)
        cols = ['fraud_prob', 'body_length', 'channels', 'delivery_method', 'event_created',
            'event_end', 'event_published', 'event_start', 'fb_published',
            'has_analytics', 'has_header', 'has_logo', 'name_length',
            'org_facebook', 'org_twitter', 'sale_duration', 'show_map',
            'user_age', 'user_created', 'user_type', 'venue_latitude', 
            'venue_longitude', 'amount', 'quantity_total', 'cost']
        # get subset of cols
        result = api_data.loc[:,cols]
        # filter based on fraud cutoff value
        result = result.loc[result['fraud_prob'] > fraud_cutoff]
        # select subset of rows and cols we want
        result = result.iloc[:n_records]
        # order descending
        result.sort_values('fraud_prob', ascending=False, inplace=True)
        # TODO error check if no results..

    except:
        return f"""You have entered an incorrect value or something isn't quite working right.
                    Sorry about that!  Hit the back button and try again."""

    return render_template('results.html', data=result.to_html(classes=["table","text-right", "table-hover"], border=0, index=False))


if __name__ == '__main__':
    # run app to run on aws: run app.py 1
    # if on AWS otherwise local debug mode
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=33507, debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)