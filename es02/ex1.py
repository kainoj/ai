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
        
        # self.nono = np.zeros((rows, cols), dtype=np.int8)    # A board matrix
        self.nono = [[0 for c in range(cols)] for r in range(rows)]

        # Cache row / cols arragement cache[0] - rows, cache[1] - cols
        self.cache = [[], []] 

        self.MAXITER = (rows + cols) * 500  # Max. number of iterations of solve()

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
    def opt_dist_tuple(self, row, what, nmbr):
        """
        Given a row and its description computes opt dist...
        what = 0 iff given nono's row
             = 1 iff given nono's col
        """
        if what == 0:
            row_desc = self.row_desc[nmbr]
            row_len = self.c
        elif what == 1:
            row_desc = self.col_desc[nmbr]
            row_len = self.r


        a = row
        opt_d = 1000000
        for b in self.cache[what][nmbr]:
            n = len(a) + 1
            m = len(b) + 1
            d = [[0 for col in range(m)] for row in range(n)]
            for i in range(0, n): d[i][0] = i
            for j in range(0, m): d[0][j] = j

            for i in range(1, n):
                for j in range(1, m):
                    d[i][j] = min( 
                        d[i-1][j] + 1,
                        d[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1),
                        d[i][j-1] + 1
                    )
            if d[n-1][m-1] < opt_d:
                opt_d = d[n-1][m-1]

        return opt_d

    def opt_dist(self, row, what, nmbr):
        return self.opt_dist_tuple(tuple(row), what, nmbr)


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
        Return index of a row that is the most closest to optimal row (d > 0)
        If no such row exists, returns -1
        """
        idx = -1
        sco = 0

        for i, row in enumerate(self.nono):
            d = self.opt_dist(row, 0, i)
            if d > sco:
                if sco > 2*self.c/3:
                    return idx

                sco = d
                idx = i

        return idx
    
    def scoreColToggled(self, colno, pixno):
        """
        For a given column returns opt_dist(col, d) - opt_dist(col' - d),
        where col' is a col with toggled i-th bit

        rateColOnToggle > 0  iff pixel toggle improved col score
                        = 0  iff              hasn't changed anything
                        < 0  iff              made the score worse
        """
        col = self.nono[:, colno]
        d = self.opt_dist(col, 1, colno)
        
        col[pixno] = 1 if col[pixno] == 0 else 0
        d2 = self.opt_dist(col, 1, colno)
        col[pixno] = 1 if col[pixno] == 0 else 0

        return d - d2
    
    def validateCols(self):
        # print("O KURDE")
        # print(self)
        for c in range(self.c):
            if self.opt_dist(self.nono[:, c].tolist(), 1, c) > 0:
                return False
        return True
    
    def randDecision(self):
        return random.randrange(0, 99) < 20

    def chooseCol(self, rowno):
        colScores = 0
        colno = -1

        for c in range(self.c):
            score = self.scoreColToggled(c, rowno)
            if score > colScores:
                colno = c
                colScores = score
        return colno


    def solve(self):
        for iterno in range(self.MAXITER):

            rowno = self.badRows()

            if rowno == -1 and self.validateCols():
                print("iteracji: {}".format(iterno))
                return
            
            # With probability x/5 choose a random row
            if rowno == - 1 or self.randDecision():
                rowno = random.randrange(0, self.r)


            colno = self.chooseCol(rowno)

            # Choose random column to toggle a pixel
            if colno == -1 or self.randDecision():
                colno = random.randrange(0, self.c)
    
            # toggle
            self.nono[rowno][colno] = (1 if self.nono[rowno][colno] == 0 else 0)
            
            if self.randDecision():
                self.presolve()
            
        # print("BANNG")
        # print(self)
        self.nono = np.zeros((self.r, self.c), dtype=np.int8)
        self.presolve()
        self.solve()
        

if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    finput = 'data/ex01_heart.tst'
   

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
    print("done")

    # for r in nono.cache:
    #     print(r)
    #     print("----")
    nono.presolve() 
    print(nono)
    nono.solve()
    print(nono)


    # fout = open(foutput, "w")
    # print(nono, file=fout)
