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

def extract_data():
    
    opp_decks = [] #list of every opponent deck
    player_decks = [] #list of every player deck
    score = [] #score of the game in a list of len 2 representing crowns taken
    win = []

    request_clan = requests.get("https://api.clashroyale.com/v1/locations/57000001/rankings/clans", 
                   headers={"Accept":"application/json", 
                            "authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYzMDU5YjgxLTQyZWUtNDIwMy1iYjIwLWIyMjJkM2Y5NTc2YiIsImlhdCI6MTcwOTU3NDAwMSwic3ViIjoiZGV2ZWxvcGVyLzY0NThiM2ZmLWZjNDctODdmMi1hYjVmLWY4MTgzNzVmZjU3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMjIwLjE1OS4yMTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.izSugOMj0Q4cwxUH0jLyiqCLKjUWeE97794sbSN8vbFSMmnr4mrykLH6xo9hL1jEtpgLipWvgLRdi8SN5viBkw"}, params = {"limit":1})
    clan_data = request_clan.json()
    df_clan = pd.DataFrame(clan_data["items"]) #df of top clans in North America
    for index, clan in df_clan.iterrows():
        clan_tag = clan["tag"].replace("#","%23")
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

                
            
            
