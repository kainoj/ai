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

class Sokoban:

    DIR = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    MOVES = ["U", "D", "L", "R"]
    def __init__(self, board):
        self.board = board

        self.keeper = (0, 0)
        self.boxes = []
        self.goals = []

        self.n = len(board)
        self.m = len(board[0])
       
        for i in range(self.n):
            for j in range(self.m):

                if self.board[i][j] == 'K':
                    self.keeper = (i, j)
                    self.board[i][j] = '.'
                elif self.board[i][j] == 'B':
                    self.boxes.append((i, j))
                    self.board[i][j] = '.'
                elif self.board[i][j] == 'G':
                    self.goals.append((i, j))
                    self.board[i][j] = '.'
                elif self.board[i][j] == '*':
                    self.goals.append((i, j))
                    self.boxes.append((i, j))
                    self.board[i][j] = '.'
                elif self.board[i][j] == '+':
                    self.goals.append((i, j))
                    self.keeper = (i, j)
                    self.board[i][j] = '.'
        
        self.boxes = set(self.boxes)
        self.goals = set(self.goals)

        
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

    def isFree(self, x, y):
        return self.board[x][y] == '.' and not (set([(x,y)]) & self.boxes)
    
    def isBox(self, x, y):
        return len(set([(x, y)]) & self.boxes) > 0

    def neighbour(self, x, y, move):
        """
        Neighbour of (x,y) towards `move`
        """
        return x + self.DIR[move][0], y +self.DIR[move][1]


    def genMoves(self):
        kx, ky = self.keeper

        for move in self.MOVES:
            # A field next to the keeper
            nx, ny = self.neighbour(kx, ky, move)

            print("Checking: {} ({} {})".format(move, nx, ny))

            if self.isFree(nx, ny):
                # A filed towards move is FREE - let's move
                print("\tOh yea I can move to ({} {}) towards {}".format(nx, ny, move))
            elif self.isBox(nx, ny):
                # The neighbour towards move is a BOX - check if it's free
                # Check if neighbour of a box is a free field
                nnx, nny = self.neighbour(ny, ny, move)
                if self.isFree(nnx, nny):
                    print("\tOh yea I can move BOX to ({} {}) towards {}".format(nnx, nny, move))
            print()
    
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
    soko.genMoves()