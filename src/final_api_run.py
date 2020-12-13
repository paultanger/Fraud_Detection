import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass
import sys

def setup_db(db_details):
    ''' set up database '''
    return create_engine(db_details)

def get_data(col, table_name):
    ''' run query on data base and return pandas df '''
    query = f'SELECT {", ".join(x for x in col)} FROM {table_name};'
    df = pd.read_sql(query, con=db_connection)
    return df

def fill_api(df):
    ''' take in the api data and fill any NaN or 0 '''
    fill = pd.read_csv("data/fillwith.csv").drop('Unnamed: 0', axis = 1)
    for idx, c in enumerate(fill['col']):
        df[c].fillna(fill.iloc[idx,0], inplace = True)    
    return df

def run_model(df):
    ''' loads model, makes a prediction, creates prediction column '''
    loaded_model = pickle.load(open('data/finalized_model.sav', 'rb'))
    fraud_prob = []
    not_fraud_prob = []
    for idx in range(df.shape[0]):
        row = df.iloc[idx,:].values
        prob = loaded_model.predict_proba(row.reshape(1,-1))
        fraud_prob.append(prob.tolist()[0][1])
        not_fraud_prob.append(prob.tolist()[0][0])  

    df['not_fraud'] = not_fraud_prob
    df['fraud_prob'] = fraud_prob

    return df

if __name__ == '__main__':
    #---    CONNECT TO DATABASE
    db_details = f'postgresql://postgres:{getpass()}@3.128.75.60:5432/fraud_data'
    db_connection = setup_db(db_details)
    print("Connection made")

    #---    COLUMNS NEEDED TO RUN MODEL
    api_cols = ['body_length', 'channels', 'delivery_method', 'event_created',
            'event_end', 'event_published', 'event_start', 'fb_published',
            'has_analytics', 'has_header', 'has_logo', 'name_length',
            'object_id', 'org_facebook', 'org_twitter', 'sale_duration', 'show_map',
            'user_age', 'user_created', 'user_type', 'venue_latitude', 'venue_longitude']

    #---    GET DATAFRAMES NEEDED, MERGE, CLEAN 
    api_main = get_data(api_cols, 'api_data')
    
    prev_payouts = get_data(['amount', 'object_id'], 'previous_payouts')
    prev_payouts = prev_payouts.groupby('object_id').agg({'amount':'sum'}).reset_index()
    
    ticket_types = get_data(['object_id', 'cost', 'quantity_total'], 'ticket_types')
    ticket_types = ticket_types.groupby('object_id').agg({'quantity_total':'sum', 'cost':'sum'}).reset_index()

    full = pd.merge(api_main, prev_payouts, how='left', on = 'object_id')
    full = pd.merge(full, ticket_types, how='left', on = 'object_id')
    full = fill_api(full)
    print("Dataframes created")

    #---    LOAD MODEL, RUN ADD PREDICTION COLUMN
    full = run_model(full)
    print("Model predictions complete")