# Text-based game
# Assignment 4
# Ugo Loobuyck

import sys
import os
import time
import random


class Player:
    ''' Class that holds information on the player '''
    def __init__(self):
        self._position = ''
        self.inventory = {}
    
    def getPosition(self):
        return self._position
    
    def setPosition(self, position):
        self._position = position

            

class House:
    ''' Class that defines the house and holds its components '''
    N = 'N'
    S = 'S'
    E = 'E'
    W = 'W'
    ITEMS = 'itemlist'

    def __init__(self, filename):
        self.filename = filename
        self.house_map = {}
        self._position = ''
        self.fileParser(filename)

    def fileParser(self, myFile):
        ''' Parses the config file to store data in dictionaries '''
        with open(myFile) as f:
            lines = f.readlines()
        for line in lines:
            split = line.split(' ')
            if split[0] == 'room':
                self.house_map[split[1][:-1]] = {
                                            self.N: '',
                                            self.S: '',
                                            self.E: '',
                                            self.W: '',
                                            self.ITEMS: {}
                                            }
            elif split[0] == 'door':
                self.house_map[split[3]][split[1][-1]] = [split[4][:-1], split[2]]
                self.house_map[split[4][:-1]][split[1][0]] = [split[3], split[2]] 
            elif split[0] == 'item':
                self.house_map[split[2]][self.ITEMS][split[1]] = (split[3], split[4][:-1]) if len(split) == 5 else (split[3][:-1], '')
            elif split[0] == 'start':
                self._position = line.split(' ')[1]

    def getRoomMap(self):
        return self.house_map
    
    def getPosition(self):
        return self._position


class Commands:
    ''' Set of available user commands '''
    def __init__(self):
        self.cardinals = ['N', 'S', 'E', 'W']
        self.opposites = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        self.movables = ['USABLE', 'MOVE']
        
    def show(self, position, house_map):
        ''' Void method that shows the player his environment '''
        available_doors = [key for key, val in house_map[position].items() if val and key in self.cardinals]
        available_items = [key for key in house_map[position]['itemlist'].keys()]
        print('You are now in the', position + '.')
        time.sleep(0.2)
        print('Available doors:', ', '.join(available_doors)) if available_doors else print('There are no doors. You are basically in jail.')
        time.sleep(0.2)
        print('Available items:', ', '.join(available_items)) if available_items else print('There are no useful items in this room.')
        time.sleep(0.2)

    def quit(self):
        ''' Quits the game '''
        print('Bye bye!\n')
        sys.exit()
    
    def commands(self, glob_commands, play_commands):
        ''' Prints all the available user & globabl commands '''
        print('Here are the available commands of the game:\n')
        for i in glob_commands:
            print(i)
        for i in play_commands:
            if i == 'go' or i == 'open' or i == 'unlock':
                print(i, '<DIR>')
            elif i == 'take' or i == 'drop' or i == 'use' or i == 'pee' or i == 'watch' or i == 'look' or i == 'defuse':
                print(i, '<ITEM>')
    
    def inventory(self, inv):
        if len(inv) == 0:
            print('You are not holding anything.')
        else:
            print(k for k in inv.keys())

    def go(self, old_position, house_map, direction):
        ''' Method that updates player position and returns it '''
        available_doors = [key for key, val in house_map[old_position].items() if val and key in self.cardinals]
        available_items = [key for key in house_map[old_position]['itemlist'].keys()]
        if direction.upper() in available_doors:
            if house_map[old_position][direction.upper()][1] == 'closed':
                print('That door is closed.')
                return old_position
            elif house_map[old_position][direction.upper()][1] == 'locked':
                print('That door is locked. Find the key that opens it.')
                return old_position
            elif house_map[old_position][direction.upper()][1] == 'open':
                new_position = house_map[old_position][direction.upper()][0]
                self.show(new_position, house_map)
                return new_position
        else:
            print('There is no door in that direction. Enter another direction.')
            return old_position

    def open(self, position, house_map, direction):
        ''' Void method that updates the status of a door from closed -> open (in both rooms it connects) '''
        available_doors = [key for key, val in house_map[position].items() if val and key in self.cardinals]
        if direction.upper() in available_doors:
            if house_map[position][direction.upper()][1] == 'locked':
                print('That door is locked. Find the key that opens it.')
            elif house_map[position][direction.upper()][1] == 'open':
                print('That door is already open !')
            elif house_map[position][direction.upper()][1] == 'closed':
                next_room = house_map[position][direction.upper()][0]
                house_map[next_room][self.opposites[direction.upper()]][1] = 'open'
                house_map[position][direction.upper()][1] = 'open'
                print('The door is now open !')
            
        #Update status of given direction door for the current position room AND the room in the given direction

    def take(self, inventory, position, house_map, item):
        available_items = [key for key in house_map[position]['itemlist'].keys()]
        if not available_items:
            print('There are no uselful items in this room.')
        elif item not in available_items:
            print('The item you want to take isn\'t in this room.')
        elif len(inventory) >= 2:
            print('You are already holding 2 items. Try droping one !')
        else:
            if house_map[position]['itemlist'][item][0] not in self.movables:
                print('You can\'t take that item.')
            else:
                print('You have picked up:', item)
                inventory[item] = house_map[position]['itemlist'][item]
                del house_map[position]['itemlist'][item]
            
            

class Game:
    ''' Main class of the game '''
    def __init__(self, house, player, command_set):
        self.house = house
        self.player = player
        self.command = command_set
        self.global_actions = ['show', 'quit', 'commands', 'inventory', 'help']
        self.player_actions = ['go', 'open', 'unlock', 'take', 'drop', 'use', 'pee', 'watch', 'look', 'defuse']
        self.win = False
        self.lose = False
        
    def play(self):
        ''' After initialization, every thing happens here '''
        self.title()
        self.player.setPosition(self.house.getPosition())
        ''' Actual player experience '''
        while not self.win and not self.lose:
            action = self.prompt()
            if len(action) == 1:
                # Argumentless commands
                if action[0] == 'show':
                    self.command.show(self.player.getPosition(), self.house.getRoomMap())
                elif action[0] == 'quit':
                    self.command.quit()
                elif action[0] == 'commands':
                    self.command.commands(self.global_actions, self.player_actions)
                elif action[0] == 'inventory':
                    self.command.inventory(self.player.inventory)
            elif len(action) == 2:
                # 1 argument commands
                if action[0] == 'go':
                    self.player.setPosition(self.command.go(self.player.getPosition(), self.house.getRoomMap(), action[1]))
                elif action[0] == 'open':
                    self.command.open(self.player.getPosition(), self.house.getRoomMap(), action[1])
                    print(self.house.getRoomMap())
                elif action[0] == 'take':
                    self.command.take(self.player.inventory, self.player.getPosition(), self.house.getRoomMap(), action[1])
            
    
    def prompt(self):
        action = input('\nWhat do you want to do ?\n> ').lower().split(' ')
        while action[0] not in self.global_actions and action[0] not in self.player_actions or len(action) > 2:
            action = input('That doesn\'t seem like something you can do, try something else\n\n> ').lower().split(' ')
        if len(action) == 1:
            return action
        elif len(action) == 2:
            return action[0], action[1]
        
    def title(self):
        print('#######################################################')
        # time.sleep(0.4)
        print('################   Welcome to DEFUSE   ################')
        # time.sleep(0.4)
        print('#######################################################')
        # time.sleep(0.8)
        print('###########        Ugo Loobuyck 2019        ###########')
        # time.sleep(0.3)
        print('#######           github.com/ugolbck/           #######')
        # time.sleep(0.3)
        print('###   Project: github.com/ugolbck/AP2019-TextGame   ###')
        # time.sleep(0.3)
        print('#                                                     #')
        # time.sleep(0.3)
        print()

    def intro(self):
        print('You are quietly asleep...')
        print()
    
    def checkReady(self):
        ans = input('Are you ready to play (yes/no)?\n> ')
        return True if ans.lower() == 'yes' else False



if __name__ == '__main__':
    os.system("clear") #To move to 'title' method before release
    game = Game(House(sys.argv[1]), Player(), Commands())
    game.play()