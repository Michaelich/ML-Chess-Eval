import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import sklearn.ensemble


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

    line = input_f.read().split('\n')[:-1]
    print(len(line),'!')

    X_train = np.zeros((len(line),789))
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
        Y_train[idx] = (float(evaluation) - 0.5)*2

PCA=sklearn.decomposition.PCA(n_components=3)
X_train=PCA.fit_transform(X_train)

x=X_train[:, 0]
y=X_train[:, 1]
z=X_train[:, 2]
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                   marker=dict(size=2, color='blue'))])
# Update layout for a better view
fig.update_layout(title="3D Scatter Plot on a Unit Sphere",
                  scene=dict(
                      xaxis_title='X Axis',
                      yaxis_title='Y Axis',
                      zaxis_title='Z Axis'
                  ),
                  margin=dict(l=0, r=0, b=0, t=0))

# Show the plot
fig.show()
