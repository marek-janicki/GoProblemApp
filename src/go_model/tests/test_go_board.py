import nose
import GoBoard
import random

class TestGoBoard:

    def setup(self):
        '''Create a board'''
        self.board = GoBoard()

    def teardown(self):
        '''Remove the board'''
        self.board = None

    def get_random_board_positions(self, n):
        '''Get an n element list of board positions.

           There may be duplicates.'''
        ret_list = []
        for i in range(n):
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            ret_list.append([x, y])
         return ret_list

    def add_stones_to_board(self, position_list, colour = True):
        for position in position_list:
            stone = GoStone(position[0], position[1], colour)
            self.board.add_stone(stone)

    def test_is_occupied(self):
        position_list = self.get_random_board_positions(10)
        self.add_stones_to_board(position_list)
        for position in position_list:
            assert self.board.is_occupied(position[0], position[1])

    def test_is_not_occupied(self):
        position_list = self.get_random_board_positions(10)
        for position in position_list:
            assert not self.board.is_occupied(position[0], position[1])

    def test_get_no_neighbours(self):
        position_list = self.get_random_board_positions(10)
        for position in position_list:
            stone = GoStone(position[0], position[1], colour)
            self.board.add_stone(stone)
            assert len(self.board.get_neighbours(stone)) == 0
            self.board.remove_stone(stone)

    def test_get_some_neighbours(self):
        pass

    def test_has_free_neighbour(self):
        position_list = self.get_random_board_positions(100)
        first_position = position_list[0]
        first_stone = GoStone(first_position[0], first_position[1], True)
        self.board.add_stone(first_stone)
        colour = True

        for i in range(1, len(position_list)):
            position = position_list[i]
            stone = GoStone(position[0], position[1], colour)
            self.board.add_stone(stone)
            # With only two stones on the board, must have a free neighbour.
            assert self._has_free_neighbour(stone)
            previous_position = position_list[i-1]
            # Remove the previous stone.
            self.board.remove_stone(previous_position[0], previous_position[1])
            # Whee!
            colour = not colour

    def test_has_no_free_neighbours(self):
        pass

    def test_get_group(self):
        pass

    def test_is_alive(self):
        pass

    def test_is_dead(self):
        pass
