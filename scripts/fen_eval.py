from data_parser import fen_convert
import sys
import numpy as np
import pandas as pd


with open(sys.argv[1],"r") as input_f:
    Arr = []
    line = input_f.read().split('\n')
    y_value = fen_convert(line)
    x_value = line
    d = {'FEN': x_value, 'Eval': y_value}
    dataset = pd.DataFrame(data=d)
    dataset.to_csv('data_after_parse.txt', sep='\t', index=False)
