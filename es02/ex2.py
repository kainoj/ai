import sys

"""
.   puste pole, 
W   ścianę, 
K   magazyniera, 
B   skrzynkę, 
G   pole docelowe, 
*   skrzynkę na polu docelowym 
+   magazyniera stojącego na polu
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


        
    def __str__(self):
        board = list(self.board)
        for i, j in self.boxes: board[i][j] = 'B'
        for i, j in self.goals: board[i][j] = 'G'
        for i, j in set(self.boxes) & set(self.goals): board[i][j] = '*'
        
        keeper = 'K' if not (set(self.goals) & set(self.keeper)) else '+'
        board[self.keeper[0]][self.keeper[1]] = keeper
        return '\n'.join([''.join(row) for row in board])

    def __repr__(self):
        return self.__str__()
    
    def info(self):
        print("Worker: {}".format(self.keeper))
        print("Boxes: {}".format(self.boxes))
        print("Golas: {}".format(self.goals))

    def genMoves(self):
        print("TODO")
    
    def play(self):
        print("TOOOOODOOOO")

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