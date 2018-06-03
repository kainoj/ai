#!/bin/bash

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

exec /usr/bin/pypy -u $DIR/reversi_player_mcts.py

# exec /usr/bin/pypy -u $DIR/reversi_player_random.py

