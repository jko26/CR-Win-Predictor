#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:53:49 2024

@author: jko26
@ ML Clash Royale win predictor
"""

import requests
#import json
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast

'''
Obtains raw data from Clash Royale's API and formats into a Datafram containing
columns representing the Player's Decks, Opponent's Decks, Score (in terms of crowns),
and Win or Loss. Decks are stored as lists of eight string card names. 
'''
def extract_data():
    opp_decks = [] #list of every opponent deck
    player_decks = [] #list of every player deck
    score = [] #score of the game in a list of len 2 representing crowns taken
    win = []

    #Obtain clan information from top clans in North America
    request_clan = requests.get("https://api.clashroyale.com/v1/locations/57000001/rankings/clans", 
                   headers={"Accept":"application/json", 
                            "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMDU5YjgxLTQyZWUtNDIwMy1iYjIwLWIyMjJkM2Y5NTc2YiIsImlhdCI6MTcwOTU3NDAwMSwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMjIwLjE1OS4yMTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.izSugOMj0Q4cwxUH0jLyiqCLKjUWeE97794sbSN8vbFSMmnr4mrykLH6xo9hL1jEtpgLipWvgLRdi8SN5viBkw"}, params = {"limit":1})
    clan_data = request_clan.json()
    df_clan = pd.DataFrame(clan_data["items"]) #df of top clans in North America
    for index, clan in df_clan.iterrows():
        
        clan_tag = clan["tag"].replace("#","%23") #Format tag to match the format of the API
        get_members_url = "https://api.clashroyale.com/v1/clans/" + clan_tag 
        request_members = requests.get(get_members_url, 
                       headers={"Accept":"application/json", 
                                "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMDU5YjgxLTQyZWUtNDIwMy1iYjIwLWIyMjJkM2Y5NTc2YiIsImlhdCI6MTcwOTU3NDAwMSwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMjIwLjE1OS4yMTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.izSugOMj0Q4cwxUH0jLyiqCLKjUWeE97794sbSN8vbFSMmnr4mrykLH6xo9hL1jEtpgLipWvgLRdi8SN5viBkw"}, params = {"limit":1})
        
        member_tags = request_members.json()["memberList"]
        for member in member_tags:
            
            member_tag = member["tag"].replace("#","%23")
            get_battles_url = "https://api.clashroyale.com/v1/players/" + member_tag + "/battlelog"
            request_battles = requests.get(get_battles_url, 
                           headers={"Accept":"application/json", 
                                    "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMDU5YjgxLTQyZWUtNDIwMy1iYjIwLWIyMjJkM2Y5NTc2YiIsImlhdCI6MTcwOTU3NDAwMSwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMjIwLjE1OS4yMTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.izSugOMj0Q4cwxUH0jLyiqCLKjUWeE97794sbSN8vbFSMmnr4mrykLH6xo9hL1jEtpgLipWvgLRdi8SN5viBkw"}, params = {"limit":1})
            
            battle_log = request_battles.json()
            
            for battle in battle_log:
                
                cards_team = battle["team"][0]["cards"]
                deck_team = []  # player's deck
                for card in cards_team:
                    deck_team.append(card["name"])
                    
                deck_opp = [] # opponent's deck
                cards_opp = battle["opponent"][0]["cards"]
                for card in cards_opp:
                    deck_opp.append(card["name"])
                
                crowns_team = battle["team"][0]["crowns"] #crowns taken by the player
                crowns_opp = battle["opponent"][0]["crowns"] #crowns taken by opponent
                
                opp_decks.append(deck_opp) 
                player_decks.append(deck_team)
                
                score.append([crowns_team, crowns_opp])
                win.append(int(crowns_team > crowns_opp)) # note that this doesn't account for ties (I'm assuming ties are too rare to necessitate needing to account for them)
                
    return pd.DataFrame({"Opponent's deck":opp_decks, "Player's deck":player_decks, "Crowns taken":score, "Win":win})


'''
One-hot-encodes the dataframe from CR_Dataloader to convert the representation
of decks as lists of eight string card names to numerical data where the presence
of a 1 indicates the presence of the card in the deck
'''
def OneHotEncode(df_raw):
    #Use one-hot-encoding on to convert decks into numerical data
    mlb = MultiLabelBinarizer()

    #Obtain a list of all 110 possible cards
    #ALL_CARDS = list(set(item for sublist in (ast.literal_eval(s) for s in list(df_raw["Player's deck"])) for item in sublist))
    ALL_CARDS = ['Guards', 'Skeleton Army', 'Zap', 'Hunter', 'Witch', 'Ice Spirit', 'Fireball', 'Electro Wizard', 'Ice Golem', 'Princess', 'Monk', 'Balloon', 'Rascals', 'Goblin Gang', 'Mortar', 'Electro Spirit', 'Fire Spirit', 'Executioner', 'Bowler', 'Bomber', 'Bomb Tower', 'Fisherman', 'Spear Goblins', 'Tornado', 'Little Prince', 'Musketeer', 'Goblin Hut', 'Clone', 'Arrows', 'Goblin Giant', 'Flying Machine', 'Wall Breakers', 'Heal Spirit', 'Miner', 'Graveyard', 'Giant Skeleton', 'Archer Queen', 'Minion Horde', 'Golden Knight', 'The Log', 'P.E.K.K.A', 'Skeleton Barrel', 'Royal Ghost', 'Tombstone', 'Phoenix', 'Royal Recruits', 'Skeleton Dragons', 'Skeleton King', 'Archers', 'Rage', 'Sparky', 'Baby Dragon', 'Elixir Collector', 'Golem', 'Minions', 'Giant Snowball', 'Zappies', 'Mother Witch', 'Freeze', 'Giant', 'Bats', 'Firecracker', 'Earthquake', 'Royal Hogs', 'Poison', 'Three Musketeers', 'Elixir Golem', 'Bandit', 'Inferno Dragon', 'Magic Archer', 'Wizard', 'Goblin Cage', 'Ice Wizard', 'Night Witch', 'Valkyrie', 'Mighty Miner', 'Mega Minion', 'Inferno Tower', 'Mega Knight', 'X-Bow', 'Mirror', 'Barbarians', 'Barbarian Barrel', 'Goblin Barrel', 'Mini P.E.K.K.A', 'Lava Hound', 'Dart Goblin', 'Ram Rider', 'Cannon', 'Elite Barbarians', 'Battle Ram', 'Knight', 'Barbarian Hut', 'Lumberjack', 'Lightning', 'Battle Healer', 'Prince', 'Hog Rider', 'Furnace', 'Skeletons', 'Electro Giant', 'Rocket', 'Goblin Drill', 'Tesla', 'Royal Delivery', 'Goblins', 'Cannon Cart', 'Royal Giant', 'Dark Prince', 'Electro Dragon']

    #format the decks into a list of lists to appease MLB's fit_transform function
    player_list_of_lists = [ast.literal_eval(s) for s in df_raw.pop("Player's deck")]
    opp_list_of_lists = [ast.literal_eval(s) for s in df_raw.pop("Opponent's deck")]

    #Create a new Dataframe containing the one-hot-encoded player and opponent decks
    df = df_raw.join(pd.DataFrame(
        mlb.fit_transform(player_list_of_lists),
        index=df_raw.index,
        columns=ALL_CARDS))

    df = df.join(pd.DataFrame(
        mlb.fit_transform(opp_list_of_lists),
        index=df_raw.index,
        columns=ALL_CARDS), how = 'left', lsuffix='_Player', rsuffix='_Opponent')
    
    return df
            
            
