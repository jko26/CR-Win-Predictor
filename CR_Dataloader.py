#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:53:49 2024

@author: jko26
@ ML Clash Royale win predictor
"""

import requests
import json
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast
from torch.utils.data import Dataset, DataLoader
import torch
import pdb
import os

LOCAL_DATA_PATH = 'clash_royale_data.json'

'''
Obtains raw data from Clash Royale's API and formats into a Datafram containing
columns representing the Player's Decks, Opponent's Decks, Score (in terms of crowns),
and Win or Loss. Decks are stored as lists of eight string card names. 
'''
class BattleDataset(Dataset):
    def __init__(self, player_deck, opp_deck, win):
        """
        Initialize the dictionaries, sequences, and labels for the dataset
        """
        self.player_deck = player_deck
        self.opp_deck = opp_deck
        self.win = win

                    
    def __len__(self):
        return len(self.win)

    def __getitem__(self, idx):
        return (torch.tensor(self.player_deck[idx]), torch.tensor(self.opp_deck[idx]), torch.tensor(self.win[idx]))




def extract_data(card_to_idx):
    next_card_num = 0
    opp_decks = [] #list of every opponent deck
    player_decks = [] #list of every player deck
    score = [] #score of the game in a list of len 2 representing crowns taken
    win = []

    if os.path.exists(LOCAL_DATA_PATH):
        # Load data from the local file if it exists
        with open(LOCAL_DATA_PATH, 'r') as f:
            saved_data = json.load(f)
            opp_decks = saved_data["opp_decks"]
            player_decks = saved_data["player_decks"]
            score = saved_data["score"]
            win = saved_data["win"]
            card_to_idx = saved_data["card_to_idx"]
            next_card_num = saved_data["next_card_num"]

    else:
        #Obtain clan information from top clans in North America
        request_clan = requests.get("https://api.clashroyale.com/v1/locations/57000001/rankings/clans", 
                    headers={"Accept":"application/json", 
                                "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZjliOGIwLWI4N2MtNGVjZC1iZTVlLTdkYjA3MzU4YzM1YiIsImlhdCI6MTcyMTY5NDU4MCwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzQuMTcyLjEzNS43Il0sInR5cGUiOiJjbGllbnQifV19.KrsIJjoAW6OCUUZ_GCa8EYtArZprdLbq8z8uK6nJgUruuwyp0R74lWDsZqk0_C4w9fT7C7hy1cfhJtXvZtWezw"}, params = {"limit":50})
        clan_data = request_clan.json()
        #pdb.set_trace()
        df_clan = pd.DataFrame(clan_data["items"]) #df of top clans in North America
        for index, clan in df_clan.iterrows():
            
            clan_tag = clan["tag"].replace("#","%23") #Format tag to match the format of the API
            get_members_url = "https://api.clashroyale.com/v1/clans/" + clan_tag 
            request_members = requests.get(get_members_url, 
                        headers={"Accept":"application/json", 
                                    "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZjliOGIwLWI4N2MtNGVjZC1iZTVlLTdkYjA3MzU4YzM1YiIsImlhdCI6MTcyMTY5NDU4MCwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzQuMTcyLjEzNS43Il0sInR5cGUiOiJjbGllbnQifV19.KrsIJjoAW6OCUUZ_GCa8EYtArZprdLbq8z8uK6nJgUruuwyp0R74lWDsZqk0_C4w9fT7C7hy1cfhJtXvZtWezw"}, params = {"limit":30})
            
            member_tags = request_members.json()["memberList"]
            for member in member_tags:
                
                member_tag = member["tag"].replace("#","%23")
                get_battles_url = "https://api.clashroyale.com/v1/players/" + member_tag + "/battlelog"
                request_battles = requests.get(get_battles_url, 
                            headers={"Accept":"application/json", 
                                        "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZjliOGIwLWI4N2MtNGVjZC1iZTVlLTdkYjA3MzU4YzM1YiIsImlhdCI6MTcyMTY5NDU4MCwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzQuMTcyLjEzNS43Il0sInR5cGUiOiJjbGllbnQifV19.KrsIJjoAW6OCUUZ_GCa8EYtArZprdLbq8z8uK6nJgUruuwyp0R74lWDsZqk0_C4w9fT7C7hy1cfhJtXvZtWezw"}, params = {"limit":20})
                
                battle_log = request_battles.json()
                
                for battle in battle_log:
                    
                    cards_team = battle["team"][0]["cards"]
                    deck_team = []  # player's deck
                    for card in cards_team:
                        if card["name"] in card_to_idx:
                            deck_team.append(card_to_idx[card["name"]])
                        else:
                            card_to_idx[card["name"]] = next_card_num
                            next_card_num += 1
                            deck_team.append(card_to_idx[card["name"]])
                    if len(deck_team) != 8:
                        continue
                        
                    deck_opp = [] # opponent's deck
                    cards_opp = battle["opponent"][0]["cards"]
                    for card in cards_opp:
                        if card["name"] in card_to_idx:
                            deck_opp.append(card_to_idx[card["name"]])
                        else:
                            card_to_idx[card["name"]] = next_card_num
                            next_card_num += 1
                            deck_opp.append(card_to_idx[card["name"]])

                    if len(deck_opp) != 8:
                        continue        
            
                    
                    crowns_team = battle["team"][0]["crowns"] #crowns taken by the player
                    crowns_opp = battle["opponent"][0]["crowns"] #crowns taken by opponent
                    
                    opp_decks.append(deck_opp) 
                    player_decks.append(deck_team)
                    
                    score.append([crowns_team, crowns_opp])
                    win.append(int(crowns_team > crowns_opp)) # note that this doesn't account for ties (I'm assuming ties are too rare to necessitate needing to account for them)
        
        # Save the fetched data to a local file
        with open(LOCAL_DATA_PATH, 'w') as f:
            json.dump({
                "opp_decks": opp_decks,
                "player_decks": player_decks,
                "score": score,
                "win": win,
                "card_to_idx": card_to_idx,
                "next_card_num": next_card_num
            }, f)
    
    return BattleDataset(player_decks, opp_decks, win), saved_data["card_to_idx"]

