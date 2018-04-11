import ex2
import heapq
import queue
import sys
from math import sqrt

class Sokoban(ex2.Sokoban):

    def dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def dist2(self, a, b):
        x = a[0] - b[0]
        y = a[1] - b[1]
        return sqrt(x**2 + y**2)

    def computeH(self, state):
        """
        Computes heuristic function and retruns modified (soko) state
        state.h = state.depth <=> BFS
        """
        d = [min([self.dist(b, g) for g in self.goals])  for b in state.boxes]
        state.h = sum(d)/len(d)
        return state

    def bestFirstSearch(self):

        box_state = self.computeH(self.state)

        # hq - a priority queue containing box' states
        hq = []
        heapq.heappush(hq, box_state)

        # States of boxes which were visited
        vis_boxes = set([box_state])

        # Best first search
        while hq and self.isSolved(box_state) is False:
            box_state = heapq.heappop(hq)

            # BFS inside
            # q - a queue containing keeper's states
            q = queue.Queue()
            q.put(box_state)
            vis_keeper = set([box_state])
            
            while q.empty() is False:
                s = q.get()
                
                for neigh in self.genStates(s):
                   
                    # If a move which doesn't move a box was made
                    if s.boxes == neigh.boxes:
                        if neigh not in vis_keeper:
                            vis_keeper = vis_keeper | set([neigh])
                            q.put(neigh)

                    # A box was moved
                    elif neigh not in vis_boxes:

                        neigh = self.computeH(neigh)
                        heapq.heappush(hq, neigh)
                        vis_boxes = vis_boxes | set([neigh])
        
        return self.traceback(box_state)


if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'
    
    if len(sys.argv) == 2:
        finput = sys.argv[1]

    board = []
    with open(finput) as f:
        board = [list(line.strip('\n')) for line in f]

    soko = Sokoban(board)
    
    ans = soko.bestFirstSearch()
    fout = open(foutput,"w")
    print(ans, file=fout)

