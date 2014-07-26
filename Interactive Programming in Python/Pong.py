# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT /2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
DIFFICULTY = 0.1 # variable to increase game's difficulty when colliding a paddle (10%)

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initialize ball's position
    ball_pos = [HALF_WIDTH, HALF_HEIGHT]
    
    # initialize ball's velocity in the specified directions
    ball_vel = [random.randrange(120, 240)/60, random.randrange(60, 180)/60]
    if direction == LEFT:
        # upwards to the left
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = - ball_vel[1]
    elif direction == RIGHT:
        # upwards to the right
        # ball_vel[0] is positive, so there's no need to change its sign
        ball_vel[1] = - ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # spawn the ball in a new game 
    # it randomly decides if it launches to the left or to the right
    spawn_ball(random.choice([LEFT, RIGHT]))
    
    # restart the paddles in the middle of their gutters and with velocity 0
    paddle1_pos = paddle2_pos = HALF_HEIGHT
    paddle1_vel = paddle2_vel = 0
    
    # restart the scores when a new game starts
    score1 = score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # collision with top and bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT -1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # collision with gutters
    # right gutter
    if ball_pos[0] >= (WIDTH - 1) - PAD_WIDTH - BALL_RADIUS:
        # check if it collides in the range defined by the paddle
        if ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT):
            # ball between the height of paddle2 -> reflect + increase DIFFICULTY
            ball_vel[0] = - ball_vel[0] * (1 + DIFFICULTY)
            ball_vel[1] = ball_vel[1] * (1 + DIFFICULTY)
        else:
            # ball not inside the right paddle margin => reset game and player 1 scores
            score1 += 1
            spawn_ball(LEFT)
    # left gutter
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        # check if it collides in the range defined by the paddle
        if ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT):
            # ball between the height of paddle1 -> reflect + increase DIFFICULTY
            ball_vel[0] = - ball_vel[0] * (1 + DIFFICULTY)
            ball_vel[1] = ball_vel[1] * (1 + DIFFICULTY)
        else:
            # ball not inside the left paddle margin => reset game and player 2 scores
            score2 += 1
            spawn_ball(RIGHT)    
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # paddle 1 
    if paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT <= 0:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT >= HEIGHT -1:              
        paddle1_pos = (HEIGHT - 1) - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
    
    # paddle2    
    if paddle2_pos + paddle2_vel- HALF_PAD_HEIGHT <= 0:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT >= HEIGHT -1:              
        paddle2_pos = (HEIGHT - 1) - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "Red")
    canvas.draw_line([WIDTH - 1 - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - 1 - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "Blue")
    
    # draw scores
    canvas.draw_text(str(score1),[WIDTH/4.0 - PAD_WIDTH, 100], 50, "Red", "sans-serif");
    canvas.draw_text(str(score2),[(WIDTH - 1) * (3.0/4.0) - PAD_WIDTH, 100], 50, "Blue", "sans-serif");
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # local variable to adjust the paddle's velocity
    modulus = 5
    
    # player 1
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel -= modulus
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = modulus
      
    # player 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= modulus
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += modulus
   
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
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart Game", new_game)

# start frame
new_game()
frame.start()