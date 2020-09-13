import numpy as np
import pandas as pd
from getpass import getpass
from sqlalchemy import create_engine

def setup_db(db_details):
    return create_engine(db_details)


def clean_rows(rows):
    col_list = []
    # get list of numeric cols
    for c in rows.columns:
        if rows[c].dtype == 'int64' or rows[c].dtype == 'float64':
            col_list.append(c)
    # return only numeric cols
    rows_subset = rows[col_list].copy()
    # fill nas etc - would need to get the mean values from the original data..
    # rows_subset[col] = rows_subset[col].fillna(rows_subset[col].mean())
    # rows_subset[col] = rows_subset[col].fillna(0)
    rows_subset.fillna(0, inplace=True)
    return rows_subset


def clean_ticket_type(ticket_type):
    ticket_type = ticket_type.groupby('object_id').agg(
        cost = ('cost', 'mean'),
        tot_q = ('quantity_total', 'sum'))
    ticket_type.fillna(0, inplace = True) 
    ticket_type = ticket_type.replace(np.inf, 110)
    return ticket_type


def combine_dfs(cleaned_rows, cleaned_ticket_type):
    # merge these using object_id as id col
    raise NotImplementedError


if __name__=='__main__':
    db_details = f'postgresql://postgres:galvanize@52.15.236.214:5432/fraud_data'
    # db_details = f'postgresql://postgres:{getpass()}@52.15.236.214:5432/fraud_data'
    engine = setup_db(db_details)
    # get some test data from api db
    with engine.connect() as conn:
        query = 'select * from api_data LIMIT 5;'
        # query = 'select * from api_data where sequence_number > 300 order by sequence_number desc limit 5;'
        query = "select * from api_data where created_at > '2020-09-12' order by created_at desc limit 5;"
        rows = pd.read_sql(query, con=engine)
        query = 'select * from ticket_types LIMIT 5;'
        ticket_types = pd.read_sql(query, con=engine)
    
    cleaned_rows = clean_rows(rows)
    cleaned_ticket_type = clean_ticket_type(ticket_types)
    # final = combine_dfs(cleaned_rows, cleaned_ticket_type)