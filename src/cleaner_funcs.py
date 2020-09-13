import numpy as np
import pandas as pd
from getpass import getpass
from sqlalchemy import create_engine

def setup_db(db_details):
    return create_engine(db_details)

def clean_rows(row):
    pass


def clean_ticket_type(ticket_type):
    pass


if __name__=='__main__':
    db_details = f'postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data'
    # db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
    engine = setup_db(db_details)
    # get some test data from api db
    with engine.connect() as conn:
        query = 'select * from api_data LIMIT 5;'
        rows = pd.read_sql(query, con=engine)
        query = 'select * from ticket_types LIMIT 5;'
        ticket_types = pd.read_sql(query, con=engine)
    
    cleaned_row = clean_rows(rows)
    cleaned_ticket_type = clean_ticket_type(ticket_types)