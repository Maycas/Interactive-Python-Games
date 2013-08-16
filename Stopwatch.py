# template for "Stopwatch: The Game"

# import libraries
import simplegui

# define global variables
seconds = 0.1
tenths = 0
x = 0 #successful stops variable
y = 0 #total stops variable
timer_runs = False

# define helper function to convert seconds to miliseconds
def sec_2_milisec(seconds):
    miliseconds = int(seconds * 1000)
    return miliseconds

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
    
# define event handlers for buttons; "Start", "Stop", "Reset"
# start button handler
def start():
    global timer_runs
    timer_runs = True
    timer.start()

# stop button handler
def stop():
    global x
    global y
    global tenths
    global timer_runs
    timer.stop()
    if tenths != 0 and tenths % 10 == 0 and timer_runs == True:
        x += 1
        y += 1
    elif timer_runs == True:
        y += 1
    timer_runs = False

# restart button handler
def restart():
    global tenths
    global x
    global y
    global timer_runs
    timer.stop()
    tenths = 0
    x = 0
    y = 0
    timer_runs = False

# define event handler for timer with 0.1 sec interval
def tick():
    global tenths
    tenths +=1
    
# define draw handler
def draw_handler(canvas):
    global tenths
    global x
    global y
    canvas.draw_text(format(tenths), (100, 100), 48, "White")
    canvas.draw_text(str(x) + "/" + str(y), (230, 40), 38, "Green")
    
# create frame
frame = simplegui.create_frame("StopWatch: The Game", 300, 150)

# register event handlers
timer = simplegui.create_timer(sec_2_milisec(seconds), tick)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Restart", restart, 150)

# start frame
frame.start()

# Please remember to review the grading rubric
