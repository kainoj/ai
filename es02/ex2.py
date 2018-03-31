import queue
import heapq
import sys

'''
Stan - mapa globalnie + lista pudełek                       ← this one
    pros: memory
    cons: ain't easy: gen + render
'''

class SokoState:
    def __init__(self, keeper, boxes, dire = "B", prevState = None, h = 0):
        self.keeper = keeper
        self.boxes = boxes
        self.dir = dire 
        self.depth = 0 if prevState is None else prevState.depth + 1
        self.prev = prevState
        self.h = 42
        
    def __str__(self):
        return "STATE: Keeper {}, boxes {}\tcame from: {}".format(self.keeper, sorted(self.boxes), self.dir)
    
    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash("K{}B{}".format(self.keeper, sorted(self.boxes)))
    
    def __eq__(self, other):
        return self.keeper == other.keeper and self.boxes == other.boxes
    
    def __lt__(self, other):
        return self.h < other.h

class Sokoban:

    DIR = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1), "B": (0, 0)}
    MOVES = ["U", "D", "L", "R"]

    def __init__(self, board):

        self.board, self.goals, self.state = self.stripBoard(board)
        
        self.n, self.m = len(board), len(board[0])

        # Exclude `goals` from corners
        self.corners = self.precomputeCorners() - self.goals

    
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

        return board, set(goals), SokoState(keeper, set(boxes))
    
    def precomputeCorners(self):
        """
        For a given board return a set of a free fields which are corrners 
        (are '.' and are surrounded by 3x 'W')
        """
        b = self.board
        corners = []
        for i in range(1, self.n - 1):
            for j in range(1, self.m - 1):
                if board[i][j] == '.':
                    tl, tt, tr = b[i-1][j-1], b[i-1][j], b[i-1][j+1]
                    ml,     mr = b[i][j-1],              b[i][j+1]
                    bl, bb, br = b[i+1][j-1], b[i+1][j], b[i+1][j+1]
                    LU = (ml == "W" and tl == "W" and tt == "W")
                    RU = (tt == "W" and tr == "W" and mr == "W")
                    LB = (ml == "W" and bl == "W" and bb == "W")
                    RB = (bb == "W" and br == "W" and mr == "W")
                    if LU or RU or LB or RB:
                        corners.append((i,j))
        return set(corners)

    def sokoToStr(self, state):
        # Copy the list
        board =  [b[:] for b in self.board]

        for i, j in state.boxes: board[i][j] = 'B'
        for i, j in self.goals: board[i][j] = 'G'
        for i, j in state.boxes & self.goals: board[i][j] = '*'
        
        keeper = 'K' if not (self.goals & set(state.keeper)) else '+'
        board[state.keeper[0]][state.keeper[1]] = keeper

        for i in range(self.n): board[i][0] = str(i)
        for j in range(self.m): board[0][j] = str(j)

        return '\n'.join([' '.join(row) for row in board])

    def __str__(self):
        return self.sokoToStr(self.state)

    def __repr__(self):
        return self.__str__()
    
    def printBoardOnly(self):
        print('\n'.join([' '.join(row) for row in list(self.board)]))

    def info(self):
        print("Keeper: {}".format(self.state.keeper))
        print("Golas: {}".format(sorted(self.goals)))
        print("Boxes: {}".format(sorted(self.state.boxes)))

    def isFree(self, xy, state):
        return self.board[xy[0]][xy[1]] == '.' and not (set([xy]) & state.boxes)
    
    def isBox(self, xy, state):
        return len(set([xy]) & state.boxes) > 0

    def neighbour(self, xy, move):
        """
        Neighbour of (x,y) towards `move`
        """
        return xy[0] + self.DIR[move][0], xy[1] + self.DIR[move][1]
    

    def genStates(self, state):
        
        for move in self.MOVES:
            # A field next to the keeper
            neigh = self.neighbour(state.keeper, move)
            
            # A filed towards move is FREE - let's move
            if self.isFree(neigh, state):
                yield SokoState(neigh, state.boxes, move, state)

            # The neighbour is a BOX - check if its neigbour free
            elif self.isBox(neigh, state):
                neigh2 = self.neighbour(neigh, move)
                if self.isFree(neigh2, state) and neigh2 not in self.corners:
                    yield SokoState(neigh, 
                                    state.boxes - set([neigh] ) | set([neigh2]), 
                                    move, state)
    
    def isSolved(self, state):
        return state.boxes == self.goals

    def traceback(self, state):
        ans = []
        while state.depth > 0:
            ans.append(state.dir)
            state = state.prev
        return ''.join(reversed(ans))

    def playBFS(self):
        state = self.state        
        q = queue.Queue()
        q.put(state)

        visited = set([state])
        
        while q.empty() == False and self.isSolved(state) == False:
            state = q.get()
            for s in self.genStates(state):
                if s not in visited:
                    q.put(s)
                    visited = visited | set([s])
    
        return self.traceback(state)

    def f(self, state):
        min_box_dist = 100000
        closest_box = None
        keeper = state.keeper

        # Distance from keeper to closest box
        for box in state.boxes:
            # Distance: keeper → a box
            keeper_box = abs(box[0] - keeper[0]) + abs(box[1] - keeper[1])
                
            # Distance: the box → the closest goal
            min_goal_dist = 10000
            for goal in self.goals:
                d = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                if d < min_goal_dist:
                    min_goal_dist = d
            
            keeper_box += min_goal_dist
            if keeper_box < min_box_dist:
                min_box_dist = keeper_box

        return min_box_dist + state.depth


    def playAstar(self):

        state = self.state        
        hq = []
  
        state.h = self.f(state)
        heapq.heappush(hq, state)

        visited = set([state])
        
        while hq and self.isSolved(state) == False:
            state = heapq.heappop(hq)
            for s in self.genStates(state):
                if s not in visited:
                    s.h = self.f(s)
                    heapq.heappush(hq, s)
                    visited = visited | set([s])
    
        return self.traceback(state)


if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'
    
    if len(sys.argv) == 2:
        finput = sys.argv[1]

    board = []
    with open(finput) as f:
        board = [list(line.strip('\n')) for line in f]

    soko = Sokoban(board)
    
    # print(soko)
    # soko.info()
    
    ans = soko.playAstar()
    fout = open(foutput,"w")
    print(ans, file=fout)

