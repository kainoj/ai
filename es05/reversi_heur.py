from reversi import ReversiState, MAX, MIN, M

def corners_bonus(board):
    CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
    max_corners = min_corners = 0.0
    for i, j in CORNERS:
        if board[i][j] == MAX:
            max_corners += 1.0

        if board[i][j] == MIN:
            min_corners += 1.0
    return max_corners - min_corners


def close_corner_penalty(board):
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
    return max_close - min_close


def balance(board):
    """
    balance black/white, %
    """
    max_coins = min_coins = 0.0
    for y in range(M):
        for x in range(M):
            b = board[y][x]
            if b == MIN:
                min_coins += 1.0
            elif b == MAX:
                max_coins += 1.0
    return max_coins - min_coins


def field_bonus(board, player):
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