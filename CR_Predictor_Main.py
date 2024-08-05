#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:45:44 2024

@author: jko26
"""
import CR_Dataloader
import CR_Predictor_Model
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import pdb
import torch.nn as nn
import torch

from torch.utils.data import random_split



class CR_Classifier(nn.Module):
    def __init__(self, unique_cards, embedding_dim, hidden_dim):
        super(CR_Classifier, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.embedding_layer = nn.Embedding(unique_cards, embedding_dim)
        self.linear1 = nn.Linear(16 * embedding_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    """
        Perform the forward computation of the model (prediction), given batched input sentences.

        :param combined_decks: tensor of size (4, 16)
        :return tag_distribution: concatenated results from the hidden to out layers (batch_size, seq_len, tagset_size)
    """
    def forward(self, combined_decks):
        (batch_size, _) = combined_decks.shape
        #player_embeddings = self.embedding_layer(player_deck) #shape is (batch_size, 8, embedding_dim)
        #opp_embeddings = self.embedding_layer(opp_deck) #shape is (batch_size, 8, embedding_dim)
        #combined_embeds = torch.cat((player_embeddings, opp_embeddings), 1) #shape should be (batch_size, 16, embedding_dim)
        
        combined_embeds = self.embedding_layer(combined_decks)
        combined_embeds = combined_embeds.view(batch_size, 16 * self.embedding_dim) #shape should be (batch_size, 16 * embedding_dim)
        hidden = self.linear1(combined_embeds)
        output = self.sigmoid(self.linear2(hidden))

        return output

def train_one_epoch(epoch_index, model, dataloader, loss_fn, optimizer):
    running_loss = 0.
    last_loss = 0.

    for i, data in enumerate(dataloader):
        (player_deck, opp_deck, labels) = data
        optimizer.zero_grad()

        combined_decks = torch.cat((player_deck, opp_deck), 1)


        outputs = model(combined_decks) #shape of outputs is (4, 1)
        #pdb.set_trace()
        outputs = outputs[:, 0] #reshape to (4) 

        loss = loss_fn(outputs, labels.float())
        loss.backward()

        optimizer.step()

        running_loss += loss.item()
        if i % 1000 == 999:
            last_loss = running_loss / 1000 #loss per batch
            print('  batch {} loss: {}'.format(i + 1, last_loss))
            running_loss = 0.

    return last_loss


def train(train_dataloader, val_dataloader, model, optimizer, loss_fn, num_epochs: int):


    best_vloss = 1_000_000.

    for epoch in range(num_epochs):
        print('EPOCH {}:'.format(epoch + 1))

        # Make sure gradient tracking is on, and do a pass over the data
        model.train(True)
        avg_loss = train_one_epoch(epoch, model, train_dataloader, loss_fn, optimizer)


        running_vloss = 0.0
        # Set the model to evaluation mode, disabling dropout and using population
        # statistics for batch normalization.
        model.eval()

        # Disable gradient computation and reduce memory consumption.
        with torch.no_grad():
            for i, vdata in enumerate(val_dataloader):
                (vplayer_deck, vopp_deck, vlabels) = vdata

                vcombined_decks = torch.cat((vplayer_deck, vopp_deck), 1)

                voutputs = model(vcombined_decks)
                voutputs = voutputs[:, 0] #reshape to (4) 

                vloss = loss_fn(voutputs, vlabels.float())
                running_vloss += vloss

        avg_vloss = running_vloss / (i + 1)
        print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

        #epoch_number += 1



def main():
    #ans = str(input("Fetch data from the CR API? Y/N: "))
    #if ans == "Y":
        #Fetching real data from API
    card_to_idx = {}
    (dataset_raw, card_to_idx) = CR_Dataloader.extract_data(card_to_idx) 
    train_dataset, val_dataset = random_split(dataset_raw, [int(len(dataset_raw)*0.8), len(dataset_raw) - int(len(dataset_raw)*0.8)])
    train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=4, shuffle=False)

    unique_cards = len(card_to_idx)
    embedding_dim = 20
    hidden_dim = 100
    num_epochs = 30

    model = CR_Classifier(unique_cards, embedding_dim, hidden_dim)

    loss_fn = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    
    train(train_dataloader, val_dataloader, model, optimizer, loss_fn, num_epochs)

    

    

if __name__ == "__main__":
    main()