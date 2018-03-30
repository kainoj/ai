import numpy as np

import itertools
import random

from functools import lru_cache


class Nonogram():

    def __init__(self, rows, cols, row_desc, col_desc):
        self.r = rows                # Number of rows
        self.c = cols                # Number of cols
        self.row_desc = row_desc     # Rows description
        self.col_desc = col_desc     # Cols description
        self.nono = np.zeros((rows, cols), dtype=np.int8)      # A board matrix

        # Cache row / cols arragement cache[0] - rows, cache[1] - cols
        self.cache = [[], []] 

        self.MAXITER = 20000      # Max. number of iterations of solve()

    def __str__(self):
        return '\n'.join([''.join(["#" if v == 1 else "." for v in row])
                         for row in self.nono])

    def __repr__(self):
        return self.__str__()

    # @lru_cache(maxsize=2**20)
    def genPossibleRows(self, row_desc, row_len):

        row_desc = list(row_desc)
        
        if len(row_desc) == 1:
            zeros = row_len - row_desc[0]
            return [[0]*i + [1]*row_desc[0] + [0]*(zeros-i) for i in range(zeros+1)]

        limit = row_len - row_desc[-1]
        ans = []
        for comb in itertools.combinations(range(limit + 1), len(row_desc)):
            not_overlapping = True
            for c in range(len(comb) - 1):
                if comb[c] + row_desc[c] >= comb[c+1]:
                    not_overlapping = False
                    break
            if not_overlapping:
                t = [0] * row_len
                for i, c in enumerate(comb):
                    for j in range(c, c + row_desc[i]):
                        t[j] = 1
                ans.append(t)
                            
        return ans
    
    @lru_cache(maxsize=2**20)
    def opt_dist_tuples(self, row, row_desc, row_len):
        """
        Given a row and its description computes opt dist...
        """
        a = row  #.tolist()
        mins = []
        for b in self.genPossibleRows(tuple(row_desc), row_len):
            n = len(a) + 1
            m = len(b) + 1
            d = np.zeros((n, m), dtype=np.int8)
            for i in range(0, n): d[i][0] = i
            for j in range(0, m): d[0][j] = j

            for i in range(1, n):
                for j in range(1, m):
                    d[i][j] = min( 
                        d[i-1][j] + 1,
                        d[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1),
                        d[i][j-1] + 1
                    )
            mins.append(d[n-1][m-1])
        return min(mins)

    def opt_dist(self, row, row_desc, row_len):
        return self.opt_dist_tuples(tuple(row), tuple(row_desc), row_len)


    def info(self):
        print("{} x {}".format(self.r, self.c))
        print("Rows desc: {}".format(self.row_desc))
        print("Cols desc: {}".format(self.col_desc))

    def transpose(self):
        self.nono = np.transpose(self.nono)
        self.r, self.c = self.c, self.r
        self.row_desc, self.col_desc = self.col_desc, self.row_desc
        # self.row, self.col = self.col, self.row

    def presolve_row(self):
        """
        >>> nono = Nonogram(2, 5, [[3], [0]], [[], [], [], [2], []])
        >>> nono.presolve()
        >>> nono.__str__() == '..##.\\n...#.'
        True
        """
        for r in range(self.r):
            if len(self.row_desc[r]) == 1 and self.row_desc[r][0] > self.c / 2:
                for i in range(self.c - self.row_desc[r][0], self.row_desc[r][0]):
                    self.nono[r][i] = 1

    def presolve(self):
        self.presolve_row()
        self.transpose()
        self.presolve_row()
        self.transpose()
        
    def presolveCache(self):
        """ 
        For each row (cache[0]) and col (chache[1]) description retrun cache 
        list of possible row (cols) arrangement
        """
        self.cache[0] = [self.genPossibleRows(row, self.c) 
                            for row in self.row_desc]
        
        self.cache[1] = [self.genPossibleRows(col, self.r)
                            for col in self.col_desc]
                    

    def badRows(self):
        """
        Return indicies of incorrect rows
        """
        return [i for i, row in enumerate(self.nono)
                if self.opt_dist(row, self.row_desc[i], self.c) > 0] 
    
    def scoreColToggled(self, colno, pixno):
        """
        For a given column returns opt_dist(col, d) - opt_dist(col' - d),
        where col' is a col with toggled i-th bit

        rateColOnToggle > 0  iff pixel toggle improved col score
                        = 0  iff              hasn't changed anything
                        < 0  iff              made the score worse
        """
        col = np.copy(self.nono[:, colno])
        d = self.opt_dist(col, self.col_desc[colno], self.r)

        col[pixno] = 1 if col[pixno] == 0 else 0
        d2 = self.opt_dist(col, self.col_desc[colno], self.r)

        return d - d2
    
    def validateCols(self):
        for c in range(self.c):
            if self.opt_dist(self.nono[:, c].tolist(), self.col_desc[c], self.r) > 0:
                return False
        return True
    
    def randDecision(self):
        return random.randrange(0, 99) < 20

    def solve(self):
        for iterno in range(self.MAXITER):

            badRows = self.badRows()

            if not badRows:
                if self.validateCols():
                    return
                else:
                    rowno = random.randrange(0, self.r)
            else:
                rowno = random.choice(badRows)
                
            # With probability 1/5 choose a random row
            if self.randDecision():
                rowno = random.randrange(0, self.r)

            colScores = [c for c in range(self.c)
                         if self.scoreColToggled(c, rowno) > 0
                         or self.randDecision()]

            # Choose random column to toggle a pixel
            if not colScores:
                colno = random.randrange(0, self.c-1)
            else:
                colno = random.choice(colScores)

            # toggle
            self.nono[rowno][colno] = (1 if self.nono[rowno][colno] == 0
                                       else 0)
            
        print(self)
            # input()
        self.solve()
        

if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    finput = 'data/zad1_input.tst'
   

    lines = []
    with open(finput) as f:
        for line in f:
            lines.append(list(map(int, line.strip('\n').split())))

    r = lines[0][0]
    c = lines[0][1]

    nono = Nonogram(r, c, row_desc=lines[1:r+1], col_desc=lines[r+1:])

    nono.info()

    print("prechaching...")
    nono.presolveCache()
    print("dine")

    # for r in nono.cache:
    #     print(r)
    #     print("----")
    # nono.presolve()
    # nono.solve()


    # fout = open(foutput, "w")
    # print(nono, file=fout)