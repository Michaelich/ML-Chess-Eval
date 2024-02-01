import numpy as np

def fen_to_picture(fen):
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
        'Kqk': 11,
        'KQq': 12,
        'Kkq': 13,
        'Qkk': 14,
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
    pos, turn, castling, en_passant=fen.split(' ')
    Board = np.zeros(67)
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
    return Board
