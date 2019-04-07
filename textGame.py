# Text-based game
# Assignment 4
# Python 3.6
# Ugo Loobuyck
# To run: 'python3 textGame.py gameConfiguration.py'

import sys
from player import Player
from house import House
from global_com import Globals   
from actions import Actions
from game import Game

if __name__ == '__main__':
    game = Game(House(sys.argv[1]), Player(), Globals(), Actions())
    