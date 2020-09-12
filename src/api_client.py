"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
import pymongo
import pandas as pd
import psycopg2 as pg2
from sqlalchemy import create_engine
import predict
import pickle

class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key='vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db=None,
                 interval=30):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        self.db = db
        self.interval = 30
        self.model = pickle.load(open('../data/pickle_model.pkl', 'rb'))
        

    def save_to_database(self, row):
        """Save a data row to the database."""
        #print("Received data:\n" + repr(row) + "\n") 
        # print(pd.json_normalize(row))
        # self.df = self.df.append(pd.json_normalize(row))
        # self.df.to_csv('../data/api_data.csv', index=False)

        # convert to df
        self.row_df = pd.json_normalize(row)
        # drop ticket types and payout jsons
        self.row_df.drop(['ticket_types', 'previous_payouts'], axis=1, inplace=True)
        # unpack nested json of ticket types and prev payouts
        self.tix_types = pd.json_normalize(data=row, record_path='ticket_types', meta=['object_id']) 
        self.prev_pay_types = pd.json_normalize(data=row, record_path='previous_payouts', meta=['object_id']) 

        ######### CLEAN UP BEFORE SAVING ##########
        # row = predict.all_together(row)
        # print(row)
        # if not row['quantity_sold']:
        #     print('this will break')
        ######### PREDICT ##########
        # row = self.make_predictions(row)

        ########## SEND TO DB ##########
        self.connect_db_add_row()
        print('row saved to db')
    
    def flag_label(self, row):
            if row['predict'] == 1 and row['predict'] > 0.97:
                return 'HIGH'
            elif row['predict'] > 0.95:
                return 'MEDIUM'
            elif row['predict'] > 0.91:
                return 'LOW'
            else:
                return 'Not Fraud'

    def make_predictions(self, row):
        proba = self.model.predict_proba(row) #array of proba
        proba = list(proba[:,1])
        row['prediction'] = proba
        #----   get pred.proba and categorize into HIGH, MED, LOW by adding column *WHERE does this info go?
        row['flag'] = row.apply(lambda row: self.flag_label(row), axis = 1)
        return row

    def connect_db_add_row(self):
        # engine = create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data')
        # conn = engine.connect()
        # # conn.execute('CREATE SCHEMA fraud')
        # self.row_df.to_sql('api_data', conn, if_exists='append', index=False)
        # self.tix_types.to_sql('ticket_types', conn, if_exists='append', index=False)
        # self.prev_pay_types.to_sql('previous_payouts', conn, if_exists='append', index=False)
        engine = create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data')
        with engine.connect() as conn:
            self.row_df.to_sql('api_data', conn, if_exists='append', index=False)
            self.tix_types.to_sql('ticket_types', conn, if_exists='append', index=False)
            self.prev_pay_types.to_sql('previous_payouts', conn, if_exists='append', index=False)

    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                for row in data:
                    self.save_to_database(row)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)


def main():
    """Collect events every 30 seconds."""
    client = EventAPIClient()
    client.collect()

if __name__ == "__main__":
    # main()
    # do it manually to access df
    client = EventAPIClient()
    client.collect()

    # df = client.get_df()
    # print(df)
    # or just get most recent 10
    # client = EventAPIClient()

    # recent10 = client.get_data()
    # result = predict.all_together(recent10)

    # row = pd.json_normalize(recent10)
    # row.drop(['ticket_types', 'payout_type', 'previous_payouts'], axis=1, inplace=True)
    # row.drop(['ticket_types', 'previous_payouts'], axis=1, inplace=True)


    # https://www.kaggle.com/jboysen/quick-tutorial-flatten-nested-json-in-pandas
    # ticket_types = pd.json_normalize(row['ticket_types'][0]) 
    # record path is name of cols that contain nested json (can pass list of cols if more than one)
    # meta is cols you want to grab and keep with the unpacked df
    # so now we can either store this in a sep table or do the calcs here
    # tix_types = pd.json_normalize(data=recent10, record_path='ticket_types', meta=['object_id']) 
    # pay_types = pd.json_normalize(data=recent10, record_path='payout_type', meta=['object_id']) 
    # prev_pay_types = pd.json_normalize(data=recent10, record_path='previous_payouts', meta=['object_id']) 

    #### PSYCO #######
    # conn = pg2.connect(database="fraud_data", user="postgres", password='galvanize', host="52.15.236.214", port="5432")
    # curs = conn.cursor()
    # sql = """INSERT INTO api_data(row) VALUES(%s);"""
    # curs.execute(sql, (row,))
    # try:
    #     with pg2.connect(database="fraud_data", user="postgres", password='galvanize', host="52.15.236.214", port="5432") as conn:
    #         with conn.cursor() as curs:
    #             # setup insert
    #             sql = """INSERT INTO api_data(row) VALUES(%s);"""
    #             # 
    #             curs.execute(sql, (row,))
    #             conn.commit()
    #             curs.close()
    # finally:
    #     conn.close()

    ##################

    # engine = create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data')
    # conn = engine.connect()
    # # conn.execute('CREATE SCHEMA fraud')
    # # can't store nested dicts
    # row = row[['body_length', 'channels']]
    # row.to_sql('api_data', conn, if_exists='append', index=False)  # if_exists='append',index=False, 
    ##################
    ##################
    ##################
    # 
    # with create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data') as engine:
    #     # with engine.connect() as conn:
    #     # pd.json_normalize(recent10)
    #     row = pd.json_normalize(recent10)
    #     row.to_sql('api_data', conn, if_exists='append',index=False)
    # this is a list of json records?
    # print(type(recent10))
    # print(len(recent10))
    #print(recent10)
    # we can convert to df:
    # record = pd.json_normalize(recent10) 
    # print(record)
    # collect will keep writing them to db once we implement that

    # then we need to call our prediction function on the data in the db
    # and update the fraud col?
    # or maybe we need two tables.. one for API data and one to store updated
    # in the notes below, it says it will come as a string, but seems like
    # it comes as a dict?

    # should we modify class to include connection to our db?

    ### IMPORTANT !!!! (after verifying that the data hasn't been seen before).
    '''
    The individual example will no longer be coming from a local file, 
    but instead you will get it by making a request to a server that will give 
    you a data point as a string, which you can parse into JSON. You can use 
    json.loads() to parse a string to json, which is the reverse process of json.dumps(). 
    You'll still need to vectorize it, predict, and store the example and prediction 
    in the database.
    '''

