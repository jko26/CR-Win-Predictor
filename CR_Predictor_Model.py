#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:59:47 2024

@author: jko26
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from statistics import mean
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


def train(D):
    # D is a dataframe containing Win and Score columns as well as one-hot-encodings
    # of the two decks being played
    train, test = train_test_split(D, test_size = 0.2, random_state = 42) #random_state = 42 makes results reproducible
    train_features = train.iloc[:, 2:]
    train_labels = train["Win"]
    test_features = test.iloc[:, 2:]
    test_labels = test["Win"]
    
    #Model 1: Decision Tree Classifier
    tree_clf = DecisionTreeClassifier()
    #tree_clf.fit(train_features, train_labels)
    
    #Use cross validation to assess effectiveness of a DTC
    dtc_scores = cross_val_score(tree_clf, train_features, train_labels, cv=10, scoring="accuracy")
    print("DTC Scores: " + str(mean(dtc_scores)))
    
    sgd_clf = SGDClassifier()
    #sgd_clf.fit(train_features, train_labels)
    
    #Use cross validation to assess effectiveness of a DTC
    sgd_scores = cross_val_score(sgd_clf, train_features, train_labels, cv=10, scoring="accuracy")
    print("SGD Scores: " + str(mean(sgd_scores)))
    
    logreg_clf = LogisticRegression()
    
    #Use cross validation to assess effectiveness of a DTC
    logref_scores = cross_val_score(logreg_clf, train_features, train_labels, cv=10, scoring="accuracy")
    print("Logistic Regression Scores: " + str(mean(logref_scores)))
    
    '''
    knn_clf = KNeighborsClassifier(n_neighbors=5)

    #Use cross validation to assess effectiveness of a DTC
    knn_scores = cross_val_score(knn_clf, train_features, train_labels, cv=10, scoring="accuracy")
    print("KNN Scores: " + str(mean(knn_scores)))
    '''
    
#def predict(D_test):
    
