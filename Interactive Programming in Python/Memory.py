# implementation of card game - Memory

import simplegui
import random

# global constants
WIDTH = 800
HEIGHT = 100
IM_WIDTH = WIDTH // 16 # evenly spaced 16 cards
IM_HEIGHT = HEIGHT
HORIZONTAL_OFFSET = 8
VERTICAL_OFFSET = 32

# external images
ext_image = True

card_images = simplegui.load_image("")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")


# helper function to initialize globals
def new_game():
    global num_list, exposed, state, selected, moves
    
    # create a deck of cards
    num_list = range(0,8)
    num_list.extend(range(0,8))
    random.shuffle(num_list)
    
    # exposed and selected lists
    exposed = [False] * 16
    selected = [] # List of 2 lists. Index 0 = numb_list selected / Index 1 numb_list index
    
    # restart game state
    state = 0
    moves = 0    
    
# define event handlers
def mouseclick(pos):
    global exposed, state, selected, moves
    index = pos[0] // IM_WIDTH
    
    # game state logic
    if state == 0: # game start
        if exposed[index] == False:
            exposed[index] = True
            selected.append([num_list[index], index])
        state = 1
    elif state == 1: # single exposed unpaired card
        if exposed[index] == False:
            exposed[index] = True
            selected.append([num_list[index], index])
            moves += 1
            state = 2
    else: # end of a turn
        if exposed[index] == False:
            exposed[index] = True
            if (selected[1][0] != selected[0][0]):
                exposed[selected[0][1]] = exposed[selected[1][1]] = False
            selected = []
            selected.append([num_list[index], index])
            state = 1  
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(0,len(num_list)):
        if not ext_image:
            if exposed[i] == False:
                canvas.draw_polygon([[IM_WIDTH*i, 0], [IM_WIDTH*(i+1), 0], [IM_WIDTH*(i+1), IM_HEIGHT], [IM_WIDTH*i, IM_HEIGHT]], 5, "Red", "Green")
            else:
                canvas.draw_text(str(num_list[i]),[IM_WIDTH * i + HORIZONTAL_OFFSET, IM_HEIGHT - VERTICAL_OFFSET], 60, "White", "sans-serif")
        elif ext_image:
            if exposed[i] == False:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [(IM_WIDTH // 2) * (2 * i + 1), IM_HEIGHT //2], [IM_WIDTH, IM_HEIGHT])
            else:
                canvas.draw_text(str(num_list[i]),[IM_WIDTH * i + HORIZONTAL_OFFSET, IM_HEIGHT - VERTICAL_OFFSET], 60, "White", "sans-serif")
    label.set_text("Turns = " + str(moves))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()