from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass
import sys

def setup_db(db_details):
    return create_engine(db_details)

def run_api(db_details):
    client = EventAPIClient(db=db_details)
    client.collect()

# setup db for queries
db_details = f'postgresql://postgres:{getpass()}@3.128.75.60:5432/fraud_data'
engine = setup_db(db_details)

x = pd.read_csv('../data/display.csv')

app = Flask(__name__, root_path='./') # template_folder = 'templates/')

# remove template limit
# app.jinja_env.cache = {}

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

#---    getting a pandas df to display on a web app
@app.route('/analysis') 
def analysis():
    return render_template("analysis.html", tables=[x.to_html(classes='data')], titles=x.columns.values)

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
    # return render_template('recent10.html', rows=[rows.to_html(
    #     classes='table table-striped', index=False, table_id= 'recent10table')], titles=['na', rows.columns.values])
    return render_template('recent10.html', data=rows.to_html( classes='table table-bordered', 
                            index=False, table_id='dataTable', border=0))

# let user choose some parameters on what to query
@app.route('/query_form')
def query_form():
    # form action is what to do when submitted
    return ''' enter the number of recent records from the API to view <form action="/query_results" method="POST">
                <input type="text" name="n_records" />
                <input type="submit" />
               </form>
             '''

@app.route('/query_results', methods=['POST'])
def query_results():
    try:
        n_records = int(request.form['n_records'])
        query = f"SELECT body_length, channels, country, currency, delivery_method, description, email_domain, \
                fb_published, has_analytics, name, org_name, \
                sale_duration, user_age, venue_country, venue_name, created_at \
                FROM api_data WHERE created_at IS NOT NULL ORDER BY created_at DESC LIMIT {n_records};"
        rows = pd.read_sql(query, con=engine)
    except:
        return f"""something is broken"""

    return render_template('query_results.html', data=rows.to_html( classes='table table-bordered', 
                            index=False, table_id='dataTable', border=0))

# custom 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    # run app
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=33507, debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
    # for AWS
    # app.run(host='0.0.0.0', port=33507, debug=False)