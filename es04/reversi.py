import random
import sys
# from collections import defaultdict as dd
import reversi_gfx as gfx

M = 8
MAX = 1
MIN = 0

DEPTH = 1
CX_RES = 10  # * self.result()
CX_FIE = 10  # * self.field_bonus(move, player)
CX_COR = 801.724   # * self.corners_bonus(player)
CX_PEN = 0.0   # * self.close_corner_penalty(player)


def initial_board():
    B = [[None] * M for i in range(M)]
    B[3][3] = MAX
    B[4][4] = MAX
    B[3][4] = MIN
    B[4][3] = MIN
    return B


class Board:    
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] is None:
                    self.fields.add((j, i))

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b is None:
                    res.append('.')
                elif b == MAX:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print()

    def show(self):
        for i in range(M):
            for j in range(M):
                gfx.kwadrat(j, i, 'green')

        for i in range(M):
            for j in range(M):
                if self.board[i][j] == MAX:
                    gfx.kolko(j, i, 'black')
                if self.board[i][j] == MIN:
                    gfx.kolko(j, i, 'white')

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in Board.dirs):
                res.append((x, y))
        if not res:
            return [None]
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.dirs:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player

    def undo_move(self):
        if self.history:
            self.board = self.history.pop()
        if self.move_list:
            x = self.move_list.pop()
            if x:
                self.fields.add(x)

    def result(self):
        """
        result = #black - #white
        """
        max_coins = min_coins = 0.0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == MIN:
                    min_coins += 1.0
                elif b == MAX:
                    max_coins += 1.0
        return 100.0 * (max_coins - min_coins) / (max_coins + min_coins)

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] is None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]

    def field_bonus(self, field, player):
        """
        https://web.stanford.edu/class/cs221/2017/restricted/p-final/man4/final.pdf
        """
        if field is None:
            return 0
        BONUS = [[16.16, -3.03,  0.99,  0.43],
                 [-4.12, -1.81, -0.08, -0.27],
                 [01.33, -0.04,  0.51,  0.07],
                 [00.63, -0.18, -0.04, -0.01]]
        x, y = field
        if x > 3:
            x = 7 - x
        if y > 3:
            y = 7 - y
        bonus = BONUS[x][y] / 16.16
        if player == MAX:
            return bonus
        return -bonus

    def corners_bonus(self, player):
        CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
        max_corners = min_corners = 0.0
        for i, j in CORNERS:
            if self.board[i][j] == MAX:
                max_corners += 1.0

            if self.board[i][j] == MIN:
                min_corners += 1.0
        bonus = 0.0
        if(max_corners + min_corners != 0):
            bonus = 100.0 * (max_corners - min_corners) / (max_corners + min_corners)

        if player == MAX:
            return bonus
        return -bonus

    def close_corner_penalty(self, player):
        CLOSE = [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)]
        max_close = min_close = 0.0
        for i, j in CLOSE:
            if self.board[i][j] == MAX:
                max_close += 1.0
            if self.board[i][j] == MIN:
                min_close += 1.0

        penalty = 0.0
        if (min_close + max_close != 0):
            penalty = 100.0 * (max_close - min_close) / (min_close + max_close)

        if player == MAX:
            return -penalty
        return penalty

    def bonus(self, move, player):
        bonus = CX_RES * self.result() + \
                CX_FIE * self.field_bonus(move, player) +\
                CX_COR * self.corners_bonus(player) +\
                CX_PEN * self.close_corner_penalty(player)
        return bonus

    def awesome_move(self, player):
        player2 = 1 - player

        # Depth-3 recursion  hardcoded in for loops

        level1 = []
        moves1 = self.moves(player)

        # Player moves - MAX
        for move in [m for m in moves1]:
            self.do_move(move, player)
            level2 = []

            # Player2 moves - MIN
            for move2 in [m for m in self.moves(player2)]:
                self.do_move(move2, player2)
                level3 = []

                # Player moves - MAX
                for move3 in [m for m in self.moves(player)]:
                    self.do_move(move3, player)
                    bon = self.bonus(move3, player) \
                        + self.bonus(move2, player2) \
                        + self.bonus(move, player)
                    level3.append(bon)
                    self.undo_move()
                level2.append(max(level3))
                self.undo_move()
            level1.append(min(level2))
            self.undo_move()

        res = moves1[level1.index(max(level1))]
        return res

    def awesomer_move(self, player):
        moves = self.moves(player)
        awesome = None
        maxval = -10000
        for m in moves:
            self.do_move(m, player)
            v = self.bonus(m, player) + self.minmax(1-player, DEPTH)
            self.undo_move()
            if v > maxval:
                maxval = v
                awesome = m
        return awesome

    def minmax(self, player, depth):
        if depth == 0 or self.terminal():
            return self.result()

        values = [self.bonus(move, player) +
                  self.minmax(1 - player, depth-1)
                  for move in self.moves(player)]

        if player == MAX:
            return max(values)
        else:
            return min(values)


def play(show=False):
    player = 0
    B = Board()

    while True:
        if show:
            B.draw()
            B.show()
        if player == MAX:
            m = B.awesome_move(player)  # !!!!
        else:
            m = B.random_move(player)
        B.do_move(m, player)
        player = 1 - player
        if show:
            input()
        if B.terminal():
            break

    if show:
        B.draw()
        B.show()
        print('Result', B.result())
        input('Game over!')
        sys.exit(0)
    return B.result()


if __name__ == "__main__":

    rounds = 1

    if len(sys.argv) == 2:
        rounds = int(sys.argv[1])

    loss = 0

    print("====== INFO =======")
    print("> depth  = {}".format(DEPTH))
    print("> CX_RES = {}".format(CX_RES))
    print("> CX_FIE = {}".format(CX_FIE))
    print("> CX_COR = {}".format(CX_COR))
    print("> CX_PEN = {}".format(CX_PEN))
    print("===================\n")

    for i in range(1, rounds+1):
        if play(rounds == 1) < 0:
            loss += 1
        if i % 100 == 0:
            print("Lost {} / {} games ({}%)".format(loss, i, 100.0 * loss/i))
