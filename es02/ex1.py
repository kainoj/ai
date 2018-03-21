import numpy as np

import itertools


class Nonogram():

    def __init__(self, rows, cols, row_desc, desc_col):
        self.r = rows                # Number of rows
        self.c = cols                # Number of cols
        self.row_desc = row_desc     # Rows description
        self.desc_col = desc_col     # Cols description
        self.nono = np.zeros((rows, cols))      # A board matrix

        self.row = [[] for _ in range(rows)]
        self.col = [[] for _ in range(cols)]

        self.MAXITER = 5000      # Max. number of iterations of solve()

    def __str__(self):
        return '\n'.join([''.join(["#" if v == 1 else "." for v in row])
                         for row in self.nono])

    def __repr__(self):
        return self.__str__()

    def genPossibleRows(self, row_desc, row_len):
        
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

    def info(self):
        print("{} x {}".format(self.r, self.c))
        print("Rows desc: {}".format(self.row_desc))
        print("Cols desc: {}".format(self.desc_col))

    def transpose(self):
        self.nono = np.transpose(self.nono)
        self.r, self.c = self.c, self.r
        self.row_desc, self.desc_col = self.desc_col, self.row_desc
        self.row, self.col = self.col, self.row

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


if __name__ == '__main__':

    finput = 'data/zad1_input.tst'
    foutput = 'zad1_output.txt'

    # finput = 'data/ex1.test'

    fout = open(foutput, "w")

    lines = []
    with open(finput) as f:
        for line in f:
            lines.append(list(map(int, line.strip('\n').split())))
    r = lines[0][0]
    c = lines[0][1]

    nono = Nonogram(r, c, row_desc=lines[1:r+1], desc_col=lines[r+1:])

    # nono.info()
    # nono.presolve()
    # print(nono)

    # nono = Nonogram(2, 5, [[3], [0]], [[], [], [], [2], []])
    # nono.info()
    # print(nono)
    # nono.presolve()
    # nono.info()
    # print(nono)
    # nono.presolve()

    x = nono.genPossibleRows([1, 1, 2], 7)
    print(x)

    # x = nono.genPossibleRowsPerm([1], 5)
    # print(x)

