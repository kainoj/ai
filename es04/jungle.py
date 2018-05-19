import random
import os
import copy

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

RAT = 'R'
TIGER = 'T'
LION = 'L'
ELEPHANT = 'E'
FIGURES = {RAT: 0, 'C': 1, 'D': 2, 'W': 3, 'J': 4, TIGER: 5, LION: 6, ELEPHANT: 7}

DIRS = {(0, -1), (0, 1), (1, 0), (-1, 0)}

P0 = 0  # Player 0
P1 = 1  # Player 1

N = 9   # Board height
M = 7   # Board width

TRAP = '#'
FREE = '.'
DEN = '*'
POND = '~'

BEATS_TRESH = 50

DEBUG = True


def dprint(string):
    if DEBUG is True:
        print(string)


class State():
    def __init__(self, board, p0, p1, whos_now, no_beats):
        self.player_0 = copy.deepcopy(p0)
        self.player_1 = copy.deepcopy(p1)
        self.whos_now = copy.deepcopy(whos_now)
        self.board = [b[:] for b in board]
        self.no_beats = no_beats

    def whos_next(self):
        if self.whos_now.id == P0:
            return self.player_1
        return self.player_0


class Player():

    def __init__(self, id, board):
        self.id = id
        self.figures = {elem: (i, j) for i, row in enumerate(board) 
                        for j, elem in enumerate(row)
                        if id == P0 and elem.isupper()
                        or id == P1 and elem.islower()}

    def figure_loss(self, figure):
        self.figures.pop(figure)

    def get_strongest(self):
        return max([FIGURES[f.upper()] for f in self.figures.keys()])

    def dists_to_trap(self, board):
        # Trap coords
        tx, ty = (0, 3) if self.id == P1 else (8, 3)
        return sorted([abs(tx - fx) + abs(ty - fy) for fx, fy in self.figures.values()])

    def no_figures(self):
        return self.figures == set()


class Jungle():

    def __init__(self):
        self.s = State(INIT_BOARD,
                       Player(P0, INIT_BOARD),
                       Player(P1, INIT_BOARD),
                       P0, BEATS_TRESH)

    def get_fig(self, field):
        x, y = field
        return self.s.board[x][y]

    def can_beat(self, fig, fig_pos, neigh_pos):
        """
        Can `figure` beat `neigh`? (is figure equal or stronger than neigh)?
        """
        neigh = self.get_fig(neigh_pos)
        if self.is_opponent(fig, neigh) is False:
            return False

        # If neigh is in a trap
        if self.is_trap(neigh_pos):
            return True
        
        # Rat which is in the pond cannot beat neigh on a meadow 
        if self.is_rat(fig) and self.is_pond(fig_pos) and self.is_meadow(neigh_pos):
            return False

        if self.is_rat(fig) and self.is_elephant(neigh):
            return True
        return FIGURES[fig.upper()] >= FIGURES[neigh.upper()]


    ####################################################
    #    Boolean functions determining current state   #
    ####################################################

    def on_board(self, board, field):
        x, y = field
        return 0 <= x and x < 9 and 0 <= y and y < 7

    def is_free(self, board, field):
        """
        Is a field in a current state free?
        """
        x, y = field
        return board[x][y] == FREE

    def is_meadow(self, field):
        x, y = field
        return BOARD[x][y] == FREE

    def is_free_meadow(self, board, field):
        return self.is_free(board, field) and self.is_meadow(field)

    def is_trap(self, field):
        x, y = field
        return BOARD[x][y] == TRAP

    def is_free_trap(self, board, field):
        """
        Check if a `field` is a free field which is a trap
        """
        return self.is_free(board, field) and self.is_trap(field)

    def is_pond(self, field):
        x, y = field
        return BOARD[x][y] == POND

    def is_free_pond(self, board, field):
        return self.is_free(board, field) and self.is_pond(field)

    def is_rat(self, fig):
        return fig.upper() == RAT
    
    def is_elephant(self, fig):
        return fig.upper() == ELEPHANT

    def is_predator(self, fig):
        """
        A predator = lion or tiger
        """
        return fig.upper() == LION or fig.upper() == TIGER

    def is_opponent(self, fig1, fig2):
        return fig1.islower() and fig2.isupper() or fig1.isupper() and fig2.islower()
    
    def is_opp_den(self, board, field, player):
        """
        Check wheather the field is opponent's den (→ win)
        """
        x, y = field
        p0wins = (player.id == P0 and x > N / 2)
        p1wins = (player.id == P1 and x == 0)
        return BOARD[x][y] == DEN and (p0wins or p1wins)

    def predator_jumps(self, board, field, dir_x, dir_y):
        """
        TODO: returns a field which is on the opposite site of the pond
                (on condition there's no opponent's rat on predator's way)
        """
        x, y = field
        predator = board[x][y]
        while True:
            x, y = x + dir_x, y + dir_y
            if self.on_board(board, (x, y)) is False:
                return None

            neigh = board[x][y]
            if self.is_rat(neigh) and self.is_opponent(predator, neigh):
                return None
            if self.is_meadow((x, y)):
                return (x, y)

    def get_neighbour(self, board, figure, field, direction, player):
        """
        Return all possible would-be fields, into which the figure can move
        """
        x, y = field
        a, b = direction
        neighbour = (x+a, y+b)
        if self.on_board(board, neighbour) is False:
            return None

        if self.is_meadow(neighbour) or \
           self.is_trap(neighbour) or \
           self.is_opp_den(board, neighbour, player):
            return neighbour

        if self.is_rat(figure) and self.is_pond(neighbour):
            return neighbour

        if self.is_predator(figure) and self.is_pond(neighbour):
            return self.predator_jumps(board, field, a, b)

        return None

    def get_moves(self, board, player):
        """
        Return list of (f, (x, y)) → figure f can move to (x, y)
        f is a tuple in form of (animal, (pos_x, pos_y))
        """
        moves = []
        for figure in player.figures.items():
            fig, field = figure
            for direction in DIRS:
                neigh_pos = self.get_neighbour(board, fig, field, direction, player)
                if neigh_pos is not None:
                    if self.is_free(board, neigh_pos):
                        moves.append((figure, neigh_pos))
                    elif self.can_beat(fig, field, neigh_pos):
                        moves.append((figure, neigh_pos))

        # TODO move if can beat
        return moves

    def random_move(self, board, player):
        p = self.s.player_0 if player == P0 else self.s.player_1
        return random.choice(self.get_moves(board, p))

    def do_move(self, move, player_id):
        # Get a player based on it's id
        p = self.s.player_0 if player_id == P0 else self.s.player_1
        opp = self.s.player_0 if player_id == P1 else self.s.player_1

        # Unpack a move
        (fig, (src_x, src_y)), (dst_x, dst_y) = move

        self.s.no_beats += 1

        if self.is_free(self.s.board, (dst_x, dst_y)) is False:
            print("{} bije {}".format(fig, self.get_fig((dst_x, dst_y))))
            opp.figure_loss(self.get_fig((dst_x, dst_y)))
            self.s.no_beats = 0

        self.s.board[src_x][src_y] = BOARD[src_x][src_y]
        self.s.board[dst_x][dst_y] = fig

        p.figures[fig] = (dst_x, dst_y)
    
    def terminal(self):
        # One of the player lacks figures
        if self.s.player_0.no_figures():
            dprint("P0 has no figures")
            return P1
        if self.s.player_1.no_figures():
            dprint("P1 has no figures")
            return P0

        # A trap is taken
        if self.s.board[0][3] != FREE:
            dprint("P1 has taken a den")
            return P1
        if self.s.board[8][3] != FREE:
            dprint("P0 has taken a den")
            return P0

        # Game lasts too long
        if self.s.no_beats > BEATS_TRESH:
            p0strong = self.s.player_0.get_strongest()
            p1strong = self.s.player_1.get_strongest()
            if p0strong > p1strong:
                dprint("P0 has a better figure")
                return P0
            if p1strong > p0strong:
                dprint("P1 has a better figure")
                return P1

            p0trap_dist = self.s.player_0.dists_to_trap(self.s.board)
            p1trap_dist = self.s.player_1.dists_to_trap(self.s.board)

            for i in range(min(len(p0trap_dist), len(p1trap_dist))):
                if p0trap_dist[i] > p1trap_dist[i]:
                    dprint("P0 is closer to den")
                    return P0
                if p1trap_dist[i] > p0trap_dist[i]:
                    dprint("P1 is closer to den")
                    return P1
            print("P1 moved second")
            return P1  # because P0 always moves 1st

        return None

    def random_game(self, player):
        """
        Play a random game from a current state and afterall restore init state
        """
        # Do backup or current state
        # backup = JungleState(self.s.player_0, self.s.player_1, player, self.s,board, self.no_beats)
        while True:
            if player == P0:
                move = self.random_move(self.s.board, player)
            else:
                move = self.random_move(self.s.board, player)
            ((fig, src), dst) = move
            print("next move: {}: {} → {}".format(fig, src, dst))
            print(self)
            print(sorted(self.s.player_0.figures.keys()))
            print(sorted(self.s.player_1.figures.keys()))

            # input()
            os.system('cls' if os.name == 'nt' else 'clear')

            self.do_move(move, player)

            term = self.terminal()
            if term is not None:
                print(self)
                print("Player{} wins!".format(term))
                # Restore backup
               # # self.

                return term

            player = 1 - player

    def __str__(self):
        res = [b[:] + [" ", str(i)] for i, b in enumerate(BOARD)]
        for fig, (a, b) in self.s.player_0.figures.items():
            res[a][b] = fig

        for fig, (a, b) in self.s.player_1.figures.items():
            res[a][b] = fig

        res = ["0123456"] + res
        return '\n'.join(''.join(roww) for roww in res)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    jungle = Jungle()
    print(jungle)
    print(jungle.s.player_0.figures)
    print(jungle.s.player_1.figures)

    jungle.random_game(P0)
