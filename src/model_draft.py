import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, f1_score, plot_roc_curve
import pickle

def Random_forest_model(X, y, num_trees, num_features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    rf_model = RandomForestClassifier(n_estimators = num_trees, max_features = num_features)
    rf_model.fit(X_train, y_train.values.ravel())
    y_predict = rf_model.predict(X_test)
    score = rf_model.score(X_test,y_test)
    return score, confusion_matrix(y_test, y_predict), f1_score(y_test, y_predict), rf_model

def Logistic_reg_model(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    LR = LogisticRegression()
    LR.fit(X_train, y_train.values.ravel())
    y_predict = LR.predict(X_test)
    confusion_matrix = confusion_matrix(y_test, y_pred)
    return LR.score(X_test, y_test), confusion_matrix

def KN_model(X,y, neigh):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    N_model = KNeighborsClassifier(n_neighbors=neigh)
    N_model.fit(X_train,y_train.values.ravel())
    y_predict = N_model.predict(X_test)
    confusion_matrix = confusion_matrix(y_test, y_pred)
    return N_model.score(X_test,y_test), confusion_matrix

def balance_work(y_train):
    n1 = np.sum(y_train)
    n2 = len(y_train) - n1
    n_samples = n1 + n2
    w1 = n_samples / (2 * n1)
    w2 = n_samples / (2 * n2)
    return w1, w2

def feature_importance(model, names):
    feature_importances = 100 * model.feature_importances_ / np.sum(model.feature_importances_)
    feature_importances, feature_names, feature_idxs = \
    zip(*sorted(zip(feature_importances, names, range(len(names)))))
    width = 0.8
    idx = np.arange(len(names))
    plt.barh(idx, feature_importances, align='center')
    plt.yticks(idx, feature_names)

    plt.title("Feature Importances")
    plt.xlabel('Relative Importance of Feature', fontsize=14)
    plt.ylabel('Feature Name', fontsize=14)
    # plt.savefig('../images/feat_importances.png')

if __name__=='__main__':
    #-- Bringing in df and concat
    ticket = pd.read_csv('../data/ticket_type_df.csv').drop('Unnamed: 0', axis = 1)
    ticket.fillna(0, inplace = True)
    ticket = ticket.round(4)
    ticket = ticket.replace(np.inf, 110)
    num_df = pd.read_csv("../data/number_df.csv").drop('Unnamed: 0', axis = 1)
    y = pd.read_csv("../data/number_target.csv").drop('Unnamed: 0', axis = 1)
    X = pd.concat([num_df, ticket], axis=1)

    #--- Get weights
    # w1, w2 = balance_work(y_train)

    #--- RF round 2 with ticket added
    rf_score2, rf_matrix2, f1_2, model2 = Random_forest_model(X, y, 50, 'sqrt')
    # 0.9862637362637363, ([tn = 4292, fp = 13, fn = 52, tp = 375]), 0.9202453987730062

    #--- RF round 1 just X and y
    # rf_score1, rf_matrix1.ravel(), f1_1, model = Random_forest_model(X, y, 50, 'sqrt')
    #0.978021978021978, ([[tn = 4285, fp = 20], [fn = 84, tp = 343]]), 0.8683544303797468, model
    # prob_lst = model.predict_proba(X)

    # get features importances
    names = X.columns
    feature_importance(model2, names)
    plt.savefig('../images/feat_importances.png')
    plt.show()

    # roc plot
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)
    # plot_roc_curve(model2, X_test, y_test)
    # plt.show()

    # with open('../web_app/model2.pkl', 'wb') as f:
    #     # Write the model to a file.
    #     pickle.dump(model2, f)
     

