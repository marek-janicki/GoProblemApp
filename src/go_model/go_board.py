from go_stone import GoStone

class GoBoard:
    '''Stores the board state

    Allows for adding and removing stones, as well as getting
    groups and testing for life.
    '''

    def __init__(self, board_size = 19):
        '''Returns an empty Go Board.

        Board size is set to 19 by default.
        '''
        self.board_size = board_size
        self.board = range(board_size)
        for i in range(board_size):
            self.board[i] = [None for  _ in range(board_size)]

    def get_stone(self, x, y):
        '''Return the stone at position x,y

        Returns a GoStone object or None if none exists, and assumes x and y are integers
        Returns None if out of bounds.
        '''
        if (x < 0) or (y < 0) or (x >= self.board_size) or (y >= self.board_size):
            return None
        return self.board[x][y]

    def is_occupied(self, x, y):
        '''True iff position x,y is occupied'''
        return self.board[x][y] != None

    def add_stone(self, stone):
        '''Adds a stone to the GoBoard.

        Needs to take a stone, otherwise won't know what colour it is.
        TODO - Throw exception if stone is occupied?
        '''
        self.board[stone.x][stone.y] = stone

    def remove_stone(self, *args):
        '''Removes a stone from the Go Board

        Takes in either a GoStone as an argument or
        x and y indices of the stone as afguments.
        Does not remove the stone itself.
        XXX: Does not check if the stone is already removed.
             Could potentially be a source of bugs.
        '''
        if (len(args) == 1):
            x = args[0].x
            y = args[0].y
        else:
            x = args[0]
            y = args[1]

        self.board[x][y] = None

    def remove_stones(self, stones):
        '''Removes every stone in the list from the board.

        Assumes stones is a list of GoStones
        '''
        for stone in stones:
            self.remove_stone(stone)

    def get_group(self, *args):
        '''Get a group centred at a stone

        Takes in either a GoStone as an argument or
        x and y indices of the stone as afguments.
        Returns a list of GoStones
        '''
        if (len(args) == 1):
            original_stone = args[0]
        else:
            original_stone = self.get_stone(args[0], args[1])

        ret_list = []
        self._get_group(original_stone, ret_list)

        #now we unmark all the stones so that future calls don't break
        for stone in ret_list:
            stone.touched = False

        return ret_list

    def _get_group(self, stone, stone_list):
        '''Add stone to stoneList and recursively calls itself on it's neighbours.'''
        stone.touched = True
        stone_list.append(stone)

        for neighbour in self.get_neighbours(stone):
            if ((neighbour.colour == stone.colour) and not (neighbour.__dict__.has_key('touched') and neighbour.touched)):
                self._get_group(neighbour, stone_list)

    def get_neighbours(self, stone):
        '''Return a list of the adjacent stones

        If no stones are adjacent will return an empty list.
        Doesn't care about the colour of the adjacent stones.
        '''
        x = stone.x
        y = stone.y
        potential_stones = [self.get_stone(x - 1, y),\
                           self.get_stone(x + 1, y),\
                           self.get_stone(x, y - 1),\
                           self.get_stone(x, y + 1)]
        #Don't return the Nones
        return [stone for stone in potential_stones if stone]

    def is_alive(self, *args):
        '''True iff the stone/s is/are alive

        Takes three possible types of arguments:
        1. A GoStone object
        2. A list of GoStone objects
        3. A pair of x,y co-ordinates specifying a GoStone object.
        '''
        if (len(args) == 1):
            if (isinstance(args[0], GoStone)):
                return self._is_alive(args[0])
            # else we have a list of stones.
            else:
                alive = True
                for stone in args[0]:
                    alive = alive and self._is_alive(stone)
                return alive
        # else we have an x and y parameter.
        else:
            stone = self.get_stone(args[0], args[1])
            return self._is_alive(args[0])

    def _is_alive(self, stone):
        '''True iff the stone is alive'''
        stone_group = self.get_group(stone)
        for a_stone in stone_group:
            if self._has_free_neighbour(a_stone):
                return True
        return False

    def _has_free_neighbour(self, stone):
        '''True iff the stone has an empty neighbouring spot'''
        x = stone.x
        y = stone.y
        potential_neighbours = []

        if (x > 0):
            potential_neighbours.append(self.get_stone(x - 1, y))
        if (x < (self.board_size - 1)):
            potential_neighbours.append(self.get_stone(x + 1, y))
        if (y > 0):
            potential_neighbours.append(self.get_stone(x, y - 1))
        if (y < (self.board_size - 1)):
            potential_neighbours.append(self.get_stone(x, y + 1))

        for neighbour in potential_neighbours:
            if (not neighbour):
                return True
        return False
