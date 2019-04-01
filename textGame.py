# Text-based game
# Assignment 4
# Ugo Loobuyck

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


class House:
    ''' Class that defines the house and holds its components '''
    N_WALL = 'N'
    S_WALL = 'S'
    E_WALL = 'E'
    W_WALL = 'W'
    ITEMS = 'itemlist'

    def __init__(self, filename):
        self.filename = filename
        self._room_map = {}
        self._position = ''
        self.fileParser(filename)

    def fileParser(self, myFile):
        ''' Parses the config file to store data in dictionaries '''
        with open(myFile) as f:
            lines = f.readlines()
        for line in lines:
            split = line.split(' ')
            if split[0] == 'room':
                self._room_map[split[1][:-1]] = {
                                            self.N_WALL: '',
                                            self.S_WALL: '',
                                            self.E_WALL: '',
                                            self.W_WALL: '',
                                            self.ITEMS: {}
                                            }
            elif split[0] == 'door':
                self._room_map[split[3]][split[1][-1]] = [split[4][:-1], split[2]]
                self._room_map[split[4][:-1]][split[1][0]] = [split[3], split[2]] 
            elif split[0] == 'item':
                self._room_map[split[2]][self.ITEMS][split[1]] = (split[3], split[4][:-1]) if len(split) == 5 else split[3][:-1]
            elif split[0] == 'start':
                self._position = line.split(' ')[1]

    def getRoomMap(self):
        return self._room_map
    
    def getPosition(self):
        return self._position


class Commands:
    ''' List of commands available '''
    @staticmethod
    def funcname():
        pass


class Game:
    ''' Main class of the game '''
    def __init__(self, house, character):
        self.house = house
        self.character = character
        
    def do_stuff(self):
        self.title()
        self.character.setPosition(self.house.getPosition())
        

    def title(self):
        os.system("clear")
        print('#######################################################')
        # time.sleep(0.3)
        print('################   Welcome to DEFUSE   ################')
        # time.sleep(0.3)
        print('###########   Copyright 2019 Ugo Loobuyck   ###########')
        # time.sleep(0.3)
        print('#######           github.com/ugolbck/           #######')
        # time.sleep(0.3)
        print('###   Project: github.com/ugolbck/AP2019-TextGame   ###')
        # time.sleep(0.3)
        print('#                                                     #')
        # time.sleep(0.3)
        print()
        print()

    def intro(self):
        print('You are quietly asleep...')
        print()



if __name__ == '__main__':
    os.system("clear")
    game = Game(House(sys.argv[1]), Character())
    game.do_stuff()
