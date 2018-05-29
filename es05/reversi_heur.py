from reversi import ReversiState, MAX, MIN, M

def corners_bonus(board):
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
    penalty = 0
    if (max_close + min_close != 0):
        penalty = 100.0 * (max_close - min_close)/(max_close + min_close)
    return -penalty


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
    return 100.0 * (max_coins - min_coins) / (max_coins + min_coins)