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
ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """
    Takes a string to indicate the direction of the ball, and then
    generates a random ball velocity for that direction.
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel[0] = random.randrange(120, 240) / 60.0
    ball_vel[1] = -random.randrange(60, 180) / 60.0
    if direction == "LEFT":
        ball_vel[0] *= -1
    ball_pos = [WIDTH / 2, HEIGHT / 2]

# define event handlers
def new_game():
    """
    Initilizes a new game
    """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = paddle2_pos = HEIGHT / 2
    paddle1_vel = paddle2_vel = 0
    score1 = score2 = 0
    direction = random.choice(["RIGHT", "LEFT"])
    spawn_ball(direction)

def draw(canvas):
    """
    Paints the game
    """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    pad1_top = [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]
    pad1_bottom = [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]
    pad2_top = [WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    pad2_bottom = [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Green")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Green")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Green")

    # update ball
    ball_pos[0] += ball_vel[0]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1.1
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Green", "Green")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + paddle1_vel > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel

    if paddle2_pos + paddle2_vel < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + paddle2_vel > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_line(pad1_top, pad1_bottom, PAD_WIDTH, "Green")
    canvas.draw_line(pad2_top, pad2_bottom, PAD_WIDTH, "Green")

    # determine whether paddle and ball collide
    if ball_pos[0] + ball_vel[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= pad1_top[1] and ball_pos[1] < pad1_bottom[1]:
            ball_vel[0] *= -1.1
        else:
            score2 += 1
            spawn_ball("RIGHT")
    elif ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= pad2_top[1] and ball_pos[1] < pad2_bottom[1]:
            ball_vel[0] *= -1.1
        else:
            score1 += 1
            spawn_ball("LEFT")

    # draw scores
    canvas.draw_text(str(score1), [150, 50], 24, "Green")
    canvas.draw_text(str(score2), [450, 50], 24, "Green")

def keydown(key):
    """
    Moves paddles vertically according to key input.
    """
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 6
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 6
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 6
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 6

def keyup(key):
    """
    Stops paddle movement when key is released.
    """
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"] or key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)

# start frame
new_game()
frame.start()
