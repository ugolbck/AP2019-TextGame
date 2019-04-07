
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
