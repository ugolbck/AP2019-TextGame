
class Player:
    ''' Class that holds information on the player '''
    def __init__(self):
        self._position = ''
        self.inventory = {}
    
    def getPosition(self):
        return self._position
    
    def setPosition(self, position):
        self._position = position
