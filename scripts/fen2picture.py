import numpy as np
import sys


with open("data_after_parse.txt","r") as input_f:
    WHITE='PNBRQK'
    BLACK='pnbrqk'
    EMPTY='12345678'
    TURN={
        'w': 0,
        'b': 1
    }
    CASTLING={
        '-': 0,
        'K': 1,
        'Q': 2,
        'k': 3,
        'q': 4,
        'KQ': 5,
        'Kk': 6,
        'Kq': 7,
        'Qk': 8,
        'Qq': 9,
        'kq': 10,
        'KQk': 11,
        'KQq': 12,
        'Kkq': 13,
        'Qkq': 14,
        'KQkq': 15
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
        print(fen.split(" "))
        pos, turn, castling, en_passant, evaluation = fen.split(" ")
        Board = np.zeros(67, dtype=int)
        counter=0
        for line in pos.split('/'):
            for i in line:
                if i in WHITE:
                    Board[counter]=WHITE.index(i)+1
                    counter+=1
                elif i in BLACK:
                    Board[counter]=BLACK.index(i)+7
                    counter+=1
                else:
                    counter+=int(i)
        Board[64]=TURN[turn]
        Board[65]=CASTLING[castling]
        Board[66]=EN_PASSANT[en_passant]
        X_train[idx] = Board
        Y_train[idx] = evaluation
