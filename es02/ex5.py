import ex4
import heapq
import sys
from random import sample

class Commando(ex4.Commando):

    def astar(self):
        state = self.initState

        hq = []
        heapq.heappush(hq, (-state.depth, state) )      # TODO !!!!!!!!

        visited = set([state])
        stLen = state.len

        while hq and self.isSolved(state) is False:
            _, state = heapq.heappop(hq)
            # Let the hQ with pending states be descending in lengths
            if state.len <= stLen:
                for move in sample(self.MOVES, 4):
                    neigh = self.getNeighbour(state, move)
                    if neigh not in visited:
                        heapq.heappush(hq, (-neigh.depth, neigh)) # TODO !!!!!
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
    print(">{}<".format(ans))

    fout = open(foutput,"w")
    print(ans, file=fout)