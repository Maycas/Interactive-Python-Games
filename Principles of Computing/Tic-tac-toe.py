"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10	# Number of trials to run
MCMATCH = 1.0  	# Score for squares played by the machine player
MCOTHER = 1.0  	# Score for squares played by the other player
    
def mc_trial(board, player):
    """
    Plays a game starting with the given player by making random 
    moves and alternating between players.
    """
    while board.check_win() == None:
        # Get a random empty square
        empty_squares = random.choice(board.get_empty_squares())
        
        # Move the player in a random position
        board.move(empty_squares[0], empty_squares[1], player)
        
        # Switch the player
        player = provided.switch_player(player)
        
    # Game has ended
    return


def mc_update_scores(scores, board, player):
    """
    Score the completed board and update the scores grid
    """
    # If the game is not a DRAW, update the scores list for each position in the board
    if board.check_win() != provided.DRAW: 
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                # Add the proper score depending on who's the winner
                if board.check_win() == board.square(row, col):
                    scores[row][col] += MCMATCH
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] -= MCOTHER

                       
def get_best_move(board, scores):
    """
    Finds all the empty squares with the maximum score and randomly
    returns one of them
    """
    # Get all the empty squares
    empty_squares = board.get_empty_squares()
    
    # Build a tuple list with the possible moves
    # List format: tuple with (score, pos(row, col))
    possible_moves = []
    for empty_square in empty_squares:
        possible_moves.append((scores[empty_square[0]][empty_square[1]], (empty_square[0], empty_square[1])))	    
    
    # Sort the list of possible moves to have the highest scores at the beginning
    possible_moves.sort(reverse=True)
    
    # Get best score and the first of all the available best moves
    best_score = possible_moves[0][0]
    best_moves = [(possible_moves[0][1][0], possible_moves[0][1][1])]
    
    # Get all the best_moves left
    for idx in range(1, len(possible_moves)):
        if possible_moves[idx][0] == best_score:
            best_moves.append((possible_moves[idx][1][0], possible_moves[idx][1][1]))
        else:
            break

    # Return a random move from the best_moves list    
    return random.choice(best_moves)
                

def mc_move(board, player, trials):
    """
    Use Monte Carlo simulation to return a move for the machine player
    in a (row, col) tuple
    """
    # Start with the current board.
    # Since it will be updated with the trial simulation, it is 
    # needed to clone it first
    current_board = board.clone()
    
    # Initialize the score grid to zeros
    scores = [[0 for dummy_col in range(current_board.get_dim())] for dummy_row in range(current_board.get_dim())]
    
    # For the desired number of trials
    for dummy_trial in range(trials):
        
        # Play entire game by randomly choosing a move for each player
        mc_trial(current_board, player)
        
        # Score the resulting board
        # Add scores to a running total across all trials
        mc_update_scores(scores, current_board, player)
        
        # Clone the board again for a new trial
        current_board = board.clone()
        
    # Select a move by randomly choosing one of the empty squares on the board that has the maximum score.
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)