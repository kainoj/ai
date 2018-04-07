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
    
    def f_average(self, state, goals):
        """
        Average distance between each state and the nearest goal.
        Works pretty good, but still not efficient enough
        """
        s = ([min([self.dist2(g, s) for g in goals]) for s in state.state])
        return sum(s)/len(s)
    
    def f_max(self, state, goals):
        s = ([max([self.dist2(s, g) for g in goals]) for s in state.state])
        return max(s)
    
    def f_min(self, state, goals):
        s = ([min([self.dist2(s, g) for g in goals]) for s in state.state])
        return min(s)

    def centroid(self, points):
        return (sum(g[0] for g in points)/len(points), sum(g[1] for g in points)/len(points))
    
    def f_goals_centroid(self, state, goals):
        c = self.centroid(goals)
        s = [self.dist2(s, c) for s in state.state]
        return sum(s)/len(s)

    def f_state_centroid(self, state, goals):
        c = self.centroid(state.state)
        s = [self.dist2(s, c) for s in goals]
        return self.avg(s)
    
    def f_centroid(self, state, goals):
        cs = self.centroid(state.state)
        cg = self.centroid(goals)
        return self.dist2(cs, cg)

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
        s = ([self.avg([self.dist2(s, g) for g in goals]) for s in state.state])

        state.F = state.depth + self.f_state_centroid(state, goals)*state.depth/state.len

        # -1 * state.depth gives cool results
        # state.len also
        return state
    
    def preProcessDists(self):
        """
        For each field compute distance to the nearest goal
        """
        dists = {(n, m): 100000 for n in range(1, len(self.board) - 1) 
                 for m in range(1, len(self.board[0]) - 1)}

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
        print(self.dists)

        hq = []
        heapq.heappush(hq, self.computeF(state, goals))

        visited = set([state])
        stLen = state.len

        while hq and self.isSolved(state) is False:
            state = heapq.heappop(hq)
            for move in self.MOVES:
                neigh = self.getNeighbour(state, move)
                if neigh not in visited:
                    heapq.heappush(hq, self.computeF(neigh, goals))
                    visited = visited | set([neigh])
                    stLen = neigh.len

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
    print(coma)
    ans = coma.astar()
    print("{}".format(ans))

    fout = open(foutput,"w")
    print(ans, file=fout)