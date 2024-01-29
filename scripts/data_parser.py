#!/usr/bin/python3y
from stockfish import Stockfish
import typing as t
import numpy as np


def sigmoid(p):
    return 1/(1+np.exp(-p*0.00368208))


def fen_convert(fen_positions: t.List[str]) -> t.List[str]:
    # Add your path to stockfish
    stockfish = Stockfish(r'C:\Users\bemic\Desktop\IT-Projekty\ML-Project\ML-Chess-Eval\stockfish\stockfish-windows-x86-64-modern.exe', depth=20, parameters={"Hash": 2048} )
    evaluations = np.zeros(len(fen_positions))
    stockfish.update_engine_parameters({'UCI_LimitStrength': False})
    for index, fen in enumerate(fen_positions):
        stockfish.set_fen_position(fen)
        eval = sigmoid(stockfish.get_evaluation()['value'])
        evaluations[index] = eval
    return evaluations
