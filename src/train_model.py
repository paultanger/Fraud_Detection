'''
model trained with provided json file
'''
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import metrics
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, f1_score, plot_roc_curve, precision_recall_curve

def div_count_pos_neg(X, y):
    negatives, positives = y == 0, y == 1
    negative_count, positive_count = np.sum(negatives), np.sum(positives)
    X_positives, y_positives = X[positives], y[positives]
    X_negatives, y_negatives = X[negatives], y[negatives]
    return negative_count, positive_count, X_positives, \
           X_negatives, y_positives, y_negatives

def oversample(X, y, tp):
    """Randomly choose positive observations from X & y, with replacement
    to achieve the target proportion of positive to negative observations.

    Parameters
    ----------
    X  : ndarray - 2D
    y  : ndarray - 1D
    tp : float - range [0, 1], target proportion of positive class observations

    Returns
    -------
    X_undersampled : ndarray - 2D
    y_undersampled : ndarray - 1D
    """
    if 0.5 < np.mean(y):
        return X, y
    neg_count, pos_count, X_pos, X_neg, y_pos, y_neg = div_count_pos_neg(X, y)
    positive_range = np.arange(pos_count)
    positive_size = (tp * neg_count) / (1 - tp)
    positive_idxs = np.random.choice(a=positive_range,
                                     size=int(positive_size),
                                     replace=True)
    X_positive_oversampled = X_pos[positive_idxs]
    y_positive_oversampled = y_pos[positive_idxs]
    X_oversampled = np.vstack((X_positive_oversampled, X_neg))
    y_oversampled = np.concatenate((y_positive_oversampled, y_neg))

    return X_oversampled, y_oversampled

def random_forest(X_train, X_test, y_train, y_test, num_trees, num_features):
    rf_model = RandomForestClassifier(n_estimators = num_trees, max_features = num_features, max_depth = 7)
    rf_model.fit(X_train, y_train.ravel())
    y_predict = rf_model.predict(X_test)
    score = rf_model.score(X_test,y_test)
    return score, confusion_matrix(y_test, y_predict), f1_score(y_test, y_predict), rf_model

def fill_nan(df, cols):
    ''' takes df and col to fill nan value with 0 '''
    for col in cols:
        df[col].fillna(0, inplace = True)
    return df

def convert(row):
    ''' defines y col based on account types'''
    if row['acct_type'] == 'fraudster_event':
        val=True
    elif row['acct_type'] == 'fraudster':
        val=True
    elif row['acct_type'] == 'fraudster_att':
        val=True
    else:
        val=False
    return val

def fill_mean(x,col):
    x[col] = x[col].fillna(x[col].mean())

def fill_zero(x,col):
    x[col] = x[col].fillna(0)

if __name__ == "__main__":

    #---  ALTERNATIVE.. utilize data stored in db rather than in data/
    db_details = f'postgresql://postgres:{getpass()}@3.128.75.60:5432/fraud_data'
    engine = create_engine(db_details)
    num_x = pd.read_sql('select * from original_data', con=engine)
    # calculate y column
    num_x_copy = num_x.copy()
    num_x_copy['Fraud'] = num_x_copy.apply(convert, axis=1)
    y = num_x_copy['Fraud']

    # keep numerical cols
    cols = ['body_length',
    'channels',
    'delivery_method',
    'event_created',
    'event_end',
    'event_published',
    'event_start',
    'fb_published',
    'has_analytics',
    'has_header',
    'has_logo',
    'name_length',
    'object_id',
    'org_facebook',
    'org_twitter',
    'sale_duration',
    'show_map',
    'user_age',
    'user_created',
    'user_type',
    'venue_latitude',
    'venue_longitude']

    num_x = num_x[cols]
    # fill with mean or zero
    fill_mean(num_x,'delivery_method')
    fill_mean(num_x,'event_published')
    fill_mean(num_x,'has_header')
    fill_mean(num_x,'org_facebook')
    fill_mean(num_x,'org_twitter')
    fill_mean(num_x,'sale_duration')
    fill_zero(num_x,'venue_latitude')
    fill_zero(num_x,'venue_longitude')

    # num_x.fillna(0, inplace=True)

    # get tix types and prev payouts
    tix_types = pd.read_sql('select * from org_ticket_types', con=engine)
    tix_types = tix_types.groupby('event_id').agg({
                                        'cost':'sum',
                                        'quantity_total':'sum'}).reset_index()
    prev_pay_types = pd.read_sql('select * from org_previous_payouts', con=engine)
    prev_pay_types = prev_pay_types.groupby('event').agg({'amount':'sum'}).reset_index()

    # merge
    full = pd.merge(num_x, tix_types, how = 'left',  left_on = 'object_id', right_on = 'event_id')
    full.drop('event_id', axis = 1, inplace = True)   
    full = pd.merge(full, prev_pay_types, how = 'left',  left_on = 'object_id', right_on = 'event') 
    full.drop('event', axis = 1, inplace = True) 
    #replace NaN with 0 will represent they were not previously paid
    full = fill_nan(full, ['quantity_total', 'cost', 'amount'])
    #some infinity values exist
    full = full.replace([np.inf, -np.inf], 0) 

    # END VERSION USING DATA FROM DATABASE

    #---    DF SET UP
    #bring in number df from original work
    num_x = pd.read_csv("../data/number_df.csv").drop('Unnamed: 0', axis = 1) #rows = 14337
    y = pd.read_csv("../data/number_target.csv").drop('Unnamed: 0', axis = 1) #rows = 14337
    #remove columns not in API, brings down to 22 numerical columns
    num_x.drop(['gts','approx_payout_date', 'num_order', 
                'num_payouts', 'sale_duration2'], axis = 1, inplace = True) 
    #load json to get nested json dicts
    with open('../data/data.json') as f:
        json_data = json.load(f)

    #---    TIX_TYPES
    #unpack nested dictionary and groupby
    tix_types = pd.json_normalize(data=json_data, record_path='ticket_types', errors='ignore')
    tix_types = tix_types.groupby('event_id').agg({'cost':'sum',
                                                'quantity_total':'sum'}).reset_index() #rows = 14249
    full = pd.merge(num_x, tix_types, how = 'left',  left_on = 'object_id', right_on = 'event_id')
    #drop event to avoid duplicate columns
    full.drop('event_id', axis = 1, inplace = True)   

    #---    PREV_PAY_TYPES
    #unpack nested dictionary and groupby
    prev_pay_types = pd.json_normalize(data=json_data, record_path='previous_payouts', errors='ignore')
    prev_pay_types = prev_pay_types.groupby('event').agg({'amount':'sum'}).reset_index()
    #merge prev_pay_types onto num_x
    full = pd.merge(full, prev_pay_types, how = 'left',  left_on = 'object_id', right_on = 'event') 
    #drop event to avoid duplicate columns
    full.drop('event', axis = 1, inplace = True)
    #replace NaN with 0 will represent they were not previously paid
    full = fill_nan(full, ['quantity_total', 'cost', 'amount'])
    #some infinity values exist
    full.replace([np.inf, -np.inf], 0) 

    #---    MODEL + RESULTS 
    X_train, X_test, y_train, y_test = train_test_split(full, y, test_size=0.25, random_state=42, stratify=y)
    x_o, y_o = oversample(X_train.values, np.ravel(y_train.values), 0.5)
    rf_score, rf_matrix, f1, model = random_forest(x_o, X_test, y_o, y_test, 200, 'sqrt')

    #---    PICKLE MODEL
    import pickle
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    #---    HEATMAP
    group_names = ['True Neg','False Pos','False Neg','True Pos']
    group_counts = ['{0:0.0f}'.format(value) for value in
                rf_matrix.flatten()]
    group_percentages = ['{0:.2%}'.format(value) for value in
                     rf_matrix.flatten()/np.sum(rf_matrix)]
    labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(rf_matrix, annot=labels, 
                xticklabels=['Not Fraud', 'Fraud'], yticklabels=['Not Fraud','Fraud'], 
                fmt='', cmap='Blues')
    plt.title('Confusion Matrix \n Actual vs. Predicted')
    plt.show()

    #---    ROC CURVE
    metrics.plot_roc_curve(model, X_test, y_test)
    plt.show()

    # precision recall curve
    # https://www.kaggle.com/lct14558/imbalanced-data-why-you-should-not-use-roc-curve
    pred_prob = model.predict_proba(X_test)[:,1]
    p, r, _ = precision_recall_curve(y_test, pred_prob)
    fig, ax = plt.subplots(1,1, figsize=(10,10))
    ax.plot(r, p)
    ax.set_xlabel('Recall', fontsize=14)
    ax.set_ylabel('Precision', fontsize=14)
    ax.set_title('Precision Recall Curve', fontsize=16)
    # plt.show()
    plt.savefig('images/prec_recall_plot.png')