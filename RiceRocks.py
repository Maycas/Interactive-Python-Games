# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_ROCKS = 12
RADIUS_FACTOR = 3
VEL_FACTOR = 1
score = 0
combo = 0
max_score = 0
max_combo = 0
lives = 3
time = 0.5
started = False
explosion_group = set()

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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 60)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# animated explosion from sprite animation lecture
EXPLOSION_DIM = [9, 9]
explosion_info_extra = ImageInfo([50, 50], [100, 100], 50, 74, True)
explosion_image_extra = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

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

# helper function to process a group of sprites: draw, update and remove them if their life has ended
def process_sprite_group(group_set, canvas):
    item_remove = set()
    for item in group_set:
        item.update()
        item.draw(canvas)
        if item.update():
            item_remove.add(item)
    group_set.difference_update(item_remove)

# helper function to check the number of collisions between an object and elements from a group
def group_collide(group, other_object):
    global explosion_group
    collisions = 0
    remove = set()
    for item in group:
        if item.collide(other_object):
            collisions += 1
            remove.add(item)
            # add animation to explosion
            an_explosion = Sprite(item.get_pos(), [0,0], 0, 0, explosion_image_extra, explosion_info_extra, explosion_sound)
            explosion_group.add(an_explosion)
            explosion_sound.play()
    group.difference_update(remove)
    return collisions

# helper function to detect collisions between groups and remove the objects from the sets if they collide
def group_group_collide(group1, group2):
    collisions = 0
    remove_group1 = set()
    for item_group1 in group1:
        if group_collide(group2, item_group1) != 0:
            collisions += 1
            remove_group1.add(item_group1)
    group1.difference_update(remove_group1)
    return collisions

# helper function to increase game difficulty
# if multiple of 500 points then increase the speed of rocks (2%)
# if multiple of 2000 points add a new rock
def increase_difficulty():
    global score, MAX_ROCKS, VEL_FACTOR
    if score % 500 == 0 and score != 0:
        VEL_FACTOR *= 1.02
    if score % 5000 == 0 and score != 0:
        MAX_ROCKS += 1

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
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, 
                              self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        # Update ship's position 
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Update ship's angle
        self.angle += self.angle_vel
        
        # Compute forward vector
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1
            
        # Friction update
        self.vel[0] *= 1 - 0.01
        self.vel[1] *= 1 - 0.01
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def increase_angle_vel(self):
        self.angle_vel += .05
    
    def decrease_angle_vel(self):
        self.angle_vel -= .05
    
    def set_thrusters(self, status):
        self.thrust = status
        if status:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)   
        missile_pos = [self.pos[0] + self.radius * forward[0], 
                       self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + forward[0] * 5, self.vel[1] + forward[1] * 5]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
                
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
   
    def draw(self, canvas):
        if self.animated:
            # adapted the code for the explosion image in the lecture about sprite animation
            index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(explosion_image_extra, [self.image_center[0] + index[0] * self.image_size[0], 
                     self.image_center[1] + index[1] * self.image_size[1]], 
                     self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, 
                              self.image_size, self.pos, self.image_size, self.angle)
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        # Update sprite's position 
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Update sprite's angle
        self.angle += self.angle_vel

        # Update age of sprite and comparison with its lifespan
        self.age += 1
        if self.age < self.lifespan:
            return False
        return True
    
    def collide(self, other_object):
        obj_distance = dist(self.get_pos(), other_object.get_pos())
        if obj_distance <= self.get_radius() + other_object.get_radius():
            # collision
            return True
        return False        
        
# key handlers
def key_down(key):
    if key == simplegui.KEY_MAP['right']:
        my_ship.increase_angle_vel()
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrease_angle_vel()
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrusters(True)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
      
def key_up(key):
    if key == simplegui.KEY_MAP['right']:
        my_ship.decrease_angle_vel()
    if key == simplegui.KEY_MAP['left']:
        my_ship.increase_angle_vel()
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrusters(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, VEL_FACTOR, MAX_ROCKS
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
    if lives == 0:
        lives = 3
        score = 0
        explosion_group = set()
        VEL_FACTOR = 1
        MAX_ROCKS = 12

# draw handler           
def draw(canvas):
    global time, lives, rock_group, score, started, explosion_group, combo, max_combo, max_score
    
    # animate background
    time += 1.0
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8.0) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2.0 + 1.25 * wtime, HEIGHT / 2.0], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2.0 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2.0], [2.5 * wtime, HEIGHT])
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    # process sprites
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # checks for collisions and updates labels
    # checks for collisions between my_ship and any rock in the rock_group
    if group_collide(rock_group, my_ship):
        lives -= 1
        if combo > max_combo:
            max_combo = combo
        combo = 0
        # end of game
        if lives == 0:
            if score > max_score:
                max_score = score
            started = False
            rock_group = set()
            soundtrack.pause()
            soundtrack.rewind()
            
    # checks for collisions between missiles and rocks
    if group_group_collide(rock_group, missile_group):
        score += 50
        combo += 1
        # update game difficulty
        increase_difficulty()   
    
    # draw feedback labels
    canvas.draw_text("Lives", [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("Score", [680, 50], 22, "White", "sans-serif")
    canvas.draw_text(str(lives), [50, 80], 22, "White", "sans-serif")
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")
    canvas.draw_text("Max Score: " + str(max_score), [50, 550], 22, "White", "sans-serif")
    canvas.draw_text("Max Combo: " + str(max_combo), [50, 580], 22, "White", "sans-serif")
    canvas.draw_text("Combo: " + str(combo), [680, 580], 22, "White", "sans-serif")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) < MAX_ROCKS and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        # check that a rock doesn't spawn too much close to the ship or the game would be frustrating
        # if it's too close the ship, keep calculating a new position
        while dist(rock_pos, my_ship.get_pos()) < RADIUS_FACTOR * my_ship.get_radius():
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        a_rock = Sprite(rock_pos, 
                    [random.random() * VEL_FACTOR * (-1) ** random.randrange(0, 10), random.random() * VEL_FACTOR * (-1) ** random.randrange(0, 10)], 
                    random.random() * 0.05 * (-1) ** random.randrange(0, 10), 
                    random.random() * 0.05 * (-1) ** random.randrange(0, 10), 
                    asteroid_image, asteroid_info)
        rock_group.add(a_rock)
    
# initialize frame
frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)

# initialize ship and two groups of sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
