
#!/usr/bin/python3

# Boosted trees z sklearna na naszych szachach

import itertools
import numpy as np
import scipy.stats as ss
import pandas as pd
import sklearn.ensemble
import sys
import os
import xgboost as xgb




with open(sys.argv[1],"r") as input_f:
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

    line = input_f.read().split('\n')[:-1]
    print(len(line),'!')

    X_train = np.zeros((len(line),789), dtype=object)
    Y_train = np.zeros(len(line))
    
    for idx, fen in enumerate(line):
        fen = fen.replace('\t', ' ')
        # print(fen.split(" "))
        try:
            pos, turn, castling, en_passant, evaluation = fen.split(" ")
        except:
            raise ValueError(f"{idx} <- {fen}")
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
        Y_train[idx] = float(evaluation)

idxs=[]
# X_train=X_train.reshape(-1,789)

with open('numbers.txt') as f:
    n=0
    l=f.read()
    for i in l.split('\n'):
        try:
            x=int(i)
        except:
            break
        if n+x>len(X_train): break

        idxs+=[(n,n+x)]
        n+=x

np.random.shuffle(idxs)
idx1,idx2=[],[]

ratio=0.8

n=0
for i,j in idxs:
    n+=j-i
    if n>int(ratio*len(X_train)): 
        idx2+=[k for k in range(i,j)]
    else:
        idx1+=[k for k in range(i,j)]

print(X_train.shape)

PCA=sklearn.decomposition.PCA(n_components=125)
# X_train=PCA.fit_transform(X_train)

print(X_train.shape)

X_tr,Y_tr=X_train[idx1],Y_train[idx1]
X_test,Y_test=X_train[idx2],Y_train[idx2]

print(len(X_tr),len(X_test))

BoostTrees = xgb.XGBRegressor(tree_method='hist',learning_rate=0.1,device='cuda',n_estimators=200,num_parallel_tree=1,max_depth=100,reg_alpha=0,reg_lambda=20)

BoostTrees.fit(X_tr, Y_tr)

# Ys=BoostTrees.predict(X_test)

from stockfish import Stockfish
stockfish = Stockfish(r'/usr/bin/stockfish', depth=20, parameters={"Hash": 2048} )
stockfish.update_engine_parameters({'UCI_LimitStrength': False})

print("Training done.")
while True:
    fen = input()

    try:
        fen = fen.replace('\t', ' ')
        # print(fen.split(" "))
        pos, turn, castling, en_passant = fen.split(" ")
           
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

        stockfish.set_fen_position(fen)
        
        print(f"Evaluation by model: {BoostTrees.predict(Board.reshape(1,-1))}")

        def sigmoid(p):
            return 1/(1+np.exp(-p*0.00368208))

        print(f"Evaluation by Stockfish: {sigmoid(stockfish.get_evaluation()['value'])}")
    
    except Exception as e:
        print(e)
        continue


