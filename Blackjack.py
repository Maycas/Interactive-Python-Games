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
see_hand_values = False # variable to track the hand values in a numerical way 

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
        self.hand_list = []

    def __str__(self):
        # return a string representation of a hand
        string = ""
        for i in range(len(self.hand_list)):
            string += str(self.hand_list[i]) + " "
        return "Hand contains " + string

    def add_card(self, card):
        # add a card object to a hand
        self.hand_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        aces = 0
        
        # get and add all the values and count the aces as 1
        for card in self.hand_list:
            if card.get_rank() == "A":
                aces += 1
            self.value += VALUES[card.get_rank()]
        
        # depending on the aces, add 10 if it doesn't bust 
        if aces > 0 and self.value + 10 <= 21:
            return self.value + 10
        else:
            return self.value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand_list)):
            self.hand_list[i].draw(canvas, [pos[0] + i * CARD_SIZE[0] * 1.05, pos[1]])
         
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card (suit, rank)
                self.deck_list.append(card.get_suit() + card.get_rank())

    def __str__(self):
        # return a string representing the deck
        deck = ""
        for i in range(len(self.deck_list)):
            deck += str(self.deck_list[i]) + " "
        return "Deck contains " + deck
            
    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck_list)

    def deal_card(self):
        # deal a card object from the deck
        last_card = self.deck_list.pop()
        card = Card(last_card[0], last_card[1])
        return card

#define a helper for viewing the score
def show_hand_values(canvas):
    if see_hand_values:
        canvas.draw_text(str(dealer.get_value()), (150, 100), 18, "Black", "sans-serif")
        canvas.draw_text(str(player.get_value()), (150, 400), 18, "Black", "sans-serif")

#define helper for activating the help or not        
def set_help():
    global see_hand_values
    see_hand_values = not see_hand_values
    return see_hand_values
        
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score 
    
    # check if a game is in play or has finished when clicking 
    # the deal button. If so, the player loses
    if in_play:
        outcome = "You dealt and lost. Hit or Stand?"
        score -= 1
        in_play = False
    else:
        outcome = "Hit or Stand?"
    
    # create and shuffle a new deck
    deck = Deck()
    deck.shuffle()
    
    # create a player hand and add 2 cards
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    # create a dealer hand and add 2 cards
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    # TEST
    #print "Deck status: ", str(deck)
    #print "Player: ", str(player), player.get_value()
    #print "Dealer: ", str(dealer), dealer.get_value()
    
    # update the game status
    in_play = True

def hit():
    global player, outcome, in_play, score
    
    # if the hand is in play, hit the player   
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        
        # TEST
        #print "Player: " + str(player), player.get_value()
        
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = "You have busted. New deal?"
            score -= 1
            in_play = False
            
            # TEST
            #print outcome, "\n"
       
def stand():
    global player, dealer, outcome, in_play, score 

    # if the player has busted, remind him
    if player.get_value() > 21:
        outcome = "You have busted. New deal?"

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        
        # check the value of the dealer's hand and update the game outcome
        if dealer.get_value() > 21:
            outcome = "Dealer has busted. You win! New deal?"
            score += 1
        elif player.get_value() <= dealer.get_value():
            outcome = "Dealer wins... New deal?"
            score -= 1
        else:
            outcome = "You win! New deal?"
            score += 1
        
        # TEST
        #print "Dealer: " + str(dealer), dealer.get_value()       
        #print outcome, "\n"
              
    in_play = False
    
# draw handler    
def draw(canvas):
    # draw player and dealer's hand
    dealer.draw(canvas, [100, 110])
    player.draw(canvas, [100, 410])
    
    # draw labels
    canvas.draw_text("BLACKJACK", (350, 50), 40, "Black", "sans-serif")
    canvas.draw_text(outcome, (75, 350), 28, "Yellow", "sans-serif")
    canvas.draw_text("Score: " + str(score), (510, 75), 20, "Yellow", "sans-serif")
    canvas.draw_text("Dealer", (10, 100), 30, "Red", "sans-serif")
    canvas.draw_text("Player", (10, 400), 30, "Red", "sans-serif")
    
    # draw hand values if the player has requested for help
    show_hand_values(canvas)
    
    # draw card back
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 110 + CARD_BACK_CENTER[1]], CARD_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Help - Show me the values", set_help, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
