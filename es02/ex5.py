import ex4
import heapq
import queue
import sys
from random import sample
from math import sqrt


class Commando(ex4.Commando):

    def computeF(self, state, goals):
        """
        Compute f = g + h  function, where:
            g - distance from initial state ( = self.depth )
            h - admissible heuristic function
        Returns the state with modiefied F.

        Note: F = g = self.depth is just an ordinary BFS
        """
        if self.non_admissible is True:
            # Ex 6.
            state.F = state.depth +  sum([self.dists[s] for s in state.state])
        else:
            # Ex 5.
            state.F = state.depth + max([self.dists[s] for s in state.state])
        return state

    def preProcessDists(self):
        """
        For each field compute distance to the nearest goal
        """
        dists = {(n, m): 100000 for n in range(1, len(self.board) - 1)
                 for m in range(1, len(self.board[0]) - 1)
                 if self.board[n][m] != ex4.WALL}

        for g in self.goals:
            """ Run BFS for each goal """

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

        visited = {state: state.F}

        while hq and self.isSolved(state) is False:
            state = heapq.heappop(hq)
            for move in self.MOVES:
                neigh = self.getNeighbour(state, move)
                neigh = self.computeF(neigh, goals)

                if neigh not in visited:
                    heapq.heappush(hq, neigh)
                    visited[neigh] = neigh.F
                else:
                    if neigh.F < visited[neigh]:
                        heapq.heappush(hq, neigh)

        return self.traceback(state)


if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    if len(sys.argv) == 2:
        finput = sys.argv[1]

    board = ex4.readBoard(finput)

    coma = Commando(board)
    ans = coma.astar()

    print(ans)

    fout = open(foutput, "w")
    print(ans, file=fout)
