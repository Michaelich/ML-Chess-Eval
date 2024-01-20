#!/usr/bin/python3y
from stockfish import Stockfish
import typing as t
import numpy as np

def fen_convert(fen_positions: t.List[str]) -> t.List[str]:
    # Add your path to stockfish
    path = ""
    stockfish = Stockfish(path, depth=25, parameters={"Hash": 2048} )
    evaluations = np.zeros(len(fen_positions))
    for index, fen in enumerate(fen_positions):
        stockfish.set_fen_position(fen)
        evaluations[index] = stockfish.get_evaluation()['value']
    return evaluations

TEST_FEN = [
    "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1",
    " 8/8/8/4p1K1/2k1P3/8/8/8 b - - 0 1",
    "4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1",
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
    "8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50",
    "r1b1k2r/pp3ppp/5b2/K2p1n2/2N5/4nN2/Pp4qP/8 w kq - 8 21"
    ]

print(fen_convert(TEST_FEN))