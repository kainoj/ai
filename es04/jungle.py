import os
import copy
from jungle_engine import P0, P1, INIT_BOARD, BOARD, FIGURES, random_move, do_move, terminal, random_game, get_moves


MOVES_PER_ANALYZE = 2000


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

    def get_copy(self):
        return State(copy.deepcopy(self.board),
                     copy.deepcopy(self.player_0),
                     copy.deepcopy(self.player_1),
                     copy.deepcopy(self.whos_now),
                     0)


class Player():

    def __init__(self, id, board):
        self.id = id
        self.figures = {elem: (i, j) for i, row in enumerate(board) 
                        for j, elem in enumerate(row)
                        if id == P0 and elem.isupper()
                        or id == P1 and elem.islower()}

    def figure_loss(self, figure):
        if figure in self.figures:
            self.figures.pop(figure)

    def get_strongest(self):
        return max([FIGURES[f.upper()] for f in self.figures.keys()])

    def dists_to_trap(self, board):
        # Trap coords
        tx, ty = (0, 3) if self.id == P1 else (8, 3)
        return sorted([abs(tx - fx) + abs(ty - fy) for fx, fy in self.figures.values()])

    def no_figures(self):
        return len(self.figures) == 0
    
    def who_am_i(self):
        print("I am player{}".format(self.id))

    def get_copy(self):
        return copy.deepcopy(self)


class Jungle():

    def __init__(self):
        self.s = State(INIT_BOARD,
                       Player(P0, INIT_BOARD),
                       Player(P1, INIT_BOARD),
                       P0, 0)

    def __str__(self):
        res = [b[:] + [" ", str(i)] for i, b in enumerate(BOARD)]
        for fig, (a, b) in self.s.player_0.figures.items():
            res[a][b] = fig

        for fig, (a, b) in self.s.player_1.figures.items():
            res[a][b] = fig

        res = ["0123456    <-- P0 (capital letters)"] + res
        return '\n'.join(''.join(roww) for roww in res)

    def __repr__(self):
        return self.__str__()

    def play(self, player_id):
        move = None
        while True:
            if player_id == P0:
                move = random_move(self.s.board, self.s.player_0)
                # move = self.analyze(self.s.player_0.get_copy())
            else:
                move = self.analyze(self.s, self.s.player_1.get_copy())

            if move is None:
                return 1-player_id

            self.s = do_move(self.s, move, player_id) 

            term = terminal(self.s)
            if term is not None:
                return term
            player_id = 1-player_id

    def analyze(self, state, player):
        """
        Play some random games for every possible state
        """
        games_played = 0
        p0_best, p1_best = 0, 0  # p0's best analyze won p0_best games
        p0_best_move, p1_best_move = None, None
        for move in get_moves(state.board, player):
            p0won, p1won = 0, 0
            for _ in range(20):
                who_won, plys = random_game(state.get_copy(), player.id)
                games_played += plys
                if who_won == P0:
                    p0won += 1
                else:
                    p1won += 1

            if p0won > p0_best:
                p0_best = p0_best
                p0_best_move = move

            if p1won > p1_best:
                p1_best = p1_best
                p1_best_move = move

            if games_played > MOVES_PER_ANALYZE:
                break
        if player == P0:
            return p0_best_move
        return p1_best_move


if __name__ == "__main__":
    player1won = 0
    games = 10

    player = P0
    for _ in range(games):
        jungle = Jungle()
        if jungle.play(player) == P1:
            player1won += 1
        player = 1 - player
    print("Player1 won {} / {} games".format(player1won, games))