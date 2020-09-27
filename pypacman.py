#!/usr/bin/env python3
# Pygame template - skeleton for a new pygame project
import pygame
import random
import time
import math
import os


SCATTER = { "red": (1,1) ,
            "blue": (26,1),
            "yellow": (1,29),
            "pink": (26,29)
}

TIMERS = {
    "red": {
        "jail": 5,
        "scatter": 6,
        "chase": 15,
        "runaway": 10,
        "random": 10
    },
    "blue": {
        "jail": 5,
        "scatter": 8,
        "chase": 15,
        "runaway": 10,
        "random": 10
    },
    "yellow": {
        "jail": 5,
        "scatter": 10,
        "chase": 15,
        "runaway": 10,
        "random": 10
    },
    "pink": {
        "jail": 5,
        "scatter": 12,
        "chase": 15,
        "runaway": 10,
        "random": 10
    }    
}

MAP = [     [52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53, 52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53], 
            [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
            [50,  1, 34, 32, 32, 35,  1, 34, 32, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 32, 35,  1, 34, 32, 32, 35,  1, 51],
            [50,  1, 33,  0,  0, 33,  1, 33,  0,  0,  0, 33,  1, 33, 33,  1, 33,  0,  0,  0, 33,  1, 33,  0,  0, 33,  1, 51],
            [50,  1, 36, 32, 32, 37,  1, 36, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 37,  1, 36, 32, 32, 37,  1, 51],
            [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
            [50,  1, 34, 32, 32, 35,  1, 34, 35,  1, 34, 32, 32, 32, 32, 32, 32, 35,  1, 34, 35,  1, 34, 32, 32, 35,  1, 51],
            [50,  1, 36, 32, 32, 37,  1, 33, 33,  1, 36, 32, 32, 35, 34, 32, 32, 37,  1, 33, 33,  1, 36, 32, 32, 37,  1, 51],
            [50,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1, 51],
            [54, 49, 49, 49, 49, 57,  1, 33, 36, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 37, 33,  1, 56, 49, 49, 49, 49, 55],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 34, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 35, 33,  1, 51,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1, 56, 49, 49, 49, 49, 49, 49, 57,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
            [48, 48, 48, 48, 48, 58,  1, 36, 37,  1, 51,  0,  0,  0,  0,  0,  0, 50,  1, 36, 37,  1, 59, 48, 48, 48, 48, 48],
            [ 0,  0,  0,  0,  0,  0,  1,  1,  1,  1, 51,  0,  0,  0,  0,  0,  0, 50,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0],
            [49, 49, 49, 49, 49, 57,  1, 34, 35,  1, 51,  0,  0,  0,  0,  0,  0, 50,  1, 34, 35,  1, 56, 49, 49, 49, 49, 49],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1, 59, 48, 48, 48, 48, 48, 48, 58,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1, 34, 32, 32, 32, 32, 32, 32, 35,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
            [52, 48, 48, 48, 48, 58,  1, 36, 37,  1, 36, 32, 32, 35, 34, 32, 32, 37,  1, 36, 37,  1, 59, 48, 48, 48, 48, 53],
            [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
            [50,  1, 34, 32, 32, 35,  1, 34, 32, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 32, 35,  1, 34, 32, 32, 35,  1, 51],
            [50,  1, 36, 32, 35, 33,  1, 36, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 37,  1, 33, 34, 32, 37,  1, 51],
            [50,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1, 51],
            [54, 32, 35,  1, 33, 33,  1, 34, 35,  1, 34, 32, 32, 32, 32, 32, 32, 35,  1, 34, 35,  1, 33, 33,  1, 34, 32, 55],
            [52, 32, 37,  1, 36, 37,  1, 33, 33,  1, 36, 32, 32, 35, 34, 32, 32, 37,  1, 33, 33,  1, 36, 37,  1, 36, 32, 53],
            [50,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1, 51],
            [50,  1, 34, 32, 32, 32, 32, 37, 36, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 37, 36, 32, 32, 32, 32, 35,  1, 51], 
            [50,  1, 36, 32, 32, 32, 32, 32, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 32, 32, 32, 32, 32, 37,  1, 51], 
            [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 , 1 ,51], 
            [54, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 55], 
    ]

WIDTH = len(MAP[0])*24
HEIGHT = len(MAP)*24

FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def display_map():
    y_length = len(MAP)
    x_length = len(MAP[0])
    for y in range(y_length):
        for x in range(x_length):
            c=MAP[y][x]
            if c in walls:
                surface.blit(walls[c],(x*24,y*24))

def collided():
    collided = False
    for f in Ghosts:
        if f.x == pacman.x and f.y == pacman.y:
            collided = True
            break

    return collided


class Pacman(pygame.sprite.Sprite):
    "pacman management"
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y

        self.image = pacman_pic
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 +12 , self.y * 24 + 12)
        self.speed = 4
        self.status = "normal"


    def set_status(self, status):
        """
        pacman status: pacgum, dead, normal
        """
        self.status = status
    
    def get_status(self):
        return self.status

class Ghost(pygame.sprite.Sprite):

    moves = ["left","right","up","down"]
    opposite = ["right", "left", "down", "up" ]

    def __init__(self, x, y, color, mode):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.distances = dict()
        self.allowed_moves = []
        self.direction = ""
        self.speed = 4

        # for the timers
        self.start_time = time.time()
        self.mode_changed = False

        self.image = Ghost_pics[self.color]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 +12 , self.y * 24 + 12)

    # In chase or runaway modes, we calculate distance between ghost and pacman
    def distance_based_direction(self):
        x = self.x
        y = self.y
        self.distances = dict()

        if self.mode == "scatter":
            x_target = SCATTER[self.color][0]
            y_target = SCATTER[self.color][1]
        else:
            x_target = pacman.x
            y_target = pacman.y

        # We calculate for each possible moves
        for direction in self.allowed_moves:
            x = self.x
            y = self.y
            if direction == "up":
                y = self.y - 1
            elif direction == "down":
                y = self.y + 1
            elif direction == "left":
                x = self.x - 1
            else:
                # right
                x = self.x + 1
            
            # Pythagore, of course
            dist_x = abs(x - x_target)
            dist_y = abs(y - y_target)
#            distance = round(math.sqrt(dist_x*dist_x + dist_y*dist_y))
            distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)
            self.distances[direction] = distance

        if self.mode == "chase" or self.mode == "scatter":
            min = 99999999999
        elif self.mode == "runaway":
            min = -1

        for key, value in self.distances.items():
            # In chase mode : select the nearest direction
            if self.mode == "chase" or self.mode == "scatter":
                if value < min:
                    min = value
                    self.direction = key
            # In run away mode: select the farthest direction
            elif self.mode == "runaway":
                if value > min:
                    min = value
                    self.direction = key

    # Direction is choosen in allowed directions
    def choose_direction(self):
        if self.mode == "random":
            self.direction=random.choice(self.allowed_moves)
        elif self.mode == "chase" or self.mode == "runaway" or self.mode == "scatter":
            self.distance_based_direction()

    # Checks the free positions around the ghost
    def get_allowed_moves(self):
        self.allowed_moves = self.moves.copy()

        # test if int = float
        if MAP[self.y][self.x-1] >= 16:
            self.allowed_moves.remove("left")
        if self.x+1 < 28 and MAP[self.y][self.x+1] >= 16:
            self.allowed_moves.remove("right")
        if MAP[self.y - 1][self.x] >= 16:
            self.allowed_moves.remove("up")
        if MAP[self.y + 1][self.x] >= 16:
            self.allowed_moves.remove("down")

        # By default : no turn back
        if not self.mode_changed:
            if self.direction != "":
                reverse=self.opposite[self.moves.index(self.direction)]
                if reverse in self.allowed_moves:
                    self.allowed_moves.remove(reverse)

    # Check time spent in current mode then change it based on a timer
    def change_mode(self):
        mode_time = TIMERS[self.color][self.mode]
        current_time = time.time()
        if current_time - self.start_time > mode_time:
            if self.mode == "scatter":
                self.mode = "chase"
            self.start_time = current_time
            self.mode_changed = True
        else:
            self.mode_changed = False

    # main function
    def update(self):

        # change mode based on timer
        self.change_mode()

        # Choose a direction only when we're on a MAP coordinates or chase mode changed
        if self.mode_changed or (self.rect.x % 24 == 0 and self.rect.y % 24 ==0):
            self.x = int(self.rect.x / 24)
            self.y = int(self.rect.y / 24)

            # What are the allowed moves ?
            self.get_allowed_moves()

            # choose a direction, based on the ghost mode
            self.choose_direction()

        # Direction is set : move the ghost
        if self.direction == "left":
            self.rect.x -= self.speed
            # go to right border
            if self.rect.x < 0:
                self.rect.x = WIDTH-12

        if self.direction == "right":
            self.rect.x += self.speed
            # go to left border
            if self.rect.x > WIDTH-12:
                self.rect.x = 0

        if self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = HEIGHT-12

        if self.direction == "down":
            self.rect.y += self.speed
            if self.rect.y > HEIGHT-12:
                self.rect.y = 0

        # For debug
        #print("color=",self.color, "x=",self.rect.x,"y=",self.rect.y, "mode=",self.mode, "f.direction=", self.direction, "allowed_moves=",self.allowed_moves, "distances=",self.distances)

# Root code
def main():
    global pacman_pic
    global pacman
    global screen
    global Ghost_pics
    global Ghosts
    global walls
    global surface

    scale = 1

    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()
    display_infos = pygame.display.Info()

    x_resolution = display_infos.current_w
    y_resolution = display_infos.current_h

    if y_resolution < 800:
        scale = 1.5

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman by Slyce")
    

    # create a surface to work on
    surface = pygame.Surface((int(WIDTH/scale), int(HEIGHT/scale)))

    clock = pygame.time.Clock()

    # load ghost pictures
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    Ghost_pics = dict()
    Ghost_pics['red'] = pygame.image.load(os.path.join(img_folder, 'red_up_ghost_1.png')).convert()
    Ghost_pics['yellow'] = pygame.image.load(os.path.join(img_folder, 'yellow_up_ghost_1.png')).convert()
    Ghost_pics['blue'] = pygame.image.load(os.path.join(img_folder, 'blue_up_ghost_1.png')).convert()
    Ghost_pics['pink'] = pygame.image.load(os.path.join(img_folder, 'pink_up_ghost_1.png')).convert()

    # load pacman picture
    pacman_pic = pygame.image.load(os.path.join(img_folder, 'pacman_right_1.png')).convert()

    # load walls based on values in MAP and if associated png exists
    walls = dict()
    for l in MAP:
        for c in l:
            if c not in walls:
                png = os.path.join(img_folder, str(c) + ".png")
                if(os.path.exists(png)):
                    walls[c] = pygame.image.load(png).convert()

    # declare sprites
    all_sprites = pygame.sprite.Group()

    Ghosts = []
    # declare the four ghosts
    Ghosts.append(Ghost(12,11, "red", "scatter"))
    Ghosts.append(Ghost(13,11, "blue", "scatter"))
    Ghosts.append(Ghost(14,11,"yellow","scatter"))
    Ghosts.append(Ghost(15,11,"pink","scatter"))

    # declare pacman
    pacman = Pacman(14, 17)

    all_sprites.add(pacman)
    all_sprites.add(Ghosts)

    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()
        surface.fill(BLACK)

        # Draw / render
        # draw walls
        display_map()

        #all_sprites.draw(screen)
        all_sprites.draw(surface)

        # Scale ?
        if scale > 1:
            frame = pygame.transform.scale(surface, (int(WIDTH/scale), int(HEIGHT/scale)))
        else:
            frame = surface
        # Surface on screen
        screen.blit(frame, (0, 0))

        # *after* drawing everything, flip the display
        pygame.display.flip()

        if collided():
            running = False

    pygame.quit()

if __name__ == "__main__":
    # execute only if run as a script
    main()
