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

# Required libraries
import random

# helper functions

def number_to_name(number):
    # fill in your code below
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if (number == 0):
        return 'rock'
    elif (number == 1):
        return 'Spock'
    elif (number == 2):
        return 'paper'
    elif (number == 3):
        return 'lizard'
    elif (number == 4):
        return 'scissors'
    else:
        return "Incorrect number. The number must be in the range between 0 to 4"

    
def name_to_number(name):
    # fill in your code below
    # convert name to number using if/elif/else
    # don't forget to return the result!
    if (name == 'rock'):
        return 0
    elif (name == 'Spock'):
        return 1
    elif (name == 'paper'):
        return 2
    elif (name == 'lizard'):
        return 3
    elif (name == 'scissors'):
        return 4
    else:
        return "Incorrect name. Please review the name spelling"


def rpsls(name): 
    # fill in your code below
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange() 
    comp_number = random.randrange(0,5)
    # As stated in the documentation, randrange computes a random number 
    # in the range 0 <= N < 5. So, in this example it will compute a number 
    # from 0 to 4, what expected

    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5

    # use if/elif/else to determine winner
    if (difference == 1) or (difference == 2):
        winner = 'Player'
    elif (difference == 3) or (difference == 4):
        winner = 'Computer'
    else:
        winner = 'Tie'

    # convert comp_number to name using number_to_name
    comp_name = number_to_name (comp_number)
    
    # print results
    print 'Player chooses', name
    print 'Computer chooses', comp_name
    if (winner != 'Tie'):
        print winner, 'wins!'
    else:
        print 'Player and computer tie!'
    print ''
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


