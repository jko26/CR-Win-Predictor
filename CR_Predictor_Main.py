#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:45:44 2024

@author: jko26
"""
import CR_Dataloader
import CR_Predictor_Model
import pandas as pd

def main():
    ans = str(input("Fetch data from the CR API? Y/N: "))
    if ans == "Y":
        #Fetching real data from API
        df_raw = CR_Dataloader.extract_data() 
        df_raw.to_csv("deck_win_data.csv", index=False)
    else:
        #Use deck_win_data.csv to prevent needing to fetch API data when debugging
        df_raw = pd.read_csv('deck_win_data.csv')
    
    df = CR_Dataloader.OneHotEncode(df_raw)
    df.to_csv("ohe_data.csv", index=False)
    
    CR_Predictor_Model.train(df)
    

if __name__ == "__main__":
    main()