import random
import sys
import reversi_gfx as gfx

M = 8
MAX = 1
MIN = 0
INF = 100000000
THRESH = 58  # A ply threshold, uppon which CR_RES is considered

DEPTH = 2
CX_RES = 1.2  # * self.result()
CX_FIE = 0    # * self.field_bonus(move, player)
CX_COR = 800  # * self.corners_bonus(player)
CX_PEN = 380  # * self.close_corner_penalty(player)


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
        self.ply = 0
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
        self.move_list.append(move)
        self.ply += 1

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

    def lookup_get(self, board, x, y):
        if 0 <= x < M and 0 <= y < M:
            return board[y][x]
        return None

    def lookup_move(self, board, move, player):
        new_board = [x[:] for x in board]

        if move is None:
            return new_board

        x, y = move
        x0, y0 = move
        new_board[y][x] = player

        for dx, dy in self.dirs:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.lookup_get(board, x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.lookup_get(board, x, y) == player:
                for (nx, ny) in to_beat:
                    new_board[ny][nx] = player
        return new_board

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

    def result(self, board):
        """
        result = #black - #white
        """
        max_coins = min_coins = 0.0
        for y in range(M):
            for x in range(M):
                b = board[y][x]
                if b == MIN:
                    min_coins += 1.0
                elif b == MAX:
                    max_coins += 1.0
        if self.ply > THRESH:
            return 100.0 * (max_coins - min_coins) / (max_coins + min_coins)
        else:
            return 10e-11

    def field_bonus(self, board, player):
        """
        https://web.stanford.edu/class/cs221/2017/restricted/p-final/man4/final.pdf
        """
        BONUS = [[16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16],
                 [-4.12, -1.81, -0.08, -0.27, -0.27, -0.08, -1.81, -4.12],
                 [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                 [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                 [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                 [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                 [-4.12, -1.81, -0.08, -0.27, -0.27, -0.08, -1.81, -4.12],
                 [16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16]]
        bonus = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == player:
                    bonus += BONUS[i][j]
                elif board[i][j] == MIN:
                    bonus -= BONUS[i][j]
        return bonus

    def corners_bonus(self, board, player):
        CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
        max_corners = min_corners = 0.0
        for i, j in CORNERS:
            if board[i][j] == MAX:
                max_corners += 1.0

            if board[i][j] == MIN:
                min_corners += 1.0
        bonus = 0
        if max_corners + min_corners != 0:
            bonus = 100*(max_corners - min_corners)/(max_corners + min_corners)
        return bonus

    def close_corner_penalty(self, board, player):
        CLOSE = {(0, 0): [(0, 1), (1, 0), (1, 1)],  # top left
                 (0, 7): [(0, 6), (1, 7), (1, 6)],  # top right
                 (7, 0): [(6, 0), (7, 1), (6, 1)],  # bot left
                 (7, 7): [(6, 7), (7, 6), (6, 6)]}  # bot right
        min_close = max_close = 0
        for i, j in CLOSE:
            if board[i][j] is None:
                for x, y in CLOSE[(i, j)]:
                    if board[x][y] == MAX:
                        max_close += 1.0
                    if board[x][y] == MIN:
                        min_close += 1.0
        penalty = 0
        if (max_close + min_close != 0):
            penalty = 100.0 * (max_close - min_close)/(max_close + min_close)
        return -penalty

    def bonus(self, board, player):
        bonus = CX_RES * self.result(board) + \
                CX_FIE * self.field_bonus(board, player) +\
                CX_COR * self.corners_bonus(board, player) +\
                CX_PEN * self.close_corner_penalty(board, player)
        return bonus

    def awesome_move(self, player):
        # Depth-1 recursion  hardcoded in for loops
        level1 = []
        moves1 = self.moves(player)

        # Player moves - MAX
        for move in [m for m in moves1]:
            board_1 = self.lookup_move(self.board, move, player)
            bon = self.bonus(board_1, player)
            level1.append(bon)

        res = moves1[level1.index(max(level1))]
        return res

    def awesomer_move(self, player):
        """
        Recursive minmax decision algorithm
        """
        moves = self.moves(player)
        awesome = None
        maxval = -INF
        for m in moves:
            v = self.bonus(self.lookup_move(self.board, m, player), player) \
                + self.minmax(self.board, 1-player, DEPTH)
            if v > maxval:
                maxval = v
                awesome = m
        return awesome

    def minmax(self, board, player, depth):
        if depth == 0:
            return 0

        if self.terminal():
            return self.bonus(board, player)

        values = [self.bonus(self.lookup_move(board, move, player), player) +
                  self.minmax(self.lookup_move(board, move, player), 1 - player, depth-1)
                  for move in self.moves(player)]

        if player == MAX:
            return max(values)
        else:
            return min(values)

    def awesomest_move(self, player):
        """
        alpha-beta pruning
        """
        awesomest = None
        minval, maxval = INF, -INF
        for m in self.moves(player):
            board = self.lookup_move(self.board, m, player)
            bonus = self.bonus(board, player)
            # Pruning will be conciderd at least on grandson's level
            if player == MAX:
                bonus += self.min_value(board, 1-player, DEPTH-1, -INF, INF)
                if bonus > maxval:
                    maxval = bonus
                    awesomest = m
            else:
                bonus += self.max_value(board, 1-player, DEPTH-1, -INF, INF)
                if bonus < minval:
                    minval = bonus
                    awesomest = m
        return awesomest

    def max_value(self, board, player, depth, alpha, beta):
        if self.terminal() or depth == 0:
            return self.bonus(board, player)
        value = -INF

        for move in self.moves(player):
            b = self.lookup_move(board, move, player)
            value = max(value, self.min_value(b, 1-player, depth-1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, board, player, depth, alpha, beta):
        if self.terminal() or depth == 0:
            return self.bonus(board, player)
        value = INF

        for move in self.moves(player):
            b = self.lookup_move(board, move, player)
            value = min(value, self.max_value(b, 1-player, depth-1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value


def play(show=False):
    player = 0
    B = Board()

    while True:
        if show:
            B.draw()
            B.show()
        if player == MAX:
            m = B.awesomest_move(player)  # !!!!
            # m = B.alpha_beta(player)
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
        print('Result', B.result(B.board))
        input('Game over!')
        sys.exit(0)
    return B.result(B.board)


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
