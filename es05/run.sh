#!/bin/bash

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

exec /usr/bin/python3 -u $DIR/reversi_player_random.py
