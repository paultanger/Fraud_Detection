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
def numerical_df(x,col_list):
    return x[col_list].drop('payee_name',axis=1)   

## replace nans with mean
def replace_nans(x):



### take  ticket column and creat df ticket info
def ticket_types(row):
    ''' makes columns from the 'ticket_types' dictionary column'''
    row=row['ticket_types']
    average_cost = np.mean([r['cost'] for r in row])
    sold = np.sum(r['quantity_sold'] for r in row)
    tot_q = np.sum([r['quantity_total'] for r in row])
    perc_sold = sold/tot_q
    return {'cost': average_cost , 'quantity':tot_q, 'num_sold': sold, 'percent_sold':perc_sold}

def make_ticket_df(x):
    return x.apply(ticket_types, axis=1, result_type='expand')   

### concat num value df and ticket df
def concat_both(x_numarical,x2)
#data = pd.concat([data,new_cols],axis=1)



if __name__=='__main__':
    
    sample = pd.read_csv('../data/test_script_examples.csv',nrows=1)
    col_name = col_names(sample)
    df = numerical_df(sample,col_name)


