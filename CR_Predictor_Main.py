#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:45:44 2024

@author: jko26
"""
import CR_Dataloader
import pandas as pd

def main():
    #Uncomment this line when fetching real data from API
    #df_raw = CR_Dataloader.extract_data() 
    
    #Use deck_win_data.csv to prevent needing to fetch API data when debugging
    df_raw = pd.read_csv('deck_win_data.csv')
    
    df = CR_Dataloader.OneHotEncode(df_raw)
    
    

if __name__ == "__main__":
    main()