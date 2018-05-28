import random
import sys
import copy

M = 8
MAX = 1
MIN = 0
INF = 100000000

DEBUG = True

def initial_board():
    B = [[None] * M for i in range(M)]
    B[3][3] = MAX
    B[4][4] = MAX
    B[3][4] = MIN
    B[4][3] = MIN
    return B

def dprint(str=""):
    if DEBUG == True:
        print(str)

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
        self.playouts = 0
    
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

    def draw(self):
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
            dprint(''.join(res))
        dprint()

   

class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        b = initial_board()
        f = {(i, j) for i in range(M) for j in range(M) if b[i][j] is None}

        self.state = ReversiState(b, f, MAX, None, None)

    def draw(self):
        self.state.draw()
    

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

    def monte_carlo(self, root):
        state = root
        dprint("~~~~~~~~~ MONTE CARLO ~~~~~~~~~~\n")
        dprint("root: ")
        root.draw()

        # 1. Selection
        while state.children:
            # choose one child
            state = random.choice(state.children)  # todo: heuristic
        
        # 2. Expansion
        for move in state.moves():
            state.children.append(state.do_move(move))
        
        # 3. Simulation
        winner = self.random_game(random.choice(state.children))
        dprint("simulation won by player{}".format(winner))

        # 4. Back propagation
        while True:
            state.playouts += 1
            if state.player == winner:
                state.wins += 1
            if state == root:
                break
            state = state.parent
        
        best = max(state.children, key=lambda s: s.wins) # to change

        print("root wins: {}".format(state.wins))
        print("root playouts: {}".format(state.playouts))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        return best.move


    def play(self):
        while True:
            if self.state.player == MAX:
                move = self.monte_carlo(self.state)
            else:
                move = self.random_move(self.state)
            print("Player{} moves".format(self.state.player))
            print("move: {}".format(move))
            self.draw()
            input()

            s = None
            for child in self.state.children:
                if child.move == move:
                    s = child
                    break

            if s == None:
                s = self.state.do_move(move)
                self.state.children.append(s)
            
            self.state = s  
            
            if (self.state.terminal()):
                return

if __name__ == "__main__":

    rounds = 1

    if len(sys.argv) == 2:
        rounds = int(sys.argv[1])

    b = Board()
    b.play()