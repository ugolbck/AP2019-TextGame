from commands import Commands
import time
import os

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
