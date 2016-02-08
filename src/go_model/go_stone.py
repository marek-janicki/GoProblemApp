class GoStone:
    '''An object representation of a Go Stone.
       
    Just wraps its current
    position and colour. Note that colour is stored as a boolean
    with true being equivalent to black.
    '''
    BLACK = True

    def __init__(self, x, y, colour):
        '''A basic constructor.

        x and y denote the position on the board, whilst colour
        is a boolean that is true iff the stone is black.
        '''
        self.x = x
        self.y = y
        self.colour = colour

    def isBlack(self):
        ''' True iff the stone is black'''
        return self.colour == GoStone.BLACK

    def __eq__(self, other):
        '''If colour and position is the same, the stones are the same'''
        if (other == None):
            return False
        return (self.x == other.x) and (self.y==other.y) and (self.isBlack() == other.isBlack())
           
    def __ne__(self, other):
        '''If colour and position are different, the stones are different'''
        return not self.__eq__(other)

    def __hash__(self):
        '''Needed to allow for making sets from lists. This isn't a psedo-random hash.'''

        thisHash = self.x + self.y * 64
        if (self.colour):
            thisHash = 2 * thisHash
        return thisHash


if __name__ == '__main__':
    x = GoStone(1, 2, True)
    print x.isBlack()



