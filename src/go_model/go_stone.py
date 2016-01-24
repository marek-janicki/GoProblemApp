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

if __name__ == '__main__':
    x = GoStone(1, 2, True)
    print x.isBlack()



