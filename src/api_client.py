"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
# import pymongo - not needed
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass

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
        self.engine = create_engine(self.db)
        self.interval = 30
        

    def save_to_database(self, row):
        """Save a data row to the database."""
        # convert to df
        self.row_df = pd.json_normalize(row)
        # drop ticket types and payout jsons
        self.row_df.drop(['ticket_types', 'previous_payouts'], axis=1, inplace=True)
        # unpack nested json of ticket types and prev payouts
        self.tix_types = pd.json_normalize(data=row, record_path='ticket_types', meta=['object_id']) 
        self.prev_pay_types = pd.json_normalize(data=row, record_path='previous_payouts', meta=['object_id']) 

        # send to db
        self.connect_db_add_row()
    

    def connect_db_add_row(self):
        # check if object id exists, if does, don't add
        query = f'SELECT 1 FROM api_data WHERE object_id = {self.row_df["object_id"][0]};'
        exists = self.engine.execute(query)
        if not exists.rowcount:
            with self.engine.connect() as conn:
                    self.row_df.to_sql('api_data', conn, if_exists='append', index=False, method='multi')
                    self.tix_types.to_sql('ticket_types', conn, if_exists='append', index=False, method='multi')
                    self.prev_pay_types.to_sql('previous_payouts', conn, if_exists='append', index=False, method='multi')
                    # add primary keys from object ids
                    # conn.execute('ALTER TABLE api_data ADD PRIMARY KEY (object_id);')
            print('row saved to db')
        else:
            print('row exists')


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
    db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
    client = EventAPIClient(db=db_details)
    client.collect()