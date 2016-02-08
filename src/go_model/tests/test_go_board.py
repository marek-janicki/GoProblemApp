import nose
from ..go_board import GoBoard
from ..go_stone import GoStone
import random

class TestGoBoard:

    def setup(self):
        '''Create a board'''
        self.board = GoBoard()

    def teardown(self):
        '''Remove the board'''
        self.board = None

    def set_test_board_positions(self):
        '''Get a list of positions that are always the same, used for fixed tests'''
        # Corner group that is dead.
        positions = [[0, 0], [0, 1], [1, 0]]
        self.add_stones_to_board(positions, True)
        positions = [[0, 2], [1, 1], [2, 0]]
        self.add_stones_to_board(positions, False)

        #Center group that is alive.
        positions = [[4, 4], [4, 5], [5, 5], [5, 4]]
        self.add_stones_to_board(positions, True)
        positions = [[3, 5], [4, 3], [4, 6], [5, 3], [5, 6], [6, 4], [6, 5]]
        self.add_stones_to_board(positions, False)


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
            stone = GoStone(position[0], position[1], True)
            self.board.add_stone(stone)
            assert len(self.board.get_neighbours(stone)) == 0
            self.board.remove_stone(stone)

    def test_get_some_neighbours(self):
        self.set_test_board_positions()
        neighbours = self.board.get_neighbours(self.board.get_stone(0, 0))
        neighbouring_stones = [GoStone(0, 1, True), GoStone(1, 0, True)]
        assert set(neighbours) == set(neighbouring_stones)

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
            assert self.board._has_free_neighbour(stone)
            previous_position = position_list[i-1]
            # Remove the previous stone.
            self.board.remove_stone(previous_position[0], previous_position[1])
            # Whee!
            colour = not colour

    def test_has_no_free_neighbours(self):
        self.set_test_board_positions()
        assert not self.board._has_free_neighbour(self.board.get_stone(0, 0))
        assert not self.board._has_free_neighbour(self.board.get_stone(0, 1))
        assert not self.board._has_free_neighbour(self.board.get_stone(5, 5))

    def test_get_group(self):
        self.set_test_board_positions()
        group = self.board.get_group(0, 0)
        actual_group = [GoStone(0, 0, True), GoStone(0, 1, True), GoStone(1, 0, True)]
        assert set(group) == set(actual_group)

    def test_is_alive(self):
        self.set_test_board_positions()
        live_group = self.board.get_group(5, 5)
        for stone in live_group:
            assert self.board.is_alive(stone)
        assert self.board.is_alive(live_group)

    def test_is_dead(self):
        self.set_test_board_positions()
        dead_group = self.board.get_group(0, 0)
        for stone in dead_group:
            assert not self.board.is_alive(stone)
        assert not self.board.is_alive(dead_group)
