from reversi_player import Player
import random

class MctsPlayer(Player):

    def loop(self):
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.game.state = self.game.do_mtcs_move(move)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
           
            move = self.game.monte_carlo(self.game.state)
            self.game.state = self.game.do_mtcs_move(move)
            if move is None:
                move = (-1, -1)
            self.say('IDO %d %d' % move)


if __name__ == '__main__':
    player = MctsPlayer()
    player.loop()
