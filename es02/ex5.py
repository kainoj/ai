import ex4
import heapq
import queue
import sys
from random import sample
from math import sqrt

class Commando(ex4.Commando):

    def dist(self, a, b):
        """
        Manhattan distance
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def dist2(self, a, b):
        """
        Pythagorean distance
        Returns sqrt(a**2, b**2)
        """
        x = a[0] - b[0]
        y = a[1] - b[1]
        return sqrt(x*x + y*y)
    
    def avg(self, arr):
        return sum(arr) / len(arr)

    def computeF(self, state, goals):
        """
        Compute f = g + h  function, where:
            g - distance from initial state ( = self.depth )
            h - admissible heuristic function
        Returns the state with modiefied F.

        Note: F = g = self.depth is just an ordinary BFS
        """
        d = max([self.dists[s] for s in state.state])
       
        state.F = state.depth + d
        return state
    
    def preProcessDists(self):
        """
        For each field compute distance to the nearest goal
        """
        dists = {(n, m): 100000 for n in range(1, len(self.board) - 1) 
                 for m in range(1, len(self.board[0]) - 1) 
                 if self.board[n][m] != ex4.WALL}

        for g in self.goals:

            q = queue.Queue()
            q.put((g, 0))
            vis = set([g])

            while q.empty() is False:
                s, depth = q.get()

                if depth < dists[s]:
                    dists[s] = depth

                for m in self.MOVES:
                    neigh = self.move(s, m)
                    if neigh not in vis:
                        q.put((neigh, depth + 1))
                        vis = vis | set([neigh])
        return dists


    def astar(self):
        state = self.initState
        goals = self.goals

        self.dists = self.preProcessDists()

        hq = []
        heapq.heappush(hq, self.computeF(state, goals))

        visited = {}
        visited[state] = state.F

        while hq and self.isSolved(state) is False:
            state = heapq.heappop(hq)
            for move in self.MOVES:
                neigh = self.getNeighbour(state, move)
                neigh = self.computeF(neigh, goals)
                
                if neigh not in visited:
                    heapq.heappush(hq, neigh)
                    visited[neigh] = neigh.F
                else:
                    score = visited[neigh]
                    if neigh.F < score:
                        heapq.heappush(hq, neigh)

        return self.traceback(state)


if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    if len(sys.argv) == 2:
        finput = sys.argv[1]
    
    board = []
    with open(finput) as f:
        board = [list(line.strip('\n')) for line in f]

    coma = Commando(board)
    ans = coma.astar()
     
    # print(coma)
    print("{}".format(ans))

    fout = open(foutput,"w")
    print(ans, file=fout)