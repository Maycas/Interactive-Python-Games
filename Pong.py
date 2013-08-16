# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if right == True:
        # ball movement to the upward right direction
        ball_vel = [random.randrange(120, 240)/60,  -random.randrange(60, 180)/60]
    else:
        # ball movement to the upward left direction
        ball_vel = [-random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
        
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    ball_init(random.choice([True,False]))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    # paddle1
    if paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT < 0:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT > HEIGHT -1:          	
        paddle1_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
    
    #paddle2    
    if paddle2_pos + paddle2_vel- HALF_PAD_HEIGHT < 0:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT > HEIGHT -1:          	
        paddle2_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "Red")
    c.draw_line([WIDTH - 1 - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - 1 - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "Blue")
     
    # update ball  
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collision with the top and bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # collision with gutters
    # left gutter
    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH): 
        if ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT):
            # ball between the height of paddle1 => reflect + increase ball velocity (10%)
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            # ball not inside the gutter => reset game and player 2 scores
            ball_init(True)
            score2 +=1
    # right gutter
    elif ball_pos[0] >= ((WIDTH - 1) - PAD_WIDTH - BALL_RADIUS):
        if ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT):
            # ball between the height of paddle2 => reflect + increase ball velocity (10%)
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            # ball not inside the gutter => reset game and player 1 scores
            ball_init(False)
            score1 +=1
           
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1),[WIDTH/4,100],50,"Red");
    c.draw_text(str(score2),[WIDTH * (3/4) - 1,100],50,"Blue");
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    # local handler variable to adjust velocities in the real game experience
    modulus = 5
    # player 1
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel -= modulus
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel += modulus
    else:
        paddle1_vel = 0  
    # player 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= modulus
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += modulus
    else:
        paddle2_vel = 0
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    # player 1
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    # player 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("PONG", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
frame.start()
new_game()


