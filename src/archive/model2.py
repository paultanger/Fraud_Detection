'''
this random forest model will over sample training data to obtain balanced classes 
then predict and score on the unbalanced data we will typically see
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
from sklearn.tree import DecisionTreeClassifier
from predict import * 

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
    pass
    # cleaned_sample = all_together('../data/api_data.csv')

    #---    GET DATA & CONCAT 
    num_x = pd.read_csv("../data/number_df.csv").drop('Unnamed: 0', axis = 1)
    y = pd.read_csv("../data/number_target.csv").drop('Unnamed: 0', axis = 1)
    ticket = pd.read_csv('../data/ticket_type_df.csv').drop('Unnamed: 0', axis = 1)
    ticket.fillna(0, inplace = True)
    ticket = ticket.replace(np.inf, 110)
    X = pd.concat([num_x, ticket],axis=1)

    # #---    GET TTS THEN OVER SAMPLE     
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    x_o, y_o = oversample(X_train.values, np.ravel(y_train.values), 0.5)

    # #---    RUN MODEL    
    # rf_score2, rf_matrix2, f1_2, model2 = random_forest(x_o, X_test, y_o, y_test, 200, 'sqrt')

    # #---    HEATMAP    
    group_names = ['True Neg','False Pos','False Neg','True Pos']
    group_counts = ['{0:0.0f}'.format(value) for value in
                rf_matrix2.flatten()]
    group_percentages = ['{0:.2%}'.format(value) for value in
                     rf_matrix2.flatten()/np.sum(rf_matrix2)]
    labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(rf_matrix2, annot=labels, fmt='', cmap='Blues')
    plt.show();
