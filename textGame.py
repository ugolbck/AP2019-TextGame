import sys
import os
import time
import random
from collections import deque


class Character:
    ''' Class that holds information on the player '''
    def __init__(self):
        self._position = ''
        self._inventory = deque(maxlen=2)
    
    def getPosition(self):
        return self._position

    def getInventory(self):
        return self._inventory
    
    def setPosition(self, position):
        self._position = position


class Item:
    ''' Class that defines items '''
    def __init__(self, name_item, position_item, type_item, function_item=None):
        self._name = name_item
        self._position = position_item
        self._type = type_item
        self._function = function_item


class House:
    ''' Class that defines the house and holds its components '''
    def __init__(self, filename):
        self.filename = filename
        self._rooms = {}
        self._doors = []
        self._items = {}
        self.fileParser(filename)

    def fileParser(self, myFile):
        ''' Parses the config file to store data in dictionaries '''
        with open(myFile) as f:
            lines = f.readlines()

        # Desired result:
        # bedroom = Room(self._doors, self._items)
        # + Items/Doors instanciated ??
        # Probably instantiate everything in House with the current Item class and similar Door class
        # -> faire une liste d'instances d'Items (same Doors) et le passer en créant chaque Room


class Game:
    ''' Main class of the game '''
    def __init__(self, house, character):
        self.house = house
        self.character = character
        
    def do_stuff(self):
        os.system("clear")



if __name__ == '__main__':
    game = Game(House(sys.argv[1]), Character())
    game.do_stuff()
