"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)    
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        distance_field = [[poc_grid.Grid.get_grid_height(self) * poc_grid.Grid.get_grid_width(self) 
                           for dummy_col in range(poc_grid.Grid.get_grid_width(self))] 
                          for dummy_row in range(poc_grid.Grid.get_grid_height(self))]
            
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
        elif entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        else:
            print "Invalid entity"
        
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        # Breadth-first search algorithm
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if poc_grid.Grid.is_empty(self, neighbor[0], neighbor[1]):
                    if visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)
                        if distance_field[current_cell[0]][current_cell[1]] + 1 < distance_field[neighbor[0]][neighbor[1]]:
                            distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                
        return distance_field   
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in self.humans():
            max_distance = float("-inf")
            moves = []
            
            # find the maximum distance in all the possible moves for a human
            possible_moves = poc_grid.Grid.eight_neighbors(self, human[0], human[1])
            for possible_move in possible_moves:
                if zombie_distance[possible_move[0]][possible_move[1]] > max_distance:
                    max_distance = zombie_distance[possible_move[0]][possible_move[1]]
            
            # get the list of possible moves that match to max_distance
            for possible_move in possible_moves:
                if zombie_distance[possible_move[0]][possible_move[1]] == max_distance:
                    moves.append(possible_move)
            
            # randomly choose and update the move
            self._human_list[self._human_list.index(human)] = random.choice(moves)     
                       
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            min_distance = float("inf")
            moves = []
            
            # find the minimum distance in all the possible moves for a zombie
            possible_moves = poc_grid.Grid.four_neighbors(self, zombie[0], zombie[1])
            for possible_move in possible_moves:
                if human_distance[possible_move[0]][possible_move[1]] < min_distance:
                    min_distance = human_distance[possible_move[0]][possible_move[1]]
            
            # get the list of possible moves that match to min_distance
            for possible_move in possible_moves:
                if human_distance[possible_move[0]][possible_move[1]] == min_distance:
                    moves.append(possible_move)
            
            # randomly choose and update the move
            self._zombie_list[self._zombie_list.index(zombie)] = random.choice(moves)


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Zombie(30, 40))


#import user35_EPZOWWGoUeaEemm as test
#test.phase1_test(Zombie)
#test.phase2_test(Zombie)
#test.phase3_test(Zombie)
