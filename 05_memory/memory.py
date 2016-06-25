# implementation of card game - Memory

import simplegui
import random

CARDS = range(8) + range(8)
for i in range(len(CARDS)):
    CARDS[i] = [CARDS[i], False]
state = 0
turns = 0
revealed_1, revealed_2 = None, None

# helper function to initialize globals
def new_game():
    """
    Initializes game variables and shuffles the cards.
    """
    global revealed_1, revealed_2, turns, state
    revealed_1, revealed_2, turns, state = None, None, 0, 0
    for card in CARDS:
        card[1] = False
    random.shuffle(CARDS)
    label.set_text("Turns = " + str(turns))

# define event handlers
def mouseclick(pos):
    """
    Click handler to reveal cards.
    """
    global state, revealed_1, revealed_2, turns
    clicked_card = pos[0] // 50
    if CARDS[clicked_card][1] == False:
        CARDS[clicked_card][1] = True
        if state == 0:
            state = 1
            revealed_1 = clicked_card
            turns += 1
            label.set_text("Turns = " + str(turns))
        elif state == 1:
            state = 2
            revealed_2 = clicked_card
        else:
            state = 1
            if CARDS[revealed_1] != CARDS[revealed_2]:
                CARDS[revealed_1][1], CARDS[revealed_2][1] = False, False
            revealed_1, revealed_2 = clicked_card, None
            turns += 1
            label.set_text("Turns = " + str(turns))

# cards are logically 50x100 pixels in size
def draw(canvas):
    """
    Draws the games play area, and the cards that users will be clicking.
    """
    x = 10
    for card in CARDS:
        canvas.draw_text(str(card[0]), (x, 75), 64, 'Red')
        if card[1] == False:
            canvas.draw_line((x + 15, 2), (x + 15, 98), 48, 'Green')
        x += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
