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


class Player():

    def __init__(self, id, board):
        self.id = id
        self.figures = {elem: (i, j) for i, row in enumerate(board) 
                        for j, elem in enumerate(row)
                        if id == P0 and elem.isupper()
                        or id == P1 and elem.islower()}


class Jungle():

    def __init__(self):
        self.board = ['L.....T',  # P0  (capital)
                      '.D...C.',
                      'R.J.W.E',
                      '.......',
                      '.......',
                      '.......',
                      'e.w.j.r',
                      '.c...d.',
                      't.....l']  # P1

        # self.board = ['L......',  # P0  (capital)
        #               '.D...C.',
        #               'R.J.WTE',
        #               '.......',
        #               '.......',
        #               '.......',
        #               'e.w.j.r',
        #               '.c...d.',
        #               't.....l']  # P1
        self.board = [list(row) for row in self.board]

        self.player_0 = Player(P0, self.board)
        self.player_1 = Player(P1, self.board)

    def can_beat(self, fig, fig_pos, neigh, neigh_pos):
        """
        Can `figure` beat `neigh`? (is figure equal or stronger than neigh)?
        Assuming neigh is an opponent of figure
        """
        if self.is_opponent(fig, neigh) is False:
            return False

        # If neigh is in a trap
        if self.is_trap(neigh_pos):
            return True
        
        # Rat which is in the pond cannot beat neigh on a meadow 
        if self.is_rat(fig) and self.is_pond(fig_pos) and self.is_meadow(neigh):
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
        x, y = field
        a, b = direction
        neighbour = (x+a, y+b)
        if self.on_board(board, neighbour) is False:
            return None

        if self.is_free_meadow(board, neighbour) or \
           self.is_free_trap(board, neighbour) or \
           self.is_opp_den(board, neighbour, player):
            return neighbour

        if self.is_rat(figure) and self.is_free_pond(board, neighbour):
            return neighbour

        if self.is_predator(figure) and self.is_meadow(neighbour):
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
            x, y = field
            for direction in DIRS:
                neighbour = self.get_neighbour(board, fig, field, direction, player)
                if neighbour is not None:
                    moves.append((figure, neighbour))
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
            print(sorted(self.player_0.figures.keys()))
            print(sorted(self.player_1.figures.keys()))

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
