# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
high = 100
low = 0
computer_guess = random.randrange(low, high)
remaining = math.ceil(math.log(high - low + 1, 2))

# helper function to initialize the game
def init():
    global f
    global remaining
    f.start()
    print "New Game. Range is from", low, "to", high
    print "Number of remaining guesses is:", remaining, "\n"

# helper function to restart the game once lost or won
def restart(high):
    # the game must be restarted once won
    # game selection depends on the current value of variable high
    if high == 100:
        range100()
    else:
        range1000()

# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100) and restarts
    # resets the number limits from 0 to 100
    # sets remaining according to 2 ** remaining >= high - low + 1
    global computer_guess
    global low
    global high
    global remaining
    low = 0
    high = 100
    remaining = math.ceil(math.log(high - low + 1, 2))
    print "New Game. Range is from", low, "to", high
    print "Number of remaining guesses is:", remaining, "\n"
    computer_guess = random.randrange(low, high)

def range1000():
    # button that changes range to range [0,1000) and restarts
    # resets the number limits from 0 to 1000
    # sets remaining according to 2 ** remaining >= high - low + 1
    global computer_guess
    global low
    global high
    global remaining
    low = 0
    high = 1000
    remaining = math.ceil(math.log(high - low + 1, 2))
    print "New Game. Range is from", low, "to", high
    print "Number of remaining guesses is:", remaining, "\n"
    computer_guess = random.randrange(low, high)
    
def get_input(guess):
    # main game logic goes here
    # retrieves the guess from the input and compares it with computer_guess
    global computer_guess
    global remaining
    global high
    global low
    guess = float(guess)
    remaining = remaining - 1
    print "Guess was", guess
    print "Number of remaining guesses is:", remaining
    if guess == computer_guess and remaining >= 0:
        print "Correct! \n"
        restart (high)
    elif guess < computer_guess and remaining != 0:
        print "Higher! \n"
    elif guess > computer_guess and remaining != 0:
        print "Lower! \n"
    else:
        print "You ran out of guesses. The number was", computer_guess, "\n"
        restart (high)
    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", get_input, 200)

# start frame
init()

# always remember to check your completed program against the grading rubric