import pandas as pd 
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, f1_score

def Random_forest_model(X, y, num_trees, num_features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)
    rf_model = RandomForestClassifier(n_estimators=num_trees, max_features=num_features)
    rf_model.fit(X_train, y_train)
    y_predict = rf_model.predict(X_test)
    score = rf_model.score(X_test,y_test)
    return score, confusion_matrix(y_test, y_predict), f1_score(y_test, y_predict), rf_model

def Logistic_reg_model(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    LR = LogisticRegression().fit(X_train, y_train)
    y_predict = LR.predict(X_test)
    confusion_matrix = confusion_matrix(y_test, y_pred)
    return LR.score(X_test, y_test), confusion_matrix

def KN_model(X,y, neigh):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    N_model = KNeighborsClassifier(n_neighbors=neigh).fit(X_train,y_train)
    y_predict = N_model.predict(X_test)
    confusion_matrix = confusion_matrix(y_test, y_pred)
    return N_model.score(X_test,y_test), confusion_matrix

def ROC_curve():
    fpr, tpr, _ = roc_curve()
    roc_auc = auc(fpr, tpr)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkturquoise',lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()
    pass

if __name__=='__main__':
    #-- Bringing in df and concat
    ticket = pd.read_csv('../data/ticket_type_df.csv').drop('Unnamed: 0', axis = 1)
    ticket.fillna(0, inplace = True)
    ticket = ticket.round(4)
    ticket = ticket.replace(np.inf, 110)
    num_df = pd.read_csv("../data/number_df.csv").drop('Unnamed: 0', axis = 1)
    y = pd.read_csv("../data/number_target.csv").drop('Unnamed: 0', axis = 1)
    X = pd.concat([num_df, ticket], axis=1)

    #--- RF round 2 with ticket added
    rf_score2, rf_matrix2, f1_2, model2 = Random_forest_model(X, y, 50, 'sqrt')

    #--- RF round 1 just X and y
    # rf_score1, rf_matrix1.ravel(), f1_1, model = Random_forest_model(X, y, 50, 'sqrt')
    # #0.978021978021978, ([[tn = 4285, fp = 20], [fn = 84, tp = 343]]), 0.8683544303797468, model
    # prob_lst = model.predict_proba(X)

    # Logistic_reg_model(X,y)
    # KN_model(X,y,#placeholder)
     

