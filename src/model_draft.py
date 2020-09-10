import pandas as pd 
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix

def Random_forest_model(X, y, num_trees, num_features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, straify=y) 
    rf_model = RandomForestClassifier().fit(X_train, y_train, n_estimators=num_trees, max_features=num_features)
    y_predict = rf_model.predict(X_test)
    confusion_matrix = confusion_matrix(y_test, y_pred)
    return rf_model.score(X_test,y_test), confusion_matrix


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
    pass

if __name__=='__main__':
    X = #placeholder
    y = #placeholder

    Random_forest_model(X,y,#placeholder, #placehodler)
    Logistic_reg_model(X,y)
    KN_model(X,y,#placeholder)
     

