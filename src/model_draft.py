import pandas as pd 
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

def Random_forest_model(X, y):
    rf_model = RandomForestClassifier().fit(X,y)
    return rf_model.score(X,y)


def Logistic_reg_model(X,y):
    LR = LogisticRegression().fit(X,y)
    return LR.score(X,y)

def KN_model(X,y, neigh):
    N_model = KNeighborsClassifier(n_neighbors=neigh).fit(X,y)
    return N_model.score(X,y)

if __name__=='__main__':
    X = #placeholder
    y = #placeholder

    Random_forest_model(X,y)
    Logistic_reg_model(X,y)
    KN_model(X,y,#placeholder)
     

