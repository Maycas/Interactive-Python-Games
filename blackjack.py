# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
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
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []
        
    def __str__(self):
        # return a string representation of a hand
        string = ""
        for i in range(len(self.cards)):
            string += str(self.cards[i]) + " "
        return "Hand contains " + string
        
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        aces = 0
        for card in self.cards:
            if card.get_rank() == 'A':
                aces +=1
            self.value += VALUES.get(card.get_rank())                   
        if aces == 0:
            return self.value
        elif self.value + 10 <= 21:
            return self.value + 10
        else:
            return self.value
           
    def draw(self, canvas, pos):       
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas, [pos[0] + i * CARD_SIZE[0] * 1.05, pos[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.decklist = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card (suit, rank)
                self.decklist.append(str(card.get_suit()) + str(card.get_rank()))

    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        random.shuffle(self.decklist)

    def deal_card(self):
        # deal a card object from the deck
        last_card = self.decklist.pop()
        card = Card (last_card[0], last_card[1])
        return card
    
    def __str__(self):
        # return a string representing the deck
        deck = ""
        for i in range(len(self.decklist)):
            deck += str(self.decklist[i]) + " "
        return "Deck contains " + deck

#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, dealer, player
    if in_play:
        outcome = "You dealt and lost. Hit or Stand?"
        score -=1
        in_play = False
    else:
        outcome = "Hit or Stand?"
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True
    
    # test print statements to track the values in the console
    # print deck
    # print "Player: " + str(player), player.get_value()
    # print "Dealer: " + str(dealer), dealer.get_value()
    
def hit(): 
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global player, outcome, in_play, score
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        # print "Player: " + str(player), player.get_value()
        if player.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            score -= 1
       
def stand():   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global player, dealer, outcome, in_play, score
    if player.get_value() > 21:
        outcome = "You have busted. New deal?"
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            # print "Dealer: " + str(dealer), dealer.get_value()
        if dealer.get_value() > 21:
            # print "Dealer: " + str(dealer), dealer.get_value()
            outcome = "Dealer has busted. You win! New deal?"
            score += 1
        elif player.get_value() <= dealer.get_value():
            outcome = "Dealer wins... New deal?"
            score -= 1
        else:
            outcome = "You win! New deal?"
            score += 1
    in_play = False
                
# draw handler    
def draw(canvas):
    # draw player and dealer's hand
    dealer.draw(canvas, [100, 100])
    player.draw(canvas, [100, 400])
    
    # draw labels
    canvas.draw_text("BLACKJACK", (350, 50), 40, "Black", "serif")
    canvas.draw_text(outcome, (75, 350), 32, "Yellow", "serif")
    canvas.draw_text("Score: " + str(score), (500, 75), 20, "Yellow")
    canvas.draw_text("Dealer", (10, 100), 30, "Red", "serif")
    canvas.draw_text("Player", (10, 400), 30, "Red", "serif")
    
    # draw card back
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]], CARD_SIZE)
    
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()

# initialize game
deck = Deck()
player = Hand()
dealer = Hand()
deal()
score = 0
in_play = True


# remember to review the gradic rubric