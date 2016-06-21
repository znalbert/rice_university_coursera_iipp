# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def valid_choice(name):
    """str -> bool
    Checks to see if the player choice is valid.
    """
    return name in ["rock", "paper", "scissors", "lizard", "Spock"]

def name_to_number(name):
    """str -> int

    Takes a string of either rock, Spock, paper, lizard, or scissors,
    and converts it to a corresponding number ranging from 0 - 4.
    """
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    return number


def number_to_name(number):
    """int -> str

    Takes an integer ranging from 0 to 4 and converts it to the corresponding
    string of either rock, paper, scissors, lizard, or Spock.
    """
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    return name


def rpsls(player_choice):
    """str -> str

    Takes a string representing the player choice, randomly generates a computer
    choice, and prints out information about the choices and winner for the round.
    """

    # print out the message for the player's choice
    if valid_choice(player_choice):
        print "Player chooses " + player_choice
    else:
        print "Hold up there, hombre. Give a valid choice if you want to play.\n"
        return

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)

    # print out the message for computer's choice
    print "Computer chooses " + comp_choice

    # compute difference of comp_number and player_number modulo five
    winning_numb = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message
    if winning_numb == 0:
        print "Player and computer tie!\n"
    elif winning_numb == 1 or winning_numb == 2:
        print "Computer wins!\n"
    else:
        print "Player wins!\n"

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
