import sys
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
    def __init__(self, i_name, i_position, i_type, i_function=None):
        self._name = i_name
        self._position = i_position
        self._type = i_type
        self._function = i_function


class House:
    ''' Class that defines the house and holds its components '''
    def __init__(self, filename):
        self.filename = filename
        self._rooms = {}
        self._doors = []
        self._items = {}
        fileParser(filename)

    def fileParser(self, myFile):
        ''' Parses the config file to store data in dictionaries '''
        with open(myFile) as f:
            lines = f.readlines()

        # Desired result:
        # bedroom = Room(self._doors, self._items)
        # + Items/Doors instanciated ??


class Game:
    ''' Main class of the game '''
    def __init__(self, house, character):
        self.house = house
        self.character = character
        
    def do_stuff(self):
        pass



if __name__ == '__main__':
    game = Game(House(sys.argv[1]), Character())
    game.do_stuff()
