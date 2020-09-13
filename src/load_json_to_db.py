import json
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass

def main():
    '''
    careful this overwrites existing tables!
    We really only need to run this once
    '''

    db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
    engine = create_engine(db_details)
    # put original data in database
    df = pd.read_json('../data/data.json')
    df.drop(['ticket_types', 'previous_payouts'], axis=1, inplace=True)
    # load json to get nested json dicts
    with open('../data/data.json') as f:
        json_data = json.load(f)
    # unpack nested json of ticket types and prev payouts
    tix_types = pd.json_normalize(data=json_data, record_path='ticket_types', meta=['object_id']) 
    prev_pay_types = pd.json_normalize(data=json_data, record_path='previous_payouts', meta=['object_id'])
    print('created dfs') 
    # return prev_pay_types
    # add these three files to tables in database (and create the tables at the same time)
    with engine.connect() as conn:
        # if you don't set method to multi it is slowwwww - chunksize is # of rows to write at a time
        df.to_sql('original_data', conn, if_exists='replace', index=False, method='multi')
        # # for the main table we can set primary key
        conn.execute('ALTER TABLE original_data ADD PRIMARY KEY (object_id);')
        print('added data to original_data')
        # # for these, there will be multiple rows for each event
        tix_types.to_sql('org_ticket_types', conn, if_exists='replace', index=False, method='multi')
        print('added data to org_ticket_types')
        # this df is very large, > 1m rows, change chunksize so we don't crash
        prev_pay_types.to_sql('org_previous_payouts', conn, if_exists='replace', index=False, method='multi', chunksize=100_000)
        print('added data to org_previous_payouts')
        # just do this to get the right columns in the table
        df = df.head()
        df.to_sql('api_data', conn, if_exists='replace', index=False, method='multi')
        print('added data to api_data')
        # add a column for sequence number (for api data)
        conn.execute('ALTER TABLE api_data ADD COLUMN sequence_number bigint;')
        # add primary key
        conn.execute('ALTER TABLE api_data ADD PRIMARY KEY (object_id);')
        # now drop the rows so it is clean table for the api
        conn.execute('DELETE FROM api_data;')


if __name__ == "__main__":
    main()
    # query = 'select * from api_data;'
    # result = pd.read_sql(query, con=engine)
    pass