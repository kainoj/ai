from reversi import Board
import sys

class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = None
        self.game = Board(0)
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]
