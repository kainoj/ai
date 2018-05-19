import random
import os

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
RAT = 'R'
TIGER = 'T'
LION = 'L'
FIGURES = {RAT: 0, 'C': 1, 'D': 2, 'W': 3, 'J': 4, TIGER: 5, LION: 6, 'E': 7}

DIRS = {'U': (0, -1), 'D': (0, 1), 'R': (1, 0), 'L': (-1, 0)}

P0 = 0  # Player 0
P1 = 1  # Player 1

N = 9   # Board height
M = 7   # Board width

TRAP = '#'
FREE = '.'
DEN = '*'
POND = '~'


class Player():

    def __init__(self, id, board):
        self.id = id
        self.figures = {elem: (i, j) for i, row in enumerate(board) 
                        for j, elem in enumerate(row)
                        if id == P0 and elem.isupper()
                        or id == P1 and elem.islower()}


class Jungle():

    def __init__(self):
        self.boad = ['L.....T',  # P0  (capital)
                     '.D...C.',
                     'R.J.W.E',
                     '.......',
                     '.......',
                     '.......',
                     'e.w.j.r',
                     '.c...d.',
                     't.....l']  # P1

        # self.boad = ['L.....T',  # P0
        #              '.D...C.',
        #              '..J.W.E',
        #              '.....t.',
        #              '.r...R.',
        #              '.......',
        #              'e.w.j..',
        #              '.c...d.',
        #              '......l']  # P1
        self.board = [list(row) for row in self.boad]

        self.player_0 = Player(P0, self.boad)
        self.player_1 = Player(P1, self.boad)

    def can_beat(self, fig1, fig2, fig2pos):
        """
        Can `fig1` beat `fig2`? (is fig1 equal or stronger than fig2)?
        """
        # If fig2 is in a trap
        if self.isTrap(fig2pos):
            return True

        fig1 = fig1.upper()
        fig2 = fig2.upper()

        if fig1 == 'R' and fig2 == 'E':
            return True
        return FIGURES[fig1] >= FIGURES[fig2]

    def on_board(self, board, field):
        x, y = field
        return 0 <= x and x < 9 and 0 <= y and y < 7

    def is_meadow(self, board, field):
        """
        Check if BASIC move is allowed (a field is a meadow)
        """
        x, y = field
        return BOARD[x][y] == FREE and board[x][y] == FREE

    def is_free_trap(self, board, field):
        """
        Check if a `field` is a free field which is a trap
        """
        x, y = field
        return BOARD[x][y] == TRAP and board[x][y] == FREE

    def is_opp_den(self, board, field, player):
        """
        Check wheather the field is opponent's den (→ win)
        """
        x, y = field
        p0wins = (player.id == P0 and x > N / 2)
        p1wins = (player.id == P1 and x == 0)
        return BOARD[x][y] == DEN and (p0wins or p1wins)

    def is_pond(self, board, field):
        x, y = field
        return BOARD[x][y] == POND and board[x][y] == FREE

    def is_rat(self, fig):
        return fig.upper() == RAT

    def is_predator(self, fig):
        """
        A predator = lion or tiger
        """
        return fig.upper() == LION or fig.upper() == TIGER

    def is_opponent(self, fig1, fig2):
        return fig1.islower() and fig2.isupper() or fig1.isupper() and fig2.islower()

    def predator_jumps(self, board, field, dir_x, dir_y):
        x, y = field
        predator = board[x][x]
        while True:
            x, y = x + dir_x, y + dir_y
            if self.on_board(board, (x, y)) is False:
                return None

            neigh = board[x][y]
            if self.is_rat(neigh) and self.is_opponent(predator, neigh):
                return None
            if self.is_meadow(board, (x, y)):
                return (x, y)
            # TODO: bicie przy wyjściu z wody

    def get_moves(self, board, player):
        """
        Return list of (f, (x, y)) = figure f can move to (x, y)
        f is a tuple in form of (animal, (pos_x, pos_y))
        """
        moves = []
        for figure in player.figures.items():
            fig, field = figure
            x, y = field
            for a, b in sorted(DIRS.values()):
                neighbour = (x+a, y+b)
                if self.on_board(board, neighbour):
                    if self.is_meadow(board, neighbour) or self.is_free_trap(board, neighbour) or self.is_opp_den(board, neighbour, player):
                        moves.append((figure, neighbour))

                    if self.is_pond(board, neighbour) and self.is_rat(fig):
                        moves.append((figure, neighbour))

                    if self.is_pond(board, neighbour) and self.is_predator(fig):
                        jump = self.predator_jumps(board, field, a, b)
                        if jump is not None:
                            moves.append((figure, jump))
        # TODO move if can beat
        return moves

    def random_move(self, board, player):
        p = self.player_0 if player == P0 else self.player_1
        return random.choice(self.get_moves(board, p))

    def do_move(self, move, player):
        p = self.player_0 if player == P0 else self.player_1
        (fig, (src_x, src_y)), (dst_x, dst_y) = move
        self.board[src_x][src_y] = BOARD[src_x][src_y]
        self.board[dst_x][dst_y] = fig

        p.figures[fig] = (dst_x, dst_y)

    def play(self):
        player = P0
        while True:
            if player == P0:
                move = self.random_move(self.board, player)
            else:
                move = self.random_move(self.board, player)
            ((fig, src), dst) = move
            print("next move: {}: {} → {}".format(fig, src, dst))
            print(self)
            input()
            os.system('cls' if os.name == 'nt' else 'clear')

            self.do_move(move, player)
            player = 1 - player

    def __str__(self):
        res = [b[:] + [" ", str(i)] for i, b in enumerate(BOARD)]
        for fig, (a, b) in self.player_0.figures.items():
            res[a][b] = fig

        for fig, (a, b) in self.player_1.figures.items():
            res[a][b] = fig

        res = ["0123456"] + res
        return '\n'.join(''.join(roww) for roww in res)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    jungle = Jungle()
    print(jungle)
    print(jungle.player_0.figures)
    print(jungle.player_1.figures)

    jungle.play()
