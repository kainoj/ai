import sys
import queue

GOAL = 'G'
START = 'S'
GOST = 'B'      # Both goal and start
WALL = '#'

class ComaState:
    def __init__(self, states, dir = "B", prev = None):
        """
        `state` is a set of states of possible commando positions
        """
        self.state = states
        self.depth = 0 if prev is None else prev.depth + 1
        self.prev = prev
        self.dir = dir;

    def add(self, states):
        self.state = self.state | states
        return self

    def __hash__(self):
        return hash(tuple(sorted(self.state)))
    
    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return ', '.join(["({} {})".format(x,y) for x,y in self.state])

    def __repr__(self):
        return self.__str__()


class Commando:
    
    DIR = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1), "B": (0, 0)}
    MOVES = ["U", "D", "L", "R"]

    def __init__(self, board, uncert=False):
        self.board, self.goals, self.starts = self.stripBoard(board)

        self.n = 20

        self.initState = ComaState(self.starts)

        if uncert:
            print('przed')
            print(self)
            self.initState = self.uncertainty(self.initState)
            self.initState.depth = 0

    def stripBoard(self, board):
        """
        Return values:
            board : [[]]        a board with '.' and '#' only
            goals : set()       a set of tuples of goals
            starts : set()      a set of tuples of start fields
        """
        starts = []
        goals = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == GOAL:
                    goals.append((i, j))
                    board[i][j] = ' '
                if board[i][j] == START:
                    starts.append((i, j))
                    board[i][j] = ' '
                if board[i][j] == GOST:
                    starts.append((i, j))
                    goals.append((i, j))
                    board[i][j] = ' '
        return board, set(goals), set(starts)

    def comaToStr(self):
        b =  [b[:] for b in self.board]
        for i, j in self.initState.state: b[i][j] = START
        for i, j in self.goals: b[i][j] = GOAL
        for i, j in self.goals & self.initState.state: b[i][j] = GOST
        return b
    
    def __str__(self):
        return '\n'.join([''.join(row) for row in self.comaToStr()])
    
    def __repr__(self):
        return self.__str__()

    def move(self, state, move):
        x, y = state[0] + self.DIR[move][0], state[1] + self.DIR[move][1]
        return (x, y) if self.board[x][y] != WALL else state

    def getNeighbour(self, comaState, move):
        return ComaState({self.move(s, move) for s in comaState.state}, move, comaState)

    def uncertainty(self, state):
        for i in range(self.n):
            ans = dict((m, len(self.getNeighbour(state, m).state)) for m in self.MOVES)
            state = self.getNeighbour(state, min(ans, key=ans.get))
        return state

    def isSolved(self, state):
        return state.state.issubset(self.goals)
        
    def traceback(self, state):
        ans = []
        while state.depth > 0:
            ans.append(state.dir)
            state = state.prev
        return ''.join(reversed(ans)) 

    def playBfs(self):
        state = self.initState

        q = queue.Queue()
        q.put(state)

        visited = set([state])

        while q.empty() == False and self.isSolved(state) == False:
            state = q.get()
            for move in self.MOVES:
                neigh = self.getNeighbour(state, move)
                if neigh not in visited:
                    q.put(neigh)
                    visited = visited | set([neigh])
        
        return self.traceback(state)




if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    if len(sys.argv) == 2:
        finput = sys.argv[1]
    
    board = []
    with open(finput) as f:
        board = [list(line.strip('\n')) for line in f]
    
    coma = Commando(board, uncert=True)
    
    print(coma)
    ans = coma.playBfs()
    print(ans)
    fout = open(foutput,"w")
    print(ans, file=fout)