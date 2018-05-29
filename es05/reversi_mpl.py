from reversi import Board, ReversiState
from reversi_heur import balance, close_corner_penalty, corners_bonus
from sklearn.neural_network import MLPClassifier
import random


def read_data(filename):
    lines = [line.rstrip('\n').replace('_', '2').split(' ') 
             for line in open(filename)]
    random.shuffle(lines)

    X_data = [[int(x) for x in i] for i in [list(line[1]) for line in lines]]
    y_data = [int(line[0]) for line in lines]

    return  X_data, y_data

def convert(state):
    """
    Convert a given reversi state to a vector of features
    """
    b = [None if x==2 else x for x in state]
    # s = ReversiState([b[i:i+8] for i in range(0, 64, 8)], None, 0, None, None)
    board = [b[i:i+8] for i in range(0, 64, 8)]
    return [balance(board), corners_bonus(board), close_corner_penalty(board)]

if __name__ == "__main__":

    features = True    
    dev_factor = 0.75

    X_data, y_data = read_data('data/bigger.dat')
    N = round(dev_factor * len(X_data))

    if features:
        X_data = [convert(x) for x in X_data]
    
    X_dev = X_data[:N]
    y_dev = y_data[:N]

    X_test = X_data[N:]
    y_test = y_data[N:]
    
    print('Data size: {}'.format(len(X_data)))
    print('Dev data size: {} ({})'.format(N, dev_factor))
    print('learning {}...\n'.format("features" if features else "states"))

    # creating and then training the model
    nn = MLPClassifier(hidden_layer_sizes=(60, 60, 10))
    nn.fit(X_dev, y_dev)
    
    print('Dev score {}'.format(nn.score(X_dev, y_dev)))
    print('Test score {}'.format(nn.score(X_test, y_test)))
    
    # Classify a random data chosen from test set
    i = random.randint(0, len(X_test))
    sample_x = X_test[i]
    sample_y = y_test[i]

    probabilities = nn.predict_proba([sample_x])
    print('Tried to classify: {}'.format(sample_y))
    print("{}\t→ prob = {}".format(nn.classes_[0], probabilities[0][0]))
    print("{}\t→ prob = {}".format(nn.classes_[1], probabilities[0][1]))