# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
points = 0
attempts = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """ int -> Time formatted string """
    tenths = str(t % 10)
    seconds = (t / 10) % 60
    if (t / 10) % 60 < 10:
        seconds = str(0) + str(seconds)
    else:
        seconds = str(seconds)
    minutes = t / 600
    return str(minutes) + ":" + str(seconds) + "." + str(tenths)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    t.start()

def stop():
    """Stops the timer and increments points and attempts as appropriate."""
    global time, points, attempts
    if t.is_running():
        if time % 10 == 0:
            points += 1
        attempts += 1
    t.stop()


def reset():
    """Stops timer and resets time, points, and attempts to 0"""
    global time, points, attempts
    time, points, attempts = 0, 0, 0
    t.stop()

# define event handler for timer with 0.1 sec interval
def time_handler():
    global time
    time += 1


# define draw handler
def draw_handler(canvas):
    global time
    canvas.draw_text(format(time), (95, 165), 50, 'White')
    canvas.draw_text(str(points) + "/" + str(attempts), (250, 50), 24, 'Red')


# create frame
f = simplegui.create_frame("Stopwatch: The Game", 300, 300)
t = simplegui.create_timer(100, time_handler)

# register event handlers
f.set_draw_handler(draw_handler)
start_button = f.add_button("Start", start, 100)
stop_button = f.add_button("Stop", stop, 100)
reset_button = f.add_button("Reset", reset, 100)

# start frame
f.start()
