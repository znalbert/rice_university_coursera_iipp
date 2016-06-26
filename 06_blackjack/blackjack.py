# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        hand = ""
        for i in range(len(self.cards)):
            hand += self.cards[i].__str__() + " "
        return hand

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = []
        for c in self.cards:
            value.append(VALUES[c.get_rank()])
        if 1 in value:
            if sum(value) + 10 <= 21:
                return sum(value) + 10
            else:
                return sum(value)
        else:
            return sum(value)

    def draw(self, canvas, pos):
        for c in self.cards:
            c.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]

class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        deck = ""
        for i in range(len(self.cards)):
            deck += self.cards[i].__str__() + " "
        return deck

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, action
    if in_play:
        outcome = ""
        score -= 1
    in_play = True
    outcome = ""
    action = "Hit or stand?"
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

def hit():
    global outcome, in_play, deck, player_hand, score, action
    if in_play:
        player_hand.add_card(deck.deal_card())
        action = "Hit or stand?"
        outcome = "Player hits!"

        if player_hand.get_value() > 21:
            outcome = "Player busts!"
            action = "New deal?"
            score -= 1
            in_play = False

def stand():
    global outcome, in_play, deck, dealer_hand, player_hand, score, action
    if in_play:
        if dealer_hand.get_value() < 17:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busts!"
            action = "New deal?"
            score += 1
        elif dealer_hand.get_value() < player_hand.get_value():
            outcome = "Player wins!"
            action = "New deal?"
            score += 1
        else:
            outcome = "Dealer wins!"
            action = "New deal?"
            score -= 1
    in_play = False

# draw handler
def draw(canvas):
    global outcome, card_back

    hole = [100, 100]
    dealer_pos = [100, 100]
    player_pos = [100, 450]

    dealer_hand.draw(canvas, dealer_pos)
    player_hand.draw(canvas, player_pos)

    canvas.draw_text("Blackjack", [200, 60], 60, 'Yellow')
    canvas.draw_text(outcome, [200, 325], 46, 'Red')
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [hole[0] + CARD_CENTER[0], hole[1] + CARD_CENTER[1]], CARD_SIZE)
    canvas.draw_text("$: " + str(score), [550, 590], 20, 'White')
    canvas.draw_text(action, [20, 590], 20, 'White')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
