"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 

def slide(end, start):
    """
    Helper function to slide all non-zero values to the 
    beginning of the list
    """
    index = 0
    for tile in start:
        if tile != 0:
            end[index] = tile
            index += 1
    return end

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # Create lists of zeros
    result = [0] * len(line) 
    added = [0] * len(line)
    
    # Put values in the next available entry in result
    result = slide(result, line)
    
    # Add values   
    for index in range(len(result) - 1):
        if result[index] == result[index + 1]:
            result[index] += result[index + 1]
            result[index + 1] = 0
        index += 1  
    result = slide(added, result)
               
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):               
        # Set grid dimensions
        self.grid_height = grid_height
        self.grid_width = grid_width
        
        # Reset the tiles values to 0
        self.tiles = self.reset()
        
        # Compute initial_tiles for moving in the grid
        dir_up = []
        dir_down = []
        dir_left = []
        dir_right = []
        for col in range(self.grid_width):
            dir_up.append((0, col))
            dir_down.append((self.grid_height - 1, col))    
        for row in range(self.grid_height):
            dir_left.append((row, 0))
            dir_right.append((row, self.grid_width - 1))         
        self.initial_tiles = {UP: dir_up,
                              DOWN: dir_down,
                              LEFT: dir_left,
                              RIGHT: dir_right }
                                           
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.tiles = [[0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
        return self.tiles
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.tiles)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        
        for initial_tile in self.initial_tiles[direction]:
            temp = []
            
            # Get the tiles 
            row = initial_tile[0]
            col = initial_tile[1]

            while 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                temp.append(self.get_tile(row,col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]

            # Merge the values
            temp = merge(temp)
            
            # Set the values
            row = initial_tile[0]
            col = initial_tile[1]
            index = 0
            while 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                if temp[index] != self.get_tile(row,col):
                    changed = True
                self.set_tile(row, col, temp[index])
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
                index += 1
            
        # Add new tile if required
        if changed:
            self.new_tile()
                    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Select the value of the tile
        new_tile_in_play = random.choice([2,2,2,2,2,2,2,2,4])
        
        # Search all the empty tiles available
        zero_pos_list = []
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.tiles[row][col] == 0:
                    zero_pos_list.append((row, col))
        
        # Select a random tile from the tuples list
        selected_zero_pos = random.choice(zero_pos_list)
        
        # Set the random value
        self.set_tile(selected_zero_pos[0], selected_zero_pos[1], new_tile_in_play)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.tiles[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.tiles[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(5, 6))