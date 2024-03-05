#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:08:21 2024

@author: jko26
"""
import CR_Dataloader
#import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MultiLabelBinarizer

def main():
    #df_raw = CR_Dataloader.extract_data()
    #df_raw.to_csv('deck_win_data.csv')
    df_raw = pd.read_csv('deck_win_data.csv')
    
    #features = df_raw.loc[:, ["Opponent's deck", "Player's deck"]]
    #train_decks, test_decks, train_win, test_win = train_test_split(features, df_raw["Win"], test_size=0.2)
    
    #Use one-hot-encoding on to convert decks into numerical data
    
    '''
    #df_raw["Opponent's deck"].unique()
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')
    ohetransform = ohe.fit_transform(df_raw["Opponent's deck"].reshape(-1,1))
    print(ohetransform)
    '''
    
    mlb = MultiLabelBinarizer(sparse_output=False)
    df_ohe = df_raw.join(
            pd.DataFrame(
                mlb.fit_transform(df_raw.pop("Opponent's deck")),
                index=df_raw.index,
                columns=mlb.classes_))
    print(df_ohe)
    

if __name__ == "__main__":
    main()