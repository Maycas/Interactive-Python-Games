# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
low = 0
high = 100

# helper function to start and restart the game
def new_game():
    # set (or resets) the number, the remaining guesses
    # and starts (or restarts) a new game
    global number, remaining
    number = random.randrange(low, high)
    remaining = int(math.ceil(math.log(high - low + 1, 2)))
    
    # show game status
    print "New game. Range is from", low, "to", high
    print "Number of remaining guesses is", remaining, "\n"

# helper function to check if the guess is between ranges
def check_guess(guess):
    if guess >= low and guess < high:
        return "Correct"
    else:
        return "Incorrect"
    
# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) 
    # and restarts the remaining guesses and the game
    global high, remaining
    high = 100
    remaining = int(math.ceil(math.log(high - low + 1, 2)))
    new_game()    

def range1000():
    # button that changes range to range [0,1000) 
    # # and restarts the remaining guesses and the game
    global high, remaining
    high = 1000
    remaining = int(math.ceil(math.log(high - low + 1, 2)))
    new_game()
        
def input_guess(guess):
    # main game logic goes here
    global number, remaining
    
    # check if the introduced guess is correct
    if check_guess(int(guess)) == "Incorrect":
        print guess, "is not in the valid range"
        print "Please introduce a number between", low, "and", high, "\n"
        return
    
    # decrease the number of remaining guesses
    remaining -= 1
    
    # show game status
    print "Guess was", guess
    print "Number of remaining guesses is", remaining
    
    # compare the introduced input, show appropiate message
    # and restart the game if it has ended
    if int(guess) < number and remaining > 0:
        print "Higher!\n"
    elif int(guess) > number and remaining > 0:
        print "Lower!\n"
    elif int(guess) == number and remaining >=0:
        print "Correct!", "\n\n"
        new_game()
    else:
        print "You ran out of guesses. The number was", number, "\n\n"
        new_game()
        
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_input("Enter your guess", input_guess, 200)
frame.add_button("Range 0 - 100", range100, 200)
frame.add_button("Range 0 - 1000", range1000, 200)

# call new_game and start frame
new_game()
frame.start()