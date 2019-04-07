import os
import time
import random
from timeit import default_timer as d_t
from player import Player
from house import House
from global_com import Globals   
from actions import Actions


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
        print('* When suddenly. *', end='\r')
        time.sleep(0.7)
        print('* When suddenly.. *', end='\r')
        time.sleep(0.7)
        print('* When suddenly... *', end='\r')
        time.sleep(1.5)
        print('* When suddenly... a strange voice wakes you up. *', end='\r')
        time.sleep(0.7)
        print('* When suddenly... a strange voice wakes you up.. *', end='\r')
        time.sleep(0.7)
        print('* When suddenly... a strange voice wakes you up... *')
        time.sleep(1.5)
        
        print(name + ', can you hear me ?')
        time.sleep(2)
        print('Good. Let\'s play a game. I hid a bomb somewhere in the house, your job is to find it and, if you discover the right code, to defuse it.')
        time.sleep(5)
        print('I will assist you in that delicate mission, and update you on the time you have left.\n')
        time.sleep(5)
    
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
