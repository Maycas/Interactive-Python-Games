"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        for dummy_i in range(target_row+1, self._height):
            for dummy_j in range(0, self._width):
                solved_value = (dummy_j + self._width * dummy_i)
                if self.get_number(dummy_i, dummy_j) != solved_value:
                    return False
        for dummy_j in range(target_col+1, self._width):
            solved_value = (dummy_j + self._width * target_row)
            if self.get_number(target_row, dummy_j) != solved_value:
                return False
        return True
    
    def down_path(self, col_diff, row_diff):
        """
        adjust the postion of 0 tile while switching from horizontal
        to vertical move by going from underneath meaning "dru" method
        """
        move = ""
        if col_diff > 0:
            move += "dru"
        else:
            move += "dlu"
        move += "lddru" * (row_diff - 1)
        move += "ld"
        return move
    
    def position_tile(self, temp_pos, tar_pos):
        """
        Reposition tile at temp_pos to tar_pos and the original tile at tar_pos
        will sit left to its original pos
        """
        row_diff = tar_pos[0] - temp_pos[0]
        col_diff = tar_pos[1] - temp_pos[1]
        # move 0 tile to temp_pos
        move = "u" * row_diff
        move += "l" * col_diff + "r" * (-col_diff)
        if col_diff != 0:
            # horizontal move to target_col
            if temp_pos[0] == 0:
                move += ("drrul" * (col_diff - 1)) + ("dllur" * ((-col_diff) - 1))
            else:
                move += ("urrdl" * (col_diff - 1)) + ("ulldr" * ((-col_diff) - 1))
            # adjust and then vertical move to target_row
            if temp_pos[0] == 0:
                move += self.down_path(col_diff, row_diff)
            elif row_diff == 1:
                if col_diff > 0:
                    move += "ur"
                else:
                    move += "ul"
                move += "lddru" * row_diff
                move += "ld"
            elif row_diff != 0:
                move += self.down_path(col_diff, row_diff)
            return move
        elif col_diff == 0 and row_diff == 1:
            move += "ld"
            return move
        else:
            move += "lddru" * (row_diff - 1)
            move += "ld"
            return move
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        temp_pos = self.current_position(target_row, target_col)
        move = self.position_tile(temp_pos, (target_row, target_col))
        self.update_puzzle(move)
        return move


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move = "ur"
        self.update_puzzle(move)
        if self.get_number(target_row, 0) == target_row * self._width:
            sub_move = "r" * (self._width - 2)
            self.update_puzzle(sub_move)
            move += sub_move
            return move
        else:
            temp_pos = self.current_position(target_row, 0)
            sub_move = self.position_tile(temp_pos, (target_row - 1, 1))
            sub_move += "ruldrdlurdluurddlur"
            sub_move += "r" * (self._width - 2)
            self.update_puzzle(sub_move)
            move += sub_move
            return move


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        for dummy_i in range(2, self._height):
            for dummy_j in range(0, self._width):
                solved_value = (dummy_j + self._width * dummy_i)
                if self.get_number(dummy_i, dummy_j) != solved_value:
                    return False
        for dummy_j in range(target_col, self._width):
            solved_value = (dummy_j + self._width * 1)
            if self.get_number(1, dummy_j) != solved_value:
                return False
        for dummy_j in range(target_col + 1, self._width):
            solved_value = (dummy_j + self._width * 0)
            if self.get_number(0, dummy_j) != solved_value:
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move = "ld"
        self.update_puzzle(move)
        if self.get_number(0, target_col) == target_col:
            return move
        else:
            temp_pos = self.current_position(0, target_col)
            sub_move = self.position_tile(temp_pos, (1, target_col-1))
            sub_move += "urdlurrdluldrruld"
            self.update_puzzle(sub_move)
            move += sub_move
        return move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        temp_pos = self.current_position(1, target_col)
        move = self.position_tile(temp_pos, (1, target_col))
        move += "ur"
        self.update_puzzle(move)
        return move

    ###########################################################
    # Phase 3 methods
    def check_2x2(self):
        """
        Helper method that check if 2x2 is a winning board
        """
        for dummy_i in range(0,2):
            for dummy_j in range(0,2):
                solved_value = (dummy_j + self._width * dummy_i)
                if self.get_number(dummy_i, dummy_j) != solved_value:
                    return False
        return True

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move = "ul"
        self.update_puzzle(move)
        for dummy_i in range(1,5):
            move = "rdlu"
            self.update_puzzle(move)
            if self.check_2x2():
                return "ul" + move * dummy_i
        for dummy_i in range(1,5):
            move = "drul"
            self.update_puzzle(move)
            if self.check_2x2():
                return "ul" + move * dummy_i
            
    def init_solver(self):
        """
        move 0 tile to rightmost corner
        and return the move string
        """
        for dummy_i in range(0, self._height):
            for dummy_j in range(0, self._width):
                if self.get_number(dummy_i, dummy_j) == 0:
                    otile_pos = (dummy_i, dummy_j)
        move = ""
        row, col = otile_pos[0], otile_pos[1]
        row_diff = self._height - row - 1
        col_diff = self._width - col - 1
        move += "d" * row_diff + "r" * col_diff
        self.update_puzzle(move)
        return move
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move = self.init_solver()
        for dummy_i in range(self._height-1, 1, -1):
            for dummy_j in range(self._width-1, 0, -1):
                assert self.lower_row_invariant(dummy_i, dummy_j)
                move += self.solve_interior_tile(dummy_i, dummy_j)
                assert self.lower_row_invariant(dummy_i, dummy_j-1)
            assert self.lower_row_invariant(dummy_i, 0)
            move += self.solve_col0_tile(dummy_i)
            assert self.lower_row_invariant(dummy_i-1,self._width-1)
        for dummy_j in range(self._width-1, 1, -1):
            move += self.solve_row1_tile(dummy_j)
            move += self.solve_row0_tile(dummy_j)
        move += self.solve_2x2()
        return move

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]]))
# poc_fifteen_gui.FifteenGUI(Puzzle(5, 5))