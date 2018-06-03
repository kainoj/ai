import random
import sys
import copy
from math import sqrt, log

M = 8
MAX = 1
MIN = 0
INF = 100000000
SIMULATIONS = 16

DEBUG = False

def initial_board():
    B = [[None] * M for i in range(M)]
    B[3][3] = MAX
    B[4][4] = MAX
    B[3][4] = MIN
    B[4][3] = MIN
    return B

def dprint(str=""):
    if DEBUG:
        print(str)

def dinput():
    if DEBUG:
        input()      


class ReversiState:

    def __init__(self, board, fields, player, parent, move):
        self.board = board
        self.fields = fields
        self.player = player
        self.opponent = 1 - player
        self.parent = parent
        self.move = move           # A move which led to this state
        self.children = []
        self.wins = 0
        self.playouts = 1
    
    def moves(self):
        """
        Get all possible moves in a current state
        """
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction) for direction in Board.dirs):
                res.append((x, y))
        if not res:
            return [None]
        return res
    
    def can_beat(self, x, y, d):
        """
        Get all possible beats of player
        """
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == self.opponent:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == self.player

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[y][x]
        return None

    def do_move(self, move):
        """
        Returns a new state which is the current state with an applied move
        """
        board = copy.deepcopy(self.board)
        fields = copy.deepcopy(self.fields)
        if move:   
            x, y = move
            x0, y0 = move
            board[y][x] = self.player
            fields -= set([move])
            for dx, dy in Board.dirs:
                x, y = x0, y0
                to_beat = []
                x += dx
                y += dy
                while self.get(x, y) == self.opponent:
                    to_beat.append((x, y))
                    x += dx
                    y += dy
                if self.get(x, y) == self.player:
                    for (nx, ny) in to_beat:
                        board[ny][nx] = self.player
        return ReversiState(board, fields, self.opponent, self, move)

    def terminal(self):
        """
        Determine wheater 
        """
        a = [x for x in self.moves() if x is not None]
        if not a:
            s = ReversiState(self.board, self.fields, self.opponent, self, None)
            opp_moves = s.moves()
            return not [y for y in opp_moves if y is not None]
        return False

    def __str__(self):
        toprint = []
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b is None:
                    res.append('.')
                elif b == MAX:
                    res.append('#')
                else:
                    res.append('o')
            toprint.append(''.join(res))
        return '\n'.join(toprint)

   

class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self, who_starts):
        b = initial_board()
        f = {(i, j) for i in range(M) for j in range(M) if b[i][j] is None}

        self.state = ReversiState(b, f, who_starts, None, None)

        # Total number of playouts
        self.N = 0  

    def __str__(self):
        return self.state.__str__()
    

    def balance(self, board):
        """
        balance = #black - #white
        """
        balance = 0
        for y in range(M):
            for x in range(M):
                b = board[y][x]
                if b == MAX:
                    balance += 1.0
                elif b == MIN:
                    balance -= 1.0
        return balance

    def random_move(self, state):
        moves = state.moves()
        if moves is None:
            return None
        return random.choice(moves)

    def random_game(self, root):
        state = ReversiState(copy.deepcopy(root.board),
                             copy.deepcopy(root.fields), 
                             root.player, None, None)
        while True:
            move = self.random_move(state)
            state = state.do_move(move)
            if state.terminal():
                if self.balance(state.board) > 0:
                    return MAX
                return MIN
    
    def Q(self, state):
        q = sqrt(2 * log(self.N) / state.playouts)
        return state.wins / state.playouts + q

    def tree_search(self, root):
        state = root
        
        # 1. Selection
        while state.children:
            # choose one child
            state = max(state.children, key=lambda s: self.Q(s))
        
        # 2. Expansion
        for move in state.moves():
            state.children.append(state.do_move(move))
        
        # 3. Simulation
        winner = self.random_game(random.choice(state.children))

        # 4. Back propagation
        while True:
            state.playouts += 1
            if state.player == winner:
                state.wins += 1
            if state == root:
                break
            state = state.parent
        
    def monte_carlo(self, root):

        for i in range(SIMULATIONS):
            self.tree_search(root)
            self.N += 1

        # Choose the best node
        best = min(root.children, key=lambda s: s.wins)
        return best.move

    def do_mtcs_move(self, move):
        """
        Doing a move in a mcts game requires traversing a game tree
        """
        s = None
        for child in self.state.children:
            if child.move == move:
                s = child
                break

        if s == None:
            s = self.state.do_move(move)
            self.state.children.append(s)
        return s

    def play(self):
        while True:
            if self.state.player == MAX:
                move = self.monte_carlo(self.state)
            else:
                move = self.random_move(self.state)

            dprint("Player{} moves".format(self.state.player))
            dprint("move: {}".format(move))
            dprint(self)
            dinput()

            self.state = self.do_mtcs_move(move)
            
            if (self.state.terminal()):
                if self.balance(self.state.board) > 0:
                    return MAX
                else:
                    return MIN

if __name__ == "__main__":

    rounds = 1

    if len(sys.argv) == 2:
        rounds = int(sys.argv[1])

    max_victories = 0
    min_victories = 0

    player = 0

    for i in range(rounds):
        b = Board(player)
        if( b.play() > 0 ):
            max_victories += 1
        else:
            min_victories += 1
        player = 1 - player
        print("max_victories: {} / {}".format(max_victories, i+1))
    
    print("min_victories: {}".format(min_victories))
    

