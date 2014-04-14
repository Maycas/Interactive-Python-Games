# "Stopwatch: The Game"

# import libraries
import simplegui

# define global variables
tenths = 0 # tenths of second
x = 0 # successful stops
y = 0 # total stops
timer_runs = False # global boolean to keep track on the timer status

game_status = ["Right on!", "Shame on you!", "None"]
status = None

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # Prints a number on the format A:BC.D given by integer t
    D = t % 10
    C = t // 10 % 10
    B = t // 100 % 6
    A = (t // 10) // 60
    # if A surpasses the value 9 (minutes), the game won't stop
    # minutes will keep increasing until the player finishes or restarts
    return str(A) + ":" + str(B) + str(C) + "." + str(D)

# handler to give feedback to the player
def print_message(canvas, status):
    if status == game_status[0]:
        canvas.draw_text(status, (90, 225), 30, "Green")
    elif status == game_status[1]:
        canvas.draw_text(status, (60, 225), 30, "Red")
    else:
        canvas.draw_text("", (100, 200), 20, "Green")        

# define event handlers for buttons; "Start", "Stop", "Reset"
# start handler
def start():
    global timer_runs, status
    timer.start()
    timer_runs = True
    status = game_status[2]

# stop handler
def stop():
    global tenths, timer_runs, x, y
    global status
    timer.stop()
    if tenths != 0 and tenths % 10 == 0 and timer_runs == True:
        x += 1
        y += 1
        status = game_status[0]
    elif timer_runs == True:
        y += 1
        status = game_status[1]
    timer_runs = False
        
# reset handler
def reset():
    global tenths, x, y, timer_runs
    timer.stop()
    tenths = 0
    x = 0
    y = 0
    timer_runs = False

# define event handler for timer with 0.1 sec interval
def tick():
    global tenths
    tenths += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(tenths), (80, 150), 48, "white")
    canvas.draw_text(str(x) + "/" + str(y), (230, 40), 38, "Yellow")
    print_message(canvas, status) 
    
# create frame and timer
frame = simplegui.create_frame("StopWatch: The game", 300, 250)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Reset", reset, 150)

# start frame
frame.start()