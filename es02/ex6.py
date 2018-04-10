from ex5 import Commando
from ex4 import readBoard
import sys


if __name__ == '__main__':

    finput = 'zad_input.txt'
    foutput = 'zad_output.txt'

    if len(sys.argv) == 2:
        finput = sys.argv[1]

    board = readBoard(finput)

    coma = Commando(board, non_admissible=True)
    ans = coma.astar()

    fout = open(foutput, "w")
    print(ans, file=fout)