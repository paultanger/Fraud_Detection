"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
import pymongo
import pandas as pd
import psycopg2 as pg2
from sqlalchemy import create_engine

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
        # paul added
        self.cols = ['body_length',
                'channels',
                'country',
                'currency',
                'delivery_method',
                'description',
                'email_domain',
                'event_created',
                'event_end',
                'event_published',
                'event_start',
                'fb_published',
                'has_analytics',
                'has_header',
                'has_logo',
                'listed',
                'name',
                'name_length',
                'object_id',
                'org_desc',
                'org_facebook',
                'org_name',
                'org_twitter',
                'payee_name',
                'payout_type',
                'previous_payouts',
                'sale_duration',
                'show_map',
                'ticket_types',
                'user_age',
                'user_created',
                'user_type',
                'venue_address',
                'venue_country',
                'venue_latitude',
                'venue_longitude',
                'venue_name',
                'venue_state',
                'sequence_number']
        self.df = pd.DataFrame(columns = self.cols)

    def save_to_database(self, row):
        """Save a data row to the database."""
        #print("Received data:\n" + repr(row) + "\n")  # replace this with your code
        # print(pd.json_normalize(row))
        # self.df = self.df.append(pd.json_normalize(row))
        # self.df.to_csv('../data/api_data.csv', index=False)
        self.connect_db_add_row(row)
        print('row saved to db')
    
    def connect_db_add_row(self, row):
        engine = create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data')
        conn = engine.connect()
        # conn.execute('CREATE SCHEMA fraud')
        # can't store nested dicts
        row = row[['body_length', 'channels']]
        row.to_sql('api_data', conn, if_exists='append', index=False)  # if_exists='append',index=False, 
        # with create_engine('postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data') as engine:
        #     # with engine.connect() as conn:
        #     pd.json_normalize(row).to_sql('api_data', engine, if_exists='replace',index=False)

    def get_df(self):
        return self.df

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
    # client.collect()
    # df = client.get_df()
    # print(df)
    # or just get most recent 10
    # client = EventAPIClient()

    recent10 = client.get_data()
    row = pd.json_normalize(recent10)
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

