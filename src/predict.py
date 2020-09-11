import numpy as np
import pandas as pd

###selected number value columns
#code to obtain column names of type int
def col_names(x):
    col_list = []
    for c in x.columns:
        if x[c].dtype == 'int64' or x[c].dtype == 'float64':
            col_list.append(c)
    return col_list


#created df of those column names
def numarical_df(x,col_list):
    return x[col_list]    #.drop('payee_name',axis=1)   

## replace nans with mea

def fill_mean(x,col):
    x[col] = x[col].fillna(x[col].mean())
def fill_zero(x,col):
    x[col] = x[col].fillna(0)



### take  ticket column and creat df ticket info
def ticket_types(row):
    ''' makes columns from the 'ticket_types' dictionary column'''
    row=row['ticket_types']
    if 'quantity_sold' not in row[0]:
        row[0]['quantity_sold'] = 0
    #row = list(row)
    #breakpoint()
    average_cost = np.mean([r['cost'] for r in row])
    sold = np.sum([r['quantity_sold'] for r in row])
    tot_q = np.sum([r['quantity_total'] for r in row])
    perc_sold = sold/tot_q
    return {'cost': average_cost , 'quantity':tot_q, 'num_sold': sold, 'percent_sold':perc_sold}

def make_ticket_df(x):
    #df = x.apply(lambda i: ticket_types(i) if i.index == 0 else i, axis=1, result_type='expand')
    df = x.apply(ticket_types, axis=1, result_type='expand')  
    df.fillna(0, inplace = True) 
    df = df.replace(np.inf, 110)
    return df



### concat num value df and ticket df
def concat_both(x_numarical,x2):
    fill_mean(x_numarical,'delivery_method')
    fill_mean(x_numarical,'event_published')
    #breakpoint()
    if 'has_header' not in x_numarical.columns:
        x_numarical['has_header'] = 0
    fill_mean(x_numarical,'has_header')
    fill_mean(x_numarical,'org_facebook')
    fill_mean(x_numarical,'org_twitter')
    fill_mean(x_numarical,'sale_duration')
    fill_zero(x_numarical,'venue_latitude')
    fill_zero(x_numarical,'venue_longitude')
    return pd.concat((x_numarical,x2),axis=1)

def all_together(sample):
    sample = pd.json_normalize(sample) 
    #breakpoint()
    col_name = col_names(sample)
    num_df = numarical_df(sample,col_name)
    ticket_df = make_ticket_df(sample)
    return concat_both(num_df,ticket_df)

if __name__=='__main__':
    
    sample = pd.read_json('../data/data.json')

    cleaned_sample = all_together(sample)
    
    