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

# put model load stuff here

# write function for model predict (called on pages below)


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

# return results - this is what we need to clean up
@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        n_records = int(request.form['n_records'])
        query = f"SELECT body_length, channels, country, currency, delivery_method, description, email_domain, \
                fb_published, has_analytics, name, org_name, \
                sale_duration, user_age, venue_country, venue_name, created_at \
                FROM api_data WHERE created_at IS NOT NULL ORDER BY created_at DESC LIMIT {n_records};"
        result = pd.read_sql(query, con=engine)
    except:
        return f"""You have entered an incorrect value or something isn't quite working right.
                    Sorry about that!  Hit the back button and try again."""

    return render_template('results.html', data=result.to_html(classes=["table","text-right", "table-hover"], border=0, index=False))


if __name__ == '__main__':
    # run app
    # if on AWS otherwise local debug mode
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=33507, debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)