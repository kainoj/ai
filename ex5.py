import random

import numpy as np

from ex4 import opt_dist


class nonogram() :

    def __init__(self, rows, cols, row, col):
        self.rows = rows        # Number of rows
        self.cols = cols        # Number of cols
        self.row = row          # Rows description
        self.col = col          # Cols description
        self.nono = np.zeros((rows, cols))      # A board matrix
        self.MAXITER = 5000      # Max. number of iterations of solve()

        self.rowToggled = [0] * rows    # Number of toggled pixel in a row (col)
        self.colToggled = [0] * cols    # game is over iff rowToggled = row

    
    def print(self):
        for row in self.nono:
            for v in row:
                print("{}".format("#" if v == 1 else "."), end = " ")
            print()

    def opt_dist(self, row, d):
        return opt_dist(row.tolist(), d)


    def badRows(self):
        """
        Return [(i, dist)] - in row `i` we need to 
        toggle `dist` bits to gain a desired row
        """
        badrows = []
        for i, row in enumerate(self.nono):
            dist = self.opt_dist(row, self.row[i])
            if dist > 0:
                badrows.append(i)
        return badrows


    def scoreColToggled(self, colno, pixno):
        """
        For a given column returns opt_dist(col, d) - opt_dist(col' - d),
        where col' is a col with toggled i-th bit

        rateColOnToggle > 0  iff pixel toggle improved col score
                        = 0  iff              hasn't changed anything
                        < 0  iff              made the score worse
        """
        col = np.copy(self.nono[:, colno])
        d = self.opt_dist(col, self.col[colno])

        col[pixno] = 1 if col[pixno] == 0 else 0
        d2 = self.opt_dist(col, self.col[colno])

        return d - d2

    def validateCols(self):
        for c in range(self.cols):
            if opt_dist(self.nono[:, c].tolist(), self.col[c]) > 0:
                return False
        return True

    def randDecision(self):
        return random.randrange(0, 99) < 20

    def solve(self):

        for _ in range(self.MAXITER):

            badRows = self.badRows()
            
            if not badRows:
                if self.validateCols():
                    return
                else:
                    rowno = random.randrange(0, self.rows)
            else:
                rowno = random.choice(badRows)
                    
            # With probability 1/5 choose a random row
            if self.randDecision():
                rowno = random.randrange(0, self.rows)
            

            colScores = [c for c in range(self.cols) 
                if self.scoreColToggled(c, rowno) > 0 or self.randDecision()]


            # choose random column to toggle a pixel
            if not colScores:
                colno = random.randrange(0, self.cols-1)
            else:
                colno = random.choice(colScores)

            # toggle
            self.nono[rowno][colno] = (1 if self.nono[rowno][colno] == 0 else 0)
        
        self.solve()
            



if __name__ == '__main__':
    
    finput = 'data/ex5e.test'
    # foutput = 'zad4_output.txt'
    lines = []
    with open(finput) as f:
        for line in f:
            lines.append(line)
    
    rows, cols = map(int, lines[0].strip().split(" "))

    row = [int(r) for r in lines[1: rows + 1]]
    col = [int(c) for c in lines[cols + 1:]]


    nono = nonogram(rows, cols, row, col)
    nono.solve()
    nono.print()
