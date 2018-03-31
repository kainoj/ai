import sys


"""
.   puste pole, 
W   ścianę, 
K   magazyniera, 
B   skrzynkę, 
G   pole docelowe, 
*   skrzynkę na polu docelowym 
+   magazyniera stojącego na polu docelowym
"""

'''
Stan - mapa, na której zaznaczone są boxy i worker
    pros: easy state generation, easy rendering
    cons: memory

vs

Stan - mapa globalnie + lista pudełek                       ← this one
    pros: memory
    cons: ain't easy: gen + render
'''
class SokoState:
    def __init__(self, keeper, boxes, depth, dir):
        self.keeper = keeper
        self.boxes = boxes
        self.depth = depth
        self.dir = dir
    
    def __str__(self):
        return "STATE: Keeper {}, boxes {}\tcame from: {}".format(self.keeper, sorted(self.boxes), self.dir)
    def __repr__(self):
        return self.__str__()

class Sokoban:

    DIR = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1), "B": (0, 0)}
    MOVES = ["U", "D", "L", "R"]

    def __init__(self, board):

        self.board, self.goals, self.state = self.stripBoard(board)
        
        self.n, self.m = len(board), len(board[0])

        self.boxes = self.state.boxes
        self.keeper = self.state.keeper
    
    def stripBoard(self, board):
        """
        Return values:
            board : [[]]               a board with '.' and '#' only
            goals : set()              a set of tuples of goals
            state : SokoState          a initial state with depth = 0
        """
        keeper = (0, 0)
        boxes = []
        goals = []

        for i in range(len(board)):
            for j in range(len(board[0])):

                if board[i][j] == 'K':
                    keeper = (i, j)
                    board[i][j] = '.'
                elif board[i][j] == 'B':
                    boxes.append((i, j))
                    board[i][j] = '.'
                elif board[i][j] == 'G':
                    goals.append((i, j))
                    board[i][j] = '.'
                elif board[i][j] == '*':
                    goals.append((i, j))
                    boxes.append((i, j))
                    board[i][j] = '.'
                elif board[i][j] == '+':
                    goals.append((i, j))
                    keeper = (i, j)
                    board[i][j] = '.'
        return board, set(goals), SokoState(keeper, set(boxes), 0, "B")


        
    def __str__(self):
        # Copy the list
        board =  [b[:] for b in self.board]

        for i, j in self.boxes: board[i][j] = 'B'
        for i, j in self.goals: board[i][j] = 'G'
        for i, j in self.boxes & self.goals: board[i][j] = '*'
        
        keeper = 'K' if not (self.goals & set(self.keeper)) else '+'
        board[self.keeper[0]][self.keeper[1]] = keeper

        for i in range(self.n): board[i][0] = str(i)
        for j in range(self.m): board[0][j] = str(j)

        return '\n'.join([' '.join(row) for row in board])

    def __repr__(self):
        return self.__str__()
    
    def printBoardOnly(self):
        print('\n'.join([' '.join(row) for row in list(self.board)]))

    def info(self):
        print("Keeper: {}".format(self.keeper))
        print("Boxes: {}".format(sorted(self.boxes)))
        print("Golas: {}".format(sorted(self.goals)))

    def isFree(self, xy):
        return self.board[xy[0]][xy[1]] == '.' and not (set([xy]) & self.boxes)
    
    def isBox(self, xy):
        return len(set([xy]) & self.boxes) > 0

    def neighbour(self, xy, move):
        """
        Neighbour of (x,y) towards `move`
        """
        return xy[0] + self.DIR[move][0], xy[1] + self.DIR[move][1]


    def genStates(self, state):
        
        for move in self.MOVES:
            # A field next to the keeper
            neigh = self.neighbour(state.keeper, move)

            if self.isFree(neigh):
                # A filed towards move is FREE - let's move
                yield SokoState(neigh, state.boxes, state.depth + 1, move)
            elif self.isBox(neigh):
                # The neighbour towards move is a BOX - check if it's free
                # Check if neighbour of a box is a free field
                neigh2 = self.neighbour(neigh, move)
                if self.isFree(neigh2):
                    yield SokoState(neigh, 
                                    state.boxes - set([neigh] ) | set([neigh2]), 
                                    state.depth + 1, move)
    
    def play(self):
        print("TODO")

if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'
    
    if len(sys.argv) == 2:
        finput = sys.argv[1]

    board = []
    with open(finput) as f:
        board = [list(line.strip('\n')) for line in f]

    soko = Sokoban(board)
    
    print(soko)
    soko.info()
    for m in soko.genStates(soko.state):
        print(m)