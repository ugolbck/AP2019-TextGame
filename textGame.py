# Text-based game
# Assignment 4
# Python 3.6
# Ugo Loobuyck

import sys
import os
import time
from timeit import default_timer as d_t
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
    
    def getPosition(self):
        return self._position


class Commands:
    ''' Set of available user commands '''
    ''' Not very useful superclass but inheritance was required by the assignment '''
    def __init__(self):
        self.cardinals = ['N', 'S', 'E', 'W']
        self.opposites = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        self.movables = ['USABLE', 'MOVE']
        

class Globals(Commands):
    def __init__(self):
            super().__init__()

    def help(self):
        os.system("clear")
        print('##      Welcome to the help center      ##')
        print('##                                      ##')
        print('##    To see the available commands,    ##')
        print('##           enter "commands"           ##')
        print('##                                      ##')
        print('##    Some commands require to enter    ##')
        print('##     a direction or an item name:     ##')
        print('##     "open N", "take plant" etc...    ##')
        print('##                                      ##')
        print('##       Enter "show" to observe        ##')
        print('##           your environment           ##')
        print('##                                      ##')
        print('##         Enter "quit" to quit         ##\n')

    def show(self, position, house_map):
        ''' Void method that shows the player his environment '''
        available_doors = [key for key, val in house_map[position].items() if val and key in self.cardinals]
        available_items = [key for key in house_map[position]['itemlist'].keys()]
        print()
        print('-'*33)
        time.sleep(0.1)
        print('You are now in the', position + '.')
        time.sleep(0.2)
        print('Available doors:', ', '.join(available_doors)) if available_doors else print('There are no doors. You are basically in jail.')
        time.sleep(0.2)
        print('Available items:', ', '.join(available_items)) if available_items else print('There are no useful items in this room.')
        time.sleep(0.2)
        print('-'*33)
        time.sleep(0.1)
        print()

    def quit(self):
        ''' Quits the game '''
        print('Oh.', end='\r')
        time.sleep(0.3)
        print('Oh..', end='\r')
        time.sleep(0.3)
        print('Oh...')
        time.sleep(0.3)
        print('You don\'t want to play anymore.', end='\r')
        time.sleep(0.3)
        print('You don\'t want to play anymore..', end='\r')
        time.sleep(0.3)
        print('You don\'t want to play anymore...')
        time.sleep(0.6)
        print('Come back any time!')

        sys.exit()
    
    def commands(self, glob_commands, play_commands):
        ''' Prints all the available user & globabl commands '''
        print('Here are the available commands of the game:\n')
        time.sleep(0.2)
        for i in glob_commands:
            print(i)
        print()
        for i in play_commands:
            if i == 'go' or i == 'open' or i == 'unlock':
                print(i, '<DIR>')
            elif i == 'take' or i == 'drop' or i == 'use' or i == 'pee' or i == 'watch' or i == 'look' or i == 'defuse':
                print(i, '<ITEM>')
        time.sleep(0.2)
        print()
    
    def inventory(self, inv):
        if len(inv) == 0:
            print('You are not holding anything.')
            time.sleep(0.2)
        else:
            l_items = [k for k in inv.keys()]
            print('You are currently holding a ' + ' and a '.join(l_items))
            time.sleep(0.2)
        print()

    def window(self):
        os.system("clear")

    def pee(self, position):
        if position == 'Bathroom':
            print('Peeing.', end='\r')
            time.sleep(1)
            print('Peeing..', end='\r')
            time.sleep(1)
            print('Peeing...')
            time.sleep(1.8)
            print('That was a big one! On with the quest now, you have a bomb to defuse.')
            time.sleep(0.2)
        else:
            print('It\'s neither the place nor the moment to do that.')
            time.sleep(0.2)
        print()


class Actions(Commands):
    def __init__(self):
            super().__init__()

    def go(self, old_position, house_map, direction):
        ''' Method that updates player position and returns it '''
        available_doors = [key for key, val in house_map[old_position].items() if val and key in self.cardinals]
        available_items = [key for key in house_map[old_position]['itemlist'].keys()]
        if direction.upper() in available_doors:
            if house_map[old_position][direction.upper()][1] == 'closed':
                print('That door is closed.')
                time.sleep(0.2)
                return old_position
            elif house_map[old_position][direction.upper()][1] == 'locked':
                print('That door is locked. Find the key that opens it.')
                time.sleep(0.2)
                return old_position
            elif house_map[old_position][direction.upper()][1] == 'open':
                new_position = house_map[old_position][direction.upper()][0]
                return new_position
        else:
            print('There is no door in that direction. Enter another direction. Enter "show" to see the doors.')
            return old_position

    def open(self, position, house_map, direction):
        ''' Void method that updates the status of a door from closed -> open (in both rooms it connects) '''
        available_doors = [key for key, val in house_map[position].items() if val and key in self.cardinals]
        if direction.upper() in available_doors:
            if house_map[position][direction.upper()][1] == 'locked':
                print('That door is locked. Find the key that opens it.')
                time.sleep(0.2)
            elif house_map[position][direction.upper()][1] == 'open':
                print('That door is already open!')
                time.sleep(0.2)
            elif house_map[position][direction.upper()][1] == 'closed':
                next_room = house_map[position][direction.upper()][0]
                house_map[next_room][self.opposites[direction.upper()]][1] = 'open'
                house_map[position][direction.upper()][1] = 'open'
                print('The door is now open!')
                time.sleep(0.2)
        else:
            print('There is no door in that direction. Enter another direction. Enter "show" to see the doors.')
            time.sleep(0.2)
        print()
            
    def take(self, inventory, position, house_map, item):
        available_items = [key for key in house_map[position]['itemlist'].keys()]
        if not available_items:
            print('There are no uselful items in this room.')
            time.sleep(0.2)
        elif item not in available_items:
            print('The item you want to take isn\'t in this room.')
            time.sleep(0.2)
        elif len(inventory) >= 2:
            print('You are already holding 2 items. Try droping one!')
            time.sleep(0.2)
        else:
            if house_map[position]['itemlist'][item][0] not in self.movables:
                print('You can\'t take that item, it\'s too heavy.')
                time.sleep(0.2)
            else:
                inventory[item] = house_map[position]['itemlist'][item]
                del house_map[position]['itemlist'][item]
                print('You have picked up the', item)
                time.sleep(0.2)
        print()
            
    def drop(self, inventory, position, house_map, item):
        house_map[position]['itemlist'][item] = inventory[item]
        del inventory[item]
        print('You have dropped the', item)
        time.sleep(0.2)
        print()

    def unlock(self, inventory, position, house_map, direction):
        available_doors = [key for key, val in house_map[position].items() if val and key in self.cardinals]
        if direction.upper() in available_doors:
            if house_map[position][direction.upper()][1] != 'locked':
                print('That door is already unlocked!')
                time.sleep(0.2)
            else:
                if 'key' not in inventory:
                    print('You need a key to open that door.')
                    time.sleep(0.2)
                else:
                    next_room = house_map[position][direction.upper()][0]
                    house_map[next_room][self.opposites[direction.upper()]][1] = 'closed'
                    house_map[position][direction.upper()][1] = 'closed'
                    print('The door is unlocked, you can now open it.')
                    time.sleep(0.2)
        else:
            print('There is no door in that direction. Enter another direction. Enter "show" to see the doors.')
            time.sleep(0.2)
        print()

    def watch(self, position, item):
        if item == 'tv':
            if position == 'LivingRoom' or position == 'Bedroom':
                print('Let\'s watch some TV.')
                time.sleep(2.5)
                print('What a waste of time that was. You have a bomb to defuse!')
                time.sleep(0.2)
            else:
                print('There is no TV in that room.')
                time.sleep(0.2)
        else:
            print('Why would you want to watch this? Try something else.')
            time.sleep(0.2)
        print()

    def look(self, inventory, item, code):
        if item == 'code':
            if item in inventory:
                print('The code is', code)
                time.sleep(0.2)
            else:
                print('Find the code before looking at it!')
                time.sleep(0.2)
        else:
            print('You are looking at the wrong item. Try to find the code!')
            time.sleep(0.2)
        print()

    def defuse(self, position, item, code):
        if item == 'bomb':    
            if position == 'Garage':
                if input('Enter the 4 digits code: ') == str(code):
                    return True
                else:
                    print('Wrong code.')
                    time.sleep(0.2)
                    return False
            else:
                print('There is nothing to defuse here.')
                time.sleep(0.2)
        else:
            print('You can\'t defuse that.')
            time.sleep(0.2)
        print()


class Game:
    ''' Main class of the game '''
    def __init__(self, house, player, global_set, action_set):
        self.house = house
        self.player = player
        self.glob = global_set
        self.action = action_set
        self.global_actions = ['help', 'show', 'quit', 'commands', 'inventory', 'window', 'pee']
        self.player_actions = ['go', 'open', 'unlock', 'take', 'drop', 'watch', 'look', 'defuse']
        self._code = ''
        self.win = False
        self.lose = False
        self.play()

    def play(self):
        ''' After initialization, everything happens here '''
        self.title()
        self.player.setPosition(self.house.getPosition())
        self._code = self.randCode()
        name = self.playerName()
        diff = self.difficulty()
        self.intro(name)

        if self.checkReady():
            self.glob.show(self.player.getPosition(), self.house.house_map)
            start = d_t()
            end = start

            ''' Actual player experience '''
            while not self.win and not self.lose:
                print('## You have {} seconds left. ##'.format(int(diff - (end - start))))
                comm = self.prompt()
                if len(comm) == 1:
                    # Argumentless commands
                    if comm[0] == 'help':
                        self.glob.help()
                    elif comm[0] == 'show':
                        self.glob.show(self.player.getPosition(), self.house.house_map)
                    elif comm[0] == 'quit':
                        self.glob.quit()
                    elif comm[0] == 'commands':
                        self.glob.commands(self.global_actions, self.player_actions)
                    elif comm[0] == 'inventory':
                        self.glob.inventory(self.player.inventory)
                    elif comm[0] == 'window':
                        self.glob.window()
                    elif comm[0] == 'pee':
                        self.glob.pee(self.player.getPosition())
                elif len(comm) == 2:
                    # 1 argument commands
                    if comm[0] == 'go':
                        self.player.setPosition(self.action.go(self.player.getPosition(), self.house.house_map, comm[1]))
                        self.glob.show(self.player.getPosition(), self.house.house_map)
                    elif comm[0] == 'open':
                        self.action.open(self.player.getPosition(), self.house.house_map, comm[1])
                    elif comm[0] == 'unlock':
                        self.action.unlock(self.player.inventory, self.player.getPosition(), self.house.house_map, comm[1])
                    elif comm[0] == 'take':
                        self.action.take(self.player.inventory, self.player.getPosition(), self.house.house_map, comm[1])
                    elif comm[0] == 'drop':
                        self.action.drop(self.player.inventory, self.player.getPosition(), self.house.house_map, comm[1])
                    elif comm[0] == 'watch':
                        self.action.watch(self.player.getPosition(), comm[1])
                    elif comm[0] == 'look':
                        self.action.look(self.player.inventory, comm[1], self._code)
                    elif comm[0] == 'defuse':
                        self.win = self.action.defuse(self.player.getPosition(), comm[1], self._code)
                end = d_t()
                if end - start >= diff:
                    # Only gets triggered after a command but gives the impression of real time
                    self.lose = True

            if self.win:
                self.winScreen()
            elif self.lose:
                self.lossScreen()
    
    def difficulty(self):
        levels = ['easy', 'hard']
        print('\nChoose your level of difficulty:\n')
        print('{0:10} | {1:^12}'.format('easy', 'hard'))
        print('-'*25)
        print('{0:10} | {1:^12}'.format('5 minutes', '2 minutes'))
        dif = input('\n> ')
        while dif.lower() not in levels:
            dif = input('Something went wrong. Choose between easy and hard\n> ')
        return 120 if dif == 'hard' else 300

    def prompt(self):
        comm = input('\nWhat do you want to do?\n> ').lower().split(' ')
        while comm[0] not in self.global_actions and comm[0] not in self.player_actions or len(comm) > 2:
            comm = input('That doesn\'t seem like something you can do, try something else.\n\n> ').lower().split(' ')
        if len(comm) == 1:
            return comm
        elif len(comm) == 2:
            return comm[0], comm[1]
        
    def title(self):
        os.system("clear")
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

    def playerName(self):
        return input('What is your character\'s name?\n> ')
        
    def intro(self, name):
        print('* You are quietly asleep. *', end='\r')
        time.sleep(0.7)
        print('* You are quietly asleep.. *', end='\r')
        time.sleep(0.7)
        print('* You are quietly asleep... *')
        time.sleep(1.5)
        print('* When suddently. *', end='\r')
        time.sleep(0.7)
        print('* When suddently.. *', end='\r')
        time.sleep(0.7)
        print('* When suddently... *', end='\r')
        time.sleep(1.5)
        print('* When suddently... a strange voice wakes you up. *', end='\r')
        time.sleep(0.7)
        print('* When suddently... a strange voice wakes you up.. *', end='\r')
        time.sleep(0.7)
        print('* When suddently... a strange voice wakes you up... *')
        time.sleep(1.5)
        
        print(name + ', can you hear me ?')
        time.sleep(2.5)
        print('Good. let\'s play a game. I hid a bomb somewhere in the house, your job is to find it and, if you discover the right code, to defuse it.')
        time.sleep(5.5)
        print('I will assist you in that delicate mission, and update you on the time you have left.\n')
        time.sleep(5.5)
    
    def checkReady(self):
        ans = input('Are you ready to play (yes/anything else)?\n> ')
        return True if ans.lower() == 'yes' else False

    def winScreen(self):
        print()
        print('########### CONGRATULATIONS ###########')
        print('########     YOU SURVIVED!     ########')
        print('###  Checkout github.com/ugolbck/  ####')
        print('########   for source code.    ########')
        print()

    def lossScreen(self):
        print()
        print()
        print('########### BOOOOOOOOOOOOOM ###########')
        print('########       YOU LOSE!       ########')
        print('###  Checkout github.com/ugolbck/  ####')
        print('########   for source code.    ########')
        print()

    def randCode(self):
        code_list = [str(random.randint(0,9)) for i in range(4)]
        return ''.join(code_list)


if __name__ == '__main__':
    game = Game(House(sys.argv[1]), Player(), Globals(), Actions())
    