from reversi import Board, ReversiState
from sklearn.neural_network import MLPClassifier
import random


if __name__ == "__main__":
    
    datafile = 'data/smaller.dat'
    lines = [line.rstrip('\n').replace('_', '2').split(' ') for line in open(datafile)]

    N = round(len(lines)/6)
    print(N)

    X_data = [[int(x) for x in i] for i in [list(line[1]) for line in lines]]
    y_data = [int(line[0]) for line in lines]
    
    X_dev = X_data[:N]
    y_dev = y_data[:N]

    X_test = X_data[N:]
    y_test = y_data[N:]
    
    # creating model
    nn = MLPClassifier(hidden_layer_sizes=(60 ,60 ,10))
    
    # training model
    nn.fit(X_dev, y_dev)
    
    print('Dev score {}'.format(nn.score(X_dev, y_dev)))
    print('Test score {}'.format(nn.score(X_test, y_test)))
    
    x = random.choice(X_test)
    probabilities = nn.predict_proba ([ x ])
    prob0 = probabilities[0][0]
    prob1 = probabilities[0][1]

    print("Prob0 = {}\nProb1 = {}".format(prob0, prob1))