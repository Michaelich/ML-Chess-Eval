#!/usr/bin/python3
# Konwertuje plik z partią szachową w notacji PGN do listy FEN-ów (po każdym ruchu)
# Wymagania: python-chess
# Jak wywołać: python [plik PGN - input] [lista FEN-ów - output]

import sys
import chess
import chess.pgn

with open(sys.argv[1],"r") as input_f,open(sys.argv[2],"w") as output_f:
    game=chess.pgn.read_game(input_f)
    board=chess.Board()

    for move in game.mainline_moves():
        board.push(move)
        output_f.write(board.epd()+'\n')

    

