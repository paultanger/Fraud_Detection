'''
model trained with provided json file
tested on api data
'''
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import metrics
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, f1_score, plot_roc_curve

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

if __name__ == "__main__":
    given = pd.read_json('../data.json')
    api = pd.read_csv("../data/api_data.csv")

    #find columns in given not api
    given_not_api = []
    for c in given.columns:
        if c not in api.columns:
            given_not_api.append(c)

    #bring in number df from original work
    num_x = pd.read_csv("../data/number_df.csv").drop('Unnamed: 0', axis = 1)
    y = pd.read_csv("../data/number_target.csv").drop('Unnamed: 0', axis = 1)

    #remove columns not in API, brings down to 22 columns
    num_x.drop(['gts','approx_payout_date', 'num_order', 'num_payouts', 'sale_duration2'], axis = 1, inplace = True) 

    X_train, X_test, y_train, y_test = train_test_split(num_x, y, test_size=0.25, random_state=42, stratify=y)
    x_o, y_o = oversample(X_train.values, np.ravel(y_train.values), 0.5)
    rf_score, rf_matrix, f1, model = random_forest(x_o, X_test, y_o, y_test, 200, 'sqrt')

    group_names = ['True Neg','False Pos','False Neg','True Pos']
    group_counts = ['{0:0.0f}'.format(value) for value in
                rf_matrix.flatten()]
    group_percentages = ['{0:.2%}'.format(value) for value in
                     rf_matrix.flatten()/np.sum(rf_matrix)]
    labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(rf_matrix, annot=labels, fmt='', cmap='Blues')
    plt.show();


    # load json to get nested json dicts
    with open('../data.json') as f:
        json_data = json.load(f)
    # unpack nested json of ticket types and prev payouts
    tix_types = pd.json_normalize(data=json_data, record_path='ticket_types', errors='ignore') 
    prev_pay_types = pd.json_normalize(data=json_data, record_path='previous_payouts', errors='ignore')

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    kfold = KFold(n_splits=5)
    accuracies = []
    precisions = []
    recalls = []
    for train_idx, test_idx in kfold.split(x_o):
        model = LogisticRegression()
        model.fit(x_o[train_idx], y_o[train_idx])
        y_pred = model.predict(x_o[test_idx])
        y_true = y_o[test_idx]
        accuracies.append(accuracy_score(y_true, y_pred))
        precisions.append(precision_score(y_true, y_pred))
        recalls.append(recall_score(y_true, y_pred))

    print(f"Accuracy: {np.average(accuracies):.3f}")
    print(f"Precision: {np.average(precisions):.3f}")
    print(f"Recall: {np.average(recalls):.3f}")