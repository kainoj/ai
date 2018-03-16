import numpy as np


class Nonogram():

    def __init__(self, rows, cols, row, col):
        self.rows = rows        # Number of rows
        self.cols = cols        # Number of cols
        self.row = row          # Rows description
        self.col = col          # Cols description
        self.nono = np.zeros((rows, cols))      # A board matrix
        self.MAXITER = 5000      # Max. number of iterations of solve()

    def __str__(self):
        return '\n'.join([''.join(["#" if v == 1 else "." for v in row])
                         for row in self.nono])

    def __repr__(self):
        return self.__str__()

    def info(self):
        print("{} x {}".format(self.rows, self.cols))
        print("Rows desc: {}".format(self.row))
        print("Cols desc: {}".format(self.col))

    def transpose(self):
        self.nono = np.transpose(self.nono)
        self.rows, self.cols = self.cols, self.rows
        self.row, self.col = self.col, self.row

    def presolve_row(self):
        """
        >>> nono = Nonogram(2, 5, [[3], [0]], [[], [], [], [2], []])
        >>> nono.presolve()
        >>> nono.__str__() == '..##.\\n...#.'
        True
        """
        for r in range(self.rows):
            if len(self.row[r]) == 1 and self.row[r][0] > self.cols / 2:
                for i in range(self.cols - self.row[r][0], self.row[r][0]):
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
    rows = lines[0][0]
    cols = lines[0][1]

    nono = Nonogram(rows, cols, row=lines[1:rows+1], col=lines[rows+1:])

    nono.info()
    nono.presolve()
    print(nono)

    # nono = Nonogram(2, 5, [[3], [0]], [[], [], [], [2], []])
    # nono.info()
    # print(nono)
    # nono.presolve()
    # nono.info()
    # print(nono)
    # nono.presolve()
