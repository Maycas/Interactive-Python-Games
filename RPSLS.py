# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# libraries required
import random

# helper functions

def name_to_number(name):
    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return 'Incorrect name. Please review the name spelling'

def number_to_name(number):
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        return 'rock'
    if number == 1:
        return 'Spock'
    if number == 2:
        return 'paper'
    if number == 3:
        return 'lizard'
    if number == 4:
        return 'scissors'
    else:
        return "Incorrect number. The number must be in the range between 0 to 4"
    

def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print ''
    
    # print out the message for the player's choice
    print 'Player chooses', player_choice

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print 'Computer chooses', comp_choice

    # compute difference of comp_number and player_number modulo five
    difference = (player_number - comp_number) % 5
    
    # use if/elif/else to determine winner, print winner message
    if difference == 1 or difference == 2:
        print 'Player wins!'
    elif difference == 3 or difference == 4:
        print 'Computer wins!'
    else:
        print 'Player and computer tie!'
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")