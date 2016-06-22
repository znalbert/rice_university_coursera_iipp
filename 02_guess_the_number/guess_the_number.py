import simplegui
import random

guess_range = 100
guess_count = 0
max_guesses = 7

# helper function to start and restart the game
def new_game():
    """
    Initializes game with secret number and resets the guess count
    """
    global secret_number, guess_range, guess_count, max_guesses
    guess_count = 0
    secret_number = random.randrange(0, guess_range)
    print "Ready? You have " + str(max_guesses) + " guesses to find a number between 0 and " + str(guess_range - 1) + ". Go!\n"

# define event handlers for control panel
def range100():
    """
    Sets the range of the game from [0, 100)
    """
    global guess_range, max_guesses
    guess_range = 100
    max_guesses = 7
    new_game()

def range1000():
    """
    Sets the range of the game from [0, 1000)
    """
    global guess_range, max_guesses
    guess_range = 1000
    max_guesses = 10
    new_game()

def input_guess(guess):
    """
    Prints the player's guess and converts it into an integer.
    """
    global secret_number, guess_count, max_guesses

    guess_count += 1
    remaining_guesses = max_guesses - guess_count

    print "Player guessed " + guess
    player_guess = int(guess)

    if player_guess == secret_number:
        print "Correct!\n"
        new_game()
    elif guess_count < max_guesses:
        print "You have " + str(remaining_guesses) + " guesses remaining."
        if player_guess > secret_number:
            print "Lower!\n"
        else:
            print "Higher!\n"
    else:
        print "Oh no! You've run out of guesses! The number was " + str(secret_number) + "!\n"
        new_game()

# create frame
f = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements
f.add_button("Range is 0 to 99", range100, 200)
f.add_button("Range is 0 to 999", range1000, 200)
f.add_input("Enter a Guess", input_guess, 100)

#start frame
f.start()

# call new_game
new_game()
