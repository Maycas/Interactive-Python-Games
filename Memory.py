# implementation of card game - Memory

import simplegui
import random

WIDTH = 800
HEIGHT = 100
IM_WIDTH = WIDTH // 16 #50
IM_HEIGHT = HEIGHT

# helper function to initialize globals
def init():
    global num_list, exposed, state, selected, moves
    num_list = range(0,8)
    num_list.extend(range(0,8))
    random.shuffle(num_list)
    exposed = [False]* 16
    selected = [] # list of 2 lists - index 0 number / index 1 num_list index
    state = 0
    moves = 0

    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, num_list, selected, moves
    i = pos[0] // IM_WIDTH 
    if state == 0: # game starts 
        selected.append([num_list[i], i])
        if (exposed[i] == False):
            exposed[i] = True
        state = 1
    elif state == 1: # single unpaired card exposed
        selected.append([num_list[i], i])
        if (exposed[i] == False):
            exposed[i] = True
            moves += 1
            label.set_text("Moves = " + str(moves))
            state = 2
        else:
            state = 1
    elif state == 2: # end of turn
        if (exposed[i] == False):
            exposed[i] = True
            if (selected[0][0] != selected [1][0]):
                exposed[selected[0][1]] = False
                exposed[selected[1][1]] = False
            selected = []
            selected.append([num_list[i],i])
            state = 1
        else:
            state = 2
            
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(0,len(num_list)):
        if (exposed[i] == False):
            canvas.draw_polygon([[IM_WIDTH*i, 0], [IM_WIDTH*(i+1), 0], [IM_WIDTH*(i+1), IM_HEIGHT], [IM_WIDTH*i, IM_HEIGHT]], 5, "Red", "Green")
        else:
            canvas.draw_text(str(num_list[i]),[IM_WIDTH*i+10, IM_HEIGHT-32], 60, "White")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

# Always remember to review the grading rubric