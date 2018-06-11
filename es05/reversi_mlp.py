from reversi import Board, ReversiState, MAX
from reversi_heur import balance, close_corner_penalty, corners_bonus, field_bonus
from sklearn.neural_network import MLPClassifier
import random


def read_data(filename):
    lines = [line.rstrip('\n').replace('_', '2').split(' ') 
             for line in open(filename)]
    random.shuffle(lines)

    X_data = [[int(x) for x in i] for i in [list(line[1]) for line in lines]]
    y_data = [int(line[0]) for line in lines]

    return list(zip(X_data, y_data))

def convert(state):
    """
    Convert a given reversi state to a vector of features
    """
    b = [None if x==2 else x for x in state]
    brd = [b[i:i+8] for i in range(0, 64, 8)]
    fields = {(i, j) for i in range(8) for j in range(8) if brd[i][j] is None}

    s = ReversiState(brd, fields, MAX, None, None)

    # Mobility balance
    mobility_1 = len(s.moves())
    s = s.do_move(None)
    mobility_2 = len(s.moves())

    # Features    
    bal = balance(brd)        # Coins
    cor = corners_bonus(brd)  # Corners
    clo = close_corner_penalty(brd)
    mob = mobility_1 - mobility_2
    ply = sum([1 for i in range(8) for j in range(8) if brd[i][j] is not None])
    bon = field_bonus(brd, MAX)
   
    return [bal, cor, clo, bon, mob, ply] + state 

if __name__ == "__main__":

    features = True    
    train_factor = 0.66

    data = read_data('data/test.dat')
    random.shuffle(data)
    print(data)
    X_data, y_data = zip(*data)

    N = round(train_factor * len(X_data))

    if features:
        X_data = [convert(x) for x in X_data]
    
    X_train = X_data[:N]
    y_train = y_data[:N]

    X_test = X_data[N:]
    y_test = y_data[N:]
    
    print('Data size: {}'.format(len(X_data)))
    print('Train data size: {} ({})'.format(N, train_factor))
    print('learning {}...\n'.format("features" if features else "states"))

    # creating and then training the model
    nn = MLPClassifier(hidden_layer_sizes=(10, 60, 10))
    nn.fit(X_train, y_train)
    
    print('Train score {}'.format(nn.score(X_train, y_train)))
    print('Test score {}'.format(nn.score(X_test, y_test)))
    
    # Classify a random data chosen from test set
    i = random.randint(0, len(X_test))
    sample_x = X_test[i]
    sample_y = y_test[i]

    probabilities = nn.predict_proba([sample_x])
    print('Tried to classify: {}'.format(sample_y))
    print("{}\t→ prob = {}".format(nn.classes_[0], probabilities[0][0]))
    print("{}\t→ prob = {}".format(nn.classes_[1], probabilities[0][1]))