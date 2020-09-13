from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)

# from src.api_client import EventAPIClient
# #---     use pickle to load in the pre-trained model; loaded at the top of the app, loaded into memory ONCE on the server rather than loaded every time
# with open(f'','rb') as f:
#     model = pickle.load(f)

def setup_db(db_details):
    return create_engine(db_details)

def run_api(db_details):
    client = EventAPIClient(db=db_details)
    client.collect()

# setup db for queries
# db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
db_details = f'postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data'
engine = setup_db(db_details)

x = pd.read_csv('../data/display.csv')

app = Flask(__name__, root_path='./') # template_folder = 'templates/')

# remove template limit
# app.jinja_env.cache = {}

# a more complex guide here: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
# https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/form_example', methods=['GET'])
def form_display():
    return ''' <form action="/string_reverse" method="POST">
                <input type="text" name="some_string" />
                <input type="submit" />
               </form>
             '''

@app.route('/string_reverse', methods=['POST'])
def reverse_string():
    text = str(request.form['some_string'])
    reversed_string = text[-1::-1]
    return ''' output: {}  '''.format(reversed_string)

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
    # setup api save to db
    # db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
    # run_api(db_details)
    # run app
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # for AWS
    app.run(host='0.0.0.0', port=33507, debug=False)


"""
M notes:
#----   after cursor add following code to take in new data and put into PD
#----   take input from SQL and place into Pandas DF
sql_query = pd.read_sql_query('SELECT * FROM **NAME**, conn)

#----   will need to run sql_query through cleaning function
from predict import all_together

cleaned_x = all_together(sql_query)

#----   will need to run code above through pickle model
loaded_model = pickle.load(open('../data/pickle_model.pkl', 'rb'))
proba = loaded_model.predict_proba(cleaned_x) #array of proba
proba = list(proba[:,1])
cleaned_x['prediction'] = proba

#----   get pred.proba and categorize into HIGH, MED, LOW by adding column *WHERE does this info go?
def flag_label(row):
    if row['predict'] == 1 and row['predict'] > 0.97:
        return 'HIGH'
    elif row['predict'] > 0.95:
        return 'MEDIUM'
    elif row['predict'] > 0.91:
        return 'LOW'
    else:
        return 'Not Fraud'

cleaned_x['flag'] = cleaned_x.apply(lambda row: flag_label(row), axis = 1)
display = cleaned_x.iloc[:,[16, 32]].copy() #DOUBLE CHECK

#----   render above dataframe as html and select 
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()

#----   write html to flask app
text_file = open("fraud_check.html", "w")
text_file.write(html)
text_file.close()
"""