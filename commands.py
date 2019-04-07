
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
     