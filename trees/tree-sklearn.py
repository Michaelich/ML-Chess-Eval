
#!/usr/bin/python3

# Boosted trees z sklearna na naszych szachach

import itertools
import numpy as np
import scipy.stats as ss
import pandas as pd
import sklearn.ensemble
import sys
import os

with open("data_after_parse.txt","r") as input_f:
    WHITE='PNBRQK'
    BLACK='pnbrqk'
    EMPTY='12345678'
    TURN={
        'w': 0,
        'b': 1
    }

    EN_PASSANT={
        '-': 0,
        'a3': 1,
        'b3': 2,
        'c3': 3,
        'd3': 4,
        'e3': 5,
        'f3': 6,
        'g3': 7,
        'h3': 8,
        'a6': 9,
        'b6': 10,
        'c6': 11,
        'd6': 12,
        'e6': 13,
        'f6': 14,
        'g6': 15,
        'h6': 16,
    }

    line = input_f.read().split('\n')
    
    X_train = np.zeros(len(line), dtype=object)
    Y_train = np.zeros(len(line))
    
    for idx, fen in enumerate(line):
        fen = fen.replace('\t', ' ')
        # print(fen.split(" "))
        pos, turn, castling, en_passant, evaluation = fen.split(" ")
        Board = np.zeros(789, dtype=int) # 768, 1, 4, 16
        counter=0

        # Reprezentacja jest w 789 wymiarach 
        # Wymiary 0-767 <- jakie figury są na szachownicy i gdzie 
        # (pierwsze 64 wymiary: białe piony; reszta wedle konwencji na górze pliku)
        # Wymiar 768 <- czyj ruch
        # Wymiary 769-772 <- roszady
        # Wymiary 773-788 <- bicia w przelocie
        
        for line in pos.split('/'):
            for i in line:
                if i in WHITE:
                    n=WHITE.index(i)
                    Board[64*n+counter]=1
                    counter+=1
                elif i in BLACK:
                    n=BLACK.index(i)
                    Board[64*(6+n)+counter]=1
                    counter+=1
                else:
                    counter+=int(i)

        Board[768]=TURN[turn]

        for i,s in enumerate("KkQq"):
            if s in castling:
                Board[769+i]=1

        if en_passant!='-':
            Board[772+EN_PASSANT[en_passant]]=1

        X_train[idx] = Board
        Y_train[idx] = evaluation

BoostTrees = sklearn.ensemble.HistGradientBoostingRegressor(max_iter=50000)

BoostTrees.fit(list(X_train), Y_train)
print(f"Accuracy: {BoostTrees.score(list(X_train),Y_train)}")
