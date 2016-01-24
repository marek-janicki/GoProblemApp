from go_stone import GoStone

def GoBoard:
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

    def remove_stone(self, stone):
        '''Removes this stone from the Go Board

        Does not remove the stone itself.
        XXX: Does not check if the stone is already removed.
             Could potentially be a source of bugs.
        '''
        self.remove_stone(stone.x, stone.y)

    def remove_stone(self, x, y):
        '''Removes the stone at x and y from the board.

        Does not check if there is a stone there. Perhaps should?
        '''
        self.board[x][y] = None

    def remove_stones(self, stones):
        '''Removes every stone in the list from the board.

        Assumes stones is a list of GoStones
        '''
        for stone in stones:
            self.remove_stone(stone)

    def get_group(self, x, y):
        '''Get a group centred at the stone at x,y
         
        Returns a list of GoStones
        '''
        stone = self.get_stone(x, y)
        if stone:
            return self.get_group(stone)
        return []

    def get_group(self, stone):
        '''Get a group centred at the given stone
         
        Returns a list of GoStones
        '''
        first_stone = self.get_stone(x, y)
        ret_list = []
        self._get_group(first_stone, ret_list)

        #now we unmark all the stones so that future calls don't break
        for stone in ret_list:
            stone.touched = False

        return ret_list

    def _get_group(self, stone, stone_list):
        '''Add stone to stoneList and recursively calls itself on it's neighbours.'''
        stone.touched = True
        stone_list.append(stone)

        for neighbour in self.get_neighbours(stone):
            if (neighbour.colour == stone.colour) and not neighbour.touched:
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

    def is_alive(self, stone):
        '''True iff the stone is alive'''
        stone_group = self.getGroup(stone)
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

    def is_alive(self, x, y):
        '''True iff the stone at x,y is alive'''
        stone = self.get_stone(x, y)
        if stone:
            return self.is_alive(stone)
        return False #I guess?

    def is_alive(self, stones):
        '''True iff the group of stones are alive

        Assumes stons is a list of GoStones that *is* a group
        '''
        first_stone = stones[0]
        return self.is_alive(first_stone)
