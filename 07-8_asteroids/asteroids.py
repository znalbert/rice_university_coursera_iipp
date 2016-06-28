# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
W_H = [WIDTH, HEIGHT]
FRICTION = 0.015
ACCELERATION = .4
SPAWN_BUFFER = 100
punisher = 1
score = 0
lives = 3
time = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 90)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        for v in range(len(self.vel)):
            self.vel[v] *= (1 - FRICTION)
            self.pos[v] = (self.vel[v] + self.pos[v]) % W_H[v]
            if self.thrust == True:
                self.vel[v] += angle_to_vector(self.angle)[v] * ACCELERATION

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def decrement_angle_vel(self):
        self.angle_vel += -0.1

    def increment_angle_vel(self):
        self.angle_vel += 0.1
        
    def set_thrust(self, on):
        self.thrust = on
        if on:
            self.image_center[0] += self.image_size[0]
            ship_thrust_sound.play()
        else:
            self.image_center[0] -= self.image_size[0]
            ship_thrust_sound.rewind()
    
    def shoot(self):
        facing = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + (facing[0] * self.radius),
                       self.pos[1] + (facing[1] * self.radius)]
        missile_vel = [self.vel[0] + (facing[0] * 3), self.vel[1] + (facing[1] * 3)]
        missile_group.add(Sprite(missile_pos, missile_vel, 0, 0,
                           missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
            self.age += 1
    
    def update(self):
        self.angle += self.angle_vel
        self.age += 1
        for v in range(len(self.vel)):
            self.pos[v] = (self.vel[v] + self.pos[v]) % W_H[v]
        return self.age > self.lifespan
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius()

def key_down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def key_up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

def click(pos):
    global started, lives, score
    lives, score = 3, 0
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    soundtrack.play()
        
def draw(canvas):
    global time, started, lives, rock_group, missile_group, explosion_group, score, punisher
    
    if lives == 0:
        started = False
        rock_group = set([])
        missile_group = set([])
        explosion_group = set([])
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        my_ship.angle = 0
        punisher = 1
        soundtrack.rewind()
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    if started:
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        process_sprite_group(canvas, explosion_group)
        if group_collide(rock_group, my_ship):
            lives -= 1
        group_group_collide(rock_group, missile_group)
        my_ship.draw(canvas)
        my_ship.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global punisher, started
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    vel = [punisher * 2 * (random.random() - random.random()),
           punisher * 2 * (random.random() - random.random())]
    starting_angle = random.random() * 2 * math.pi
    ang_vel = (random.random() - random.random()) * 0.1
    if len(rock_group) < 12 and started:
        if dist(my_ship.get_position(), pos) > SPAWN_BUFFER:
            rock_group.add(Sprite(pos, vel, starting_angle, ang_vel,
                                  asteroid_image, asteroid_info))
        
def process_sprite_group(canvas, group):
    iterable_group = set(group)
    for element in iterable_group:
        element.draw(canvas)
        if element.update():
            group.remove(element)
            
    
def group_collide(group, other_object):
    global lives
    iterable_group = set(group)
    for element in iterable_group:
        if element.collide(other_object):
            explosion_group.add(Sprite(element.get_position(), [0, 0], 0, 0,
                                       explosion_image, explosion_info, explosion_sound))
            group.remove(element)
            return element.collide(other_object)
        
def group_group_collide(rocks, missiles):
    global score, punisher
    iterable_missiles = set(missiles)
    for missile in iterable_missiles:
        if group_collide(rocks, missile):
            missiles.discard(missile)
            score += 1
            punisher += 0.1
            
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()