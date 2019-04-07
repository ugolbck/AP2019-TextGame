from commands import Commands
import time
import os

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
