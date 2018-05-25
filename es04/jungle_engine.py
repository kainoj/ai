import random


BOARD = [list(row) for row in
         ['..#*#..',  # meadow: .
          '...#...',  # trap:   #
          '.......',  # pond:   ~
          '.~~.~~.',  # den:    *
          '.~~.~~.',
          '.~~.~~.',
          '.......',
          '...#...',
          '..#*#..']]

INIT_BOARD = [list(row) for row in
              ['L.....T',  # P0  (capital)
               '.D...C.',
               'R.J.W.E',
               '.......',
               '.......',
               '.......',
               'e.w.j.r',
               '.c...d.',
               't.....l']]

N = 9   # Board height
M = 7   # Board width

P0 = 0  # Player 0
P1 = 1  # Player 1
BEATS_TRESH = 50


RAT = 'R'
TIGER = 'T'
LION = 'L'
ELEPHANT = 'E'
FIGURES = {RAT: 0, 'C': 1, 'D': 2, 'W': 3, 'J': 4,
           TIGER: 5, LION: 6, ELEPHANT: 7}

DIRS = {(0, -1), (0, 1), (1, 0), (-1, 0)}


TRAP = '#'
FREE = '.'
DEN = '*'
POND = '~'

################
#  GAME LOGIC  #
################


def on_board(board, field):
    x, y = field
    return 0 <= x and x < 9 and 0 <= y and y < 7


def is_free(board, field):
    """
    Is a field in a current state free?
    """
    x, y = field
    return board[x][y] == FREE


def is_meadow(field):
    x, y = field
    return BOARD[x][y] == FREE


def is_free_meadow(board, field):
    return is_free(board, field) and is_meadow(field)


def is_trap(field):
    x, y = field
    return BOARD[x][y] == TRAP


def is_free_trap(board, field):
    """
    Check if a `field` is a free field which is a trap
    """
    return is_free(board, field) and is_trap(field)


def is_pond(field):
    x, y = field
    return BOARD[x][y] == POND


def is_free_pond(board, field):
    return is_free(board, field) and is_pond(field)


def is_rat(fig):
    return fig.upper() == RAT


def is_elephant(fig):
    return fig.upper() == ELEPHANT


def is_predator(fig):
    """
    A predator = lion or tiger
    """
    return fig.upper() == LION or fig.upper() == TIGER


def is_opponent(fig1, fig2):
    return fig1.islower() and fig2.isupper() \
           or fig1.isupper() and fig2.islower()


def is_opp_den(board, field, player):
    """
    Check wheather the field is opponent's den (→ win)
    """
    x, y = field
    p0wins = (player.id == P0 and x > N / 2)
    p1wins = (player.id == P1 and x == 0)
    return BOARD[x][y] == DEN and (p0wins or p1wins)


def get_fig(board, field):
    x, y = field
    return board[x][y]

####################
#  GAME MECHANICS  #
####################


def get_neighbour(board, figure, field, direction, player):
    """
    Return all possible would-be fields, into which the figure can move
    """
    x, y = field
    a, b = direction
    neighbour = (x+a, y+b)
    if on_board(board, neighbour) is False:
        return None

    if is_meadow(neighbour) or \
       is_trap(neighbour) or \
       is_opp_den(board, neighbour, player):
        return neighbour

    if is_rat(figure) and is_pond(neighbour):
        return neighbour

    if is_predator(figure) and is_pond(neighbour):
        return predator_jumps(board, field, a, b)

    return None


def predator_jumps(board, field, dir_x, dir_y):
    """
    Returns a field which is on the opposite site of the pond
            (on condition there's no opponent's rat on predator's way)
    """
    x, y = field
    predator = board[x][y]
    while True:
        x, y = x + dir_x, y + dir_y
        if on_board(board, (x, y)) is False:
            return None

        neigh = board[x][y]
        if is_rat(neigh) and is_opponent(predator, neigh):
            return None
        if is_meadow((x, y)):
            return (x, y)


def get_moves(board, player):
    """
    Return list of (f, (x, y)) → figure f can move to (x, y)
    f is a tuple in form of (animal, (pos_x, pos_y))
    """
    moves = []
    for figure in player.figures.items():
        fig, field = figure
        for direction in DIRS:
            neigh_pos = get_neighbour(board, fig, field, direction, player)
            if neigh_pos is not None:
                if is_free(board, neigh_pos):
                    moves.append((figure, neigh_pos))
                elif can_beat(fig, field, get_fig(board, neigh_pos), neigh_pos):
                    moves.append((figure, neigh_pos))
    return moves


def can_beat(fig, fig_pos, neigh, neigh_pos):
    """
    Can `figure` beat `neigh`? (is figure equal or stronger than neigh)?
    """
    if is_opponent(fig, neigh) is False:
        return False

    # If neigh is in a trap
    if is_trap(neigh_pos):
        return True

    # Rat which is in the pond cannot beat neigh on a meadow
    if is_rat(fig) and is_pond(fig_pos) and is_meadow(neigh_pos):
        return False

    if is_rat(fig) and is_elephant(neigh):
        return True
    return FIGURES[fig.upper()] >= FIGURES[neigh.upper()]


def terminal(state):
    # One of the player lacks figures
    if state.player_1.no_figures():
        return P0
    if state.player_0.no_figures():
        return P1

    # A trap is taken
    if state.board[0][3] != FREE:
        return P1
    if state.board[8][3] != FREE:
        return P0

    # Game lasts too long
    if state.no_beats > BEATS_TRESH:
        p0strong = state.player_0.get_strongest()
        p1strong = state.player_1.get_strongest()
        if p0strong > p1strong:
            return P0
        if p1strong > p0strong:
            return P1

        p0trap_dist = state.player_0.dists_to_trap(state.board)
        p1trap_dist = state.player_1.dists_to_trap(state.board)

        for i in range(min(len(p0trap_dist), len(p1trap_dist))):
            if p0trap_dist[i] < p1trap_dist[i]:
                return P0
            if p0trap_dist[i] > p1trap_dist[i]:
                return P1
        return P0  # because P0 always moves 1st
    return None


def random_move(board, player):
    moves = get_moves(board, player)
    if len(moves) == 0:
        return None
    return random.choice(moves)


def do_move(state, move, player_id):
    # Get a player based on it's id
    p = state.player_0 if player_id == P0 else state.player_1
    opp = state.player_0 if player_id == P1 else state.player_1

    # Unpack a move
    (fig, (src_x, src_y)), (dst_x, dst_y) = move

    state.no_beats += 1

    if is_free(state.board, (dst_x, dst_y)) is False:
        opp.figure_loss(get_fig(state.board, (dst_x, dst_y)))
        state.no_beats = 0

    state.board[src_x][src_y] = BOARD[src_x][src_y]
    state.board[dst_x][dst_y] = fig
    p.move(fig, (dst_x, dst_y))
    return state


def random_game(base_state, player_id):
    """
    Play a random game from a given state and afterall restore init state
    """
    ply = 0
    state = base_state.get_copy()

    while True:
        ply += 1
        if player_id == P0:
            move = random_move(state.board, state.player_0)
        else:
            move = random_move(state.board, state.player_1)

        if move is None:
            return 1-player_id, ply

        ((fig, src), dst) = move

        do_move(state, move, player_id)

        term = terminal(state)
        if term is not None:
            return term, ply

        player_id = 1 - player_id


def h(state, move, player):
    ((fig, src), dst) = move
    sx, sy = src
    dx, dy = dst
    bonus = random.randint(0, 10)

    # Jump into the den if possible
    if is_opp_den(state.board, dst, player):
        bonus += 1000000

    # Preffer moves which eliminates opp's figures
    if is_free(state.board, (dx, dy)) is False:
        bonus += 100

    # P0 moved down towards P1's den
    if dx - sx > 0 and player.id == P0:
        bonus += 400000000
    # P1 moved up towards P0's den
    elif dx - sx < 0 and player.id == P1:
        bonus += 400000000

    return bonus


def awesome_move(state, player):
    moves = get_moves(state.board, player)
    if moves is None:
        return None
    return max(moves, key=lambda m: h(state, m, player))


DEBUG = False


def dprint(string):
    if DEBUG is True:
        print(string)


def dinput():
    if DEBUG:
        input()
