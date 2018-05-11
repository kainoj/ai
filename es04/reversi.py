import random
import sys
import reversi_gfx as gfx

M = 8
MAX = 1
MIN = 0
INF = 100000000
PLY = 0

DEPTH = 1
CX_RES = 10  # * self.result()
CX_FIE = 0  # * self.field_bonus(move, player)
CX_COR = 8   # * self.corners_bonus(player)
CX_PEN = 6  # * self.close_corner_penalty(player)


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
        if PLY > 50:
            return 100.0 * (max_coins - min_coins) / (max_coins + min_coins)
        else:
            return 0

    def field_bonus(self, board, field, player):
        """
        https://web.stanford.edu/class/cs221/2017/restricted/p-final/man4/final.pdf
        """
        if field is None:
            return 0
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
                if board[i][j] == MAX:
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
        close_diff = 0
        for i, j in CLOSE:
            if board[i][j] is None:
                for x, y in CLOSE[(i, j)]:
                    if board[x][y] == MAX:
                        close_diff += 1.0
                    if board[x][y] == MIN:
                        close_diff -= 1.0
        penalty = -12.5 * (close_diff)
        return penalty

    def bonus(self, board, move, player):
        bonus = CX_RES * self.result(board) + \
                CX_FIE * self.field_bonus(board, move, player) +\
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
            bon = self.bonus(board_1, move, player)
            level1.append(bon)

        res = moves1[level1.index(max(level1))]
        return res


def play(show=False):
    global PLY
    PLY = 0
    player = 0
    B = Board()

    while True:
        PLY += 1
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
