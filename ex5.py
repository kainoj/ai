import numpy as np
import random

from ex4 import opt_dist

class nonogram() :

    def __init__(self, rows, cols, row, col):
        self.rows = rows        # Number of rows
        self.cols = cols        # Number of cols
        self.row = row          # Rows description
        self.col = col          # Cols description
        self.nono = np.zeros((rows, cols))      # A board matrix
        self.MAXITER = rows * cols *100       # Max. number of iteration

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
        # return [(i, ??) for (i, row) in enumerate(self.nono) if self.opt_dist(row, self.row[i]) > 0 ]
    
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


    def solve(self):
        # TODO remove
        self.MAXITER = 100
        for _ in range(self.MAXITER):
            self.print()
            input()
            if not self.badRows():
                print("oł jea nie ma złych")
                return
            # print("bad rows: {}-th".format(self.badRows()))
            
            rowno = random.choice(self.badRows())
            
            # if random.randrange(0, 99) < 100:
            #     rowno = random.randrange(0, self.rows - 1)
            colScores = []
            for c in range(self.cols):
                score = self.scoreColToggled(c, rowno)
                # with probability 1/10 add non-optimal element
                if score > 0: #or random.randint(0, 99) < 100:
                    colScores.append((c, score))

            # print("col scores: ")
            # print(colScores)
            # colScores = sorted(colScores, key=lambda x: x[1])
            
            colno = random.randrange(0, self.cols-1)


            # choose random column to toggle a pixel
            if not colScores:
                colno = random.randrange(0, self.cols-1)
            else:
                colno, _ = random.choice(colScores)
            print("toggle  ({}, {})".format(rowno, colno))
            # toggle
            self.nono[rowno][colno] = (1 if self.nono[rowno][colno] == 0 else 1)
            # self.print()





if __name__ == '__main__':
    
    finput = 'data/ex5d.test'
    # foutput = 'zad4_output.txt'
    lines = []
    with open(finput) as f:
        for line in f:
            lines.append(line)
    
    rows, cols = map(int, lines[0].strip().split(" "))

    row = [int(r) for r in lines[1: rows + 1]]
    col = [int(c) for c in lines[cols + 1:]]

    print("row {}".format(row))
    print("col {}".format(col))

    nono = nonogram(rows, cols, row, col)

    nono.solve()
    nono.print()
    
    
    