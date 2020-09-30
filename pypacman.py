#!/usr/bin/env python3
"""
A single pacman game designed as a proof of concept:
- to learn python
- to understand ghosts algorithms
"""

import random
import time
import math
import os
import pygame

SCATTER = { "red": (1,1) ,
            "blue": (26,1),
            "yellow": (1,29),
            "pink": (26,29)
}

PACMAN_TIMERS = {
    "normal": 999999999,
    "chase": 8
}
GHOST_TIMERS = {
    "red": {
        "jail": 2,
        "scatter": 10,
        "chase": 15,
        "random": 10
    },
    "blue": {
        "jail": 3,
        "scatter": 8,
        "chase": 15,
        "random": 10
    },
    "yellow": {
        "jail": 5,
        "scatter": 10,
        "chase": 15,
        "random": 10
    },
    "pink": {
        "jail": 6,
        "scatter": 12,
        "chase": 15,
        "random": 10
    }
}

MAP = [
        [52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53, 52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53],
        [50,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2, 51],
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
        [ 0,  0,  0,  0,  0, 50,  1, 33, 33,  1, 56, 49, 49, 17, 17, 49, 49, 57,  1, 33, 33,  1, 51,  0,  0,  0,  0,  0],
        [48, 48, 48, 48, 48, 58,  1, 36, 37,  1, 51, 64,  0,  0,  0,  0, 64, 50,  1, 36, 37,  1, 59, 48, 48, 48, 48, 48],
        [ 0,  0,  0,  0,  0,  0,  1,  1,  1,  1, 51, 64,  0,  0,  0,  0, 64, 50,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0],
        [49, 49, 49, 49, 49, 57,  1, 34, 35,  1, 51, 64,  0,  0,  0,  0, 64, 50,  1, 34, 35,  1, 56, 49, 49, 49, 49, 49],
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
        [50,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 , 2 ,51],
        [54, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 55]
]

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
class Pacman(pygame.sprite.Sprite):
    """
    Pacman management class
    """

    def __init__(self, my_game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = my_game
        self.x = None
        self.y = None
        self.speed = None
        self.mode = None
        self.mode_changed = None
        self.direction = None
        self.image = None
        self.allowed_moves = None
        self.count_moves = None
        self.start_time = None

        self.reinit(x, y)

    def reinit(self, x, y):
        """
        Reinit pacman parameters
        """
        self.x = x
        self.y = y

        self.image = self.game.Pacman_pics['left'][1]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 + 12, self.y * 24 + 12)
        self.speed = 4
        self.direction = ""
        self.mode = "normal"
        self.allowed_moves = []
        self.count_moves = 0

        # for the timers
        self.start_time = time.time()
        self.mode_changed = False

        # for collisions
        self.radius = 6

    # Check what moves are allowed from this position
    def get_allowed_moves(self):
        """
        Check if pacman is allowed to move here
        """
        self.allowed_moves = []

        # check walls
        if MAP[self.y][self.x-1] < 16:
            self.allowed_moves.append("left")
        if (self.x+1 < 28 and MAP[self.y][self.x+1] < 16) or (self.x == 27 and self.direction == "right"):
            self.allowed_moves.append("right")
        if MAP[self.y - 1][self.x] < 16:
            self.allowed_moves.append("up")
        if MAP[self.y + 1][self.x] < 16:
            self.allowed_moves.append("down")

    # Do we ate something ? Remove it from map, increment score, and could be mega pacgum
    def check_pacgums(self):
        """
        Are we eating something ?
        """
        chase = False
        # Single pacgum : 10
        if MAP[self.y][self.x] == 1:
            self.game.score = self.game.score + 10
            MAP[self.y][self.x] = 0
            self.game.pacgums = self.game.pacgums - 1

        # Big pacgum : 50 It's time to chase !
        if MAP[self.y][self.x] == 2:
            self.game.score += 50
            MAP[self.y][self.x] = 0
            self.game.pacgums -= 1
            chase = True

        return chase

    def change_mode(self):
        """
        Two modes for pacman: chase or normal
        """
        self.mode_changed = False
        current_time = time.time()

        # Enter chase mode
        if self.check_pacgums():
            self.mode = "chase"
            self.start_time = current_time
            self.speed = 6
            self.mode_changed = True
            for ghost in self.game.Ghosts:
                ghost.change_mode("runaway")

        # rotate between modes based on timer
        else:
            mode_time = PACMAN_TIMERS[self.mode]
            if current_time - self.start_time > mode_time:
                if self.mode == "chase":
                    self.mode = "normal"
                    self.speed = 4
                self.start_time = current_time
                self.mode_changed = True

        #if self.mode_changed:
        #    print("Pacman mode changed to", self.mode)

    # move pacman
    def update(self):
        """
        used to move pacman in any direction
        """

        # Choose a direction only when we're on a MAP coordinates
        if self.rect.x % 24 == 0 and self.rect.y % 24 == 0:
            self.x = int(self.rect.x / 24)
            self.y = int(self.rect.y / 24)

            self.change_mode()

            self.get_allowed_moves()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                if MAP[self.y][self.x-1] < 16:
                    self.direction = "left"
            if keys[pygame.K_RIGHT]:
                if self.x+1 < 28 and MAP[self.y][self.x+1] < 16:
                    self.direction = "right"
            if keys[pygame.K_UP]:
                if MAP[self.y - 1][self.x] < 16:
                    self.direction = "up"
            if keys[pygame.K_DOWN]:
                if self.y + 1 < 30 and MAP[self.y + 1][self.x] < 16:
                    self.direction = "down"

        #print("Pacman: self.x=",self.x, "self.y=",self.y, "allowed_moves=",self.allowed_moves)
        # Direction is set : move the ghost
        moved = False

        if self.direction == "left" and "left" in self.allowed_moves:
            self.rect.x -= self.speed
            moved = True
            # go to right border
            if self.rect.x < 0:
                self.rect.x = self.game.WIDTH-24

        if self.direction == "right" and "right" in self.allowed_moves:
            self.rect.x += self.speed
            moved = True
            # go to left border
            if self.rect.x > self.game.WIDTH-24:
                self.rect.x = 0

        if self.direction == "up" and "up" in self.allowed_moves:
            self.rect.y -= self.speed
            moved = True
            if self.rect.y < 0:
                self.rect.y = self.game.HEIGHT-24

        if self.direction == "down" and "down" in self.allowed_moves:
            self.rect.y += self.speed
            moved = True
            if self.rect.y > self.game.HEIGHT-24:
                self.rect.y = 0

        if moved:
            self.count_moves += 1

        if self.direction:
            if moved:
                self.image = self.game.Pacman_pics[self.direction][self.count_moves % 3 + 1]
            else:
                self.image = self.game.Pacman_pics[self.direction][2]
            self.image.set_colorkey(BLACK)

class Ghost(pygame.sprite.Sprite):
    """
    Defines a ghost
    """
    moves = ["left", "right", "up", "down"]
    opposite = ["right", "left", "down", "up"]

    def __init__(self, my_game, x, y, color, mode):
        pygame.sprite.Sprite.__init__(self)

        self.game = my_game
        self.x = None
        self.y = None
        self.color = color
        self.mode = None
        self.old_mode = None
        self.distances = None
        self.allowed_moves = None
        self.forbid_turnback = None
        self.direction = None
        self.speed = None
        self.count_moves = None
        self.mode_changed = None
        self.start_time = None
        self.image = None

        self.reinit(x, y, mode)

    def reinit(self, x, y, mode):
        """
        reinit a ghost
        """
        self.x = x
        self.y = y

        self.mode = mode
        self.old_mode = ""
        self.distances = dict()
        self.allowed_moves = []
        self.forbid_turnback = True
        self.direction = ""
        self.speed = 4
        self.count_moves = 0

        # for collisions
        self.radius = 6

        # for the timers
        self.start_time = time.time()
        self.mode_changed = False

        self.image = self.game.Ghost_pics[self.color]['left'][1]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 + 12, self.y * 24 + 12)

    # In chase or runaway modes, we calculate distance between ghost and pacman
    def distance_based_direction(self):
        """
        calculate a direction based on the distance with pacman
        """
        x = self.x
        y = self.y
        self.distances = dict()

        # Previously in jail: target just outside jail to go outside
        if self.old_mode == "jail":
            x_target = 14
            y_target = 11
            # We're outside : go to normal coordinates
            if self.y <= 11:
                self.old_mode = ""

        elif self.mode == "scatter":
            x_target = SCATTER[self.color][0]
            y_target = SCATTER[self.color][1]
        else:
            x_target = self.game.pacman.x
            y_target = self.game.pacman.y

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
            distance = round(math.sqrt(dist_x * dist_x + dist_y * dist_y))
#            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            self.distances[direction] = distance

        if self.mode == "chase" or self.mode == "scatter":
            min_dist = 99999999999
        elif self.mode == "runaway":
            min_dist = -1

        for key, value in self.distances.items():
            # In chase mode : select the nearest direction
            if self.mode == "chase" or self.mode == "scatter":
                if value < min_dist:
                    min_dist = value
                    self.direction = key
            # In run away mode: select the farthest direction
            elif self.mode == "runaway":
                if value > min_dist:
                    min_dist = value
                    self.direction = key

    # Direction is choosen in allowed directions
    def choose_direction(self):
        """
        Based on current mode, make a choice of the movement algorithm
        """
        if self.mode == "random" or self.mode == "jail":
            self.direction = random.choice(self.allowed_moves)
        elif self.mode == "chase" or self.mode == "runaway" or self.mode == "scatter":
            self.distance_based_direction()

    # Checks the free positions around the ghost
    def get_allowed_moves(self):
        """
        based on current position, list all possible directions
        """
        self.allowed_moves = []

        # check walls
        if MAP[self.y][self.x-1] < 16:
            self.allowed_moves.append("left")
        if self.x+1 < 28 and MAP[self.y][self.x+1] < 16:
            self.allowed_moves.append("right")
        # if in jail, and no more in jail mode, we can go outside
        if MAP[self.y - 1][self.x] < 16 or (self.mode != "jail" and MAP[self.y - 1][self.x] == 17):
            self.allowed_moves.append("up")
        if MAP[self.y + 1][self.x] < 16:
            self.allowed_moves.append("down")

        # Remove opposition direction By default : no turn back
        if self.forbid_turnback and self.direction != '':
            reverse = self.opposite[self.moves.index(self.direction)]
            if reverse in self.allowed_moves:
                self.allowed_moves.remove(reverse)

    # Check time spent in current mode then change it based on a timer
    def change_mode(self, mode=False):
        """
        Change th current move mode, based on a timer or a given value
        """
        current_time = time.time()

        if mode == "runaway":
            # start time of runaway is aways the same as pacman in chase
            self.start_time = self.game.pacman.start_time
            self.old_mode = self.mode
            self.mode = "runaway"
            self.mode_changed = True
            #self.get_allowed_moves()
            #self.choose_direction()
        else:
            # rotate between modes
            mode_time = GHOST_TIMERS[self.color][self.mode]
            if current_time - self.start_time > mode_time:
                self.old_mode = self.mode
                if self.mode == "jail":
                    self.mode = "scatter"
                elif self.mode == "scatter":
                    self.mode = "chase"
                elif self.mode == "chase":
                    self.mode = "scatter"
                elif self.mode == "runaway":
                    self.mode = "jail"
                    GHOST_TIMERS[self.color]['jail'] = 0
                self.start_time = current_time
                self.mode_changed = True
            else:
                self.mode_changed = False

        if self.mode_changed:
            self.forbid_turnback = False
            #print(self.color, "mode changed to ", self.mode)

    # main function
    def update(self):
        """
        Update the ghost status and position
        main control
        """
        # change mode based on timer
        self.change_mode()

        # Choose a direction only when we're on a MAP coordinates
        if self.rect.x % 24 == 0 and self.rect.y % 24 == 0:
            self.x = int(self.rect.x / 24)
            self.y = int(self.rect.y / 24)

            # We moved one case
            self.count_moves += 1

            # What are the allowed moves ?
            self.get_allowed_moves()

            # choose a direction, based on the ghost mode
            self.choose_direction()

            # change mode alreay done, directino alreay set, we can forbid
            self.forbid_turnback = True

        # Direction is set : move the ghost
        if self.direction == "left":
            self.rect.x -= self.speed
            # go to right border
            if self.rect.x < 0:
                self.rect.x = self.game.WIDTH-12

        if self.direction == "right":
            self.rect.x += self.speed
            # go to left border
            if self.rect.x > self.game.WIDTH-12:
                self.rect.x = 0

        if self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = self.game.HEIGHT-12

        if self.direction == "down":
            self.rect.y += self.speed
            if self.rect.y > self.game.HEIGHT-12:
                self.rect.y = 0

        if self.mode == "runaway":
            current_time = time.time()
            if GHOST_TIMERS[self.color]['runaway'] - (current_time - self.start_time) < 3:
                self.image = self.game.Frightened_ghost_blinking[self.count_moves % 4 + 1]
            else:
                self.image = self.game.Frightened_ghost[self.count_moves % 2 + 1]
        else:
            self.image = self.game.Ghost_pics[self.color][self.direction][self.count_moves % 2 + 1]
        self.image.set_colorkey(BLACK)

        # For debug
        #print("color=",self.color, "map_x=",self.x, "map_y=",self.y,"x=",self.rect.x,"y=",self.rect.y, "old mode=",self.old_mode, "mode=",self.mode, "f.direction=", self.direction, "allowed_moves=",self.allowed_moves, "distances=",self.distances)


class Game:
    """
    Main class that manages the full game
    """
    def __init__(self):
        self.dymmy = None
        self.Pacman_pics = None
        self.Dead_pacman = None
        self.Ghost_pics = None
        self.Frightened_ghost = None
        self.Frightened_ghost_blinking = None
        self.Walls = None

        self.WIDTH = len(MAP[0])*24
        self.HEIGHT = len(MAP)*24

        self.FULL_WIDTH = self.WIDTH
        self.FULL_HEIGHT = self.HEIGHT + 64

        self.lifes = 3

        self.pacgums = self.count_pacgums()
        self.score = 0

        self.scale = 1
        self.FPS = 30 

        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()

        # Check vertical resolution
        display_infos = pygame.display.Info()
        y_resolution = display_infos.current_h

        if y_resolution < 800:
            self.scale = 0.75


        self.screen = pygame.display.set_mode((int(self.FULL_WIDTH * self.scale), int(self.FULL_HEIGHT * self.scale)))
        self.fake_screen = pygame.Surface((self.FULL_WIDTH, self.FULL_HEIGHT))
        pygame.display.set_caption("Pacman by Slyce")

        # create a surface to work on
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.top = pygame.Surface((self.WIDTH, 32))
        self.bottom = pygame.Surface((self.WIDTH, 32))

        # load bitmaps
        self.load_bitmaps()

        # declare sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_ghosts = pygame.sprite.Group()

        self.Ghosts = []
        # declare the four ghosts
        self.Ghosts.append(Ghost(self, 14, 14, "red", "jail"))
        self.Ghosts.append(Ghost(self, 13, 14, "blue", "jail"))
        self.Ghosts.append(Ghost(self, 13, 14, "yellow", "jail"))
        self.Ghosts.append(Ghost(self, 15, 14, "pink", "jail"))

        # Prepare runaway values
        for ghost in self.Ghosts:
            GHOST_TIMERS[ghost.color]['runaway'] = PACMAN_TIMERS['chase']

        # declare pacman
        self.pacman = Pacman(self, 14, 17)

        self.all_sprites.add(self.pacman)
        self.all_sprites.add(self.Ghosts)
        # for collisions
        self.all_ghosts.add(self.Ghosts)

    def load_bitmaps(self):
        """
        Load all bitmaps in use in the game
        """

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')

        # load ghost pictures
        self.Frightened_ghost = dict()
        self.Frightened_ghost[1] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_1.png')).convert()
        self.Frightened_ghost[2] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_2.png')).convert()

        # frightened and blinking
        self.Frightened_ghost_blinking = dict()
        self.Frightened_ghost_blinking[1] = self.Frightened_ghost[1]
        self.Frightened_ghost_blinking[2] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_3.png')).convert()
        self.Frightened_ghost_blinking[3] = self.Frightened_ghost[2]
        self.Frightened_ghost_blinking[4] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_4.png')).convert()

        # Standard ones
        self.Ghost_pics = dict()
        for color in ('red', 'yellow', 'blue', 'pink'):
            self.Ghost_pics[color] = dict()
            for direction in ('left', 'right', 'up', 'down'):
                self.Ghost_pics[color][direction] = dict()
                for i in range(1, 3):
                    self.Ghost_pics[color][direction][i] = pygame.image.load(os.path.join(img_folder, color+'_'+direction+'_ghost_'+str(i)+'.png')).convert()

        # load pacman pictures
        self.Pacman_pics = dict()
        for direction in ('left', 'right', 'up', 'down'):
            self.Pacman_pics[direction] = dict()
            for i in range(1, 4):
                self.Pacman_pics[direction][i] = pygame.image.load(os.path.join(img_folder, 'pacman_'+direction+'_'+str(i)+'.png')).convert()

        # dead pacman pictures
        self.Dead_pacman = dict()
        for i in range(1, 11):
            self.Dead_pacman[i] = pygame.image.load(os.path.join(img_folder, 'pacman_dead_'+str(i)+'.png')).convert()

        # load walls based on values in MAP and if associated png exists
        self.Walls = dict()
        for l in MAP:
            for c in l:
                if c not in self.Walls:
                    png = os.path.join(img_folder, str(c) + ".png")
                    if os.path.exists(png):
                        self.Walls[c] = pygame.image.load(png).convert()

    def display_board_game(self):
        """
        Display board game with map and sprites
        """
        # Draw all
        self.surface.fill(BLACK)
        self.top.fill(BLACK)
        self.bottom.fill(BLACK)

        # draw walls
        self.display_map(self.surface)

        # Draw sprites
        self.all_sprites.draw(self.surface)

        self.display_lifes(self.bottom)
        self.fake_screen.blit(self.top, (0, 0))
        self.fake_screen.blit(self.surface, (0, 32))
        self.fake_screen.blit(self.bottom, (0, self.HEIGHT+32))

    def display_text(self, my_surface, my_text):
        """
        TBD: display a text
        """
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(my_text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2))
        my_surface.blit(text, textRect)

    def display_lifes(self, my_surface):
        """
        Based on number of remaining lifes, display them
        """
        for life in range(0, self.lifes - 1):
            my_surface.blit(self.Pacman_pics['right'][2], (life*32+24, 4))

    def loose_life(self):
        """
        Display the dead pacman animation
        and reset everything
        """
        i = 1
        while i < 10:
            time.sleep(0.1)

            # evaluate the pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            # Draw all
            self.surface.fill(BLACK)
            self.top.fill(BLACK)
            self.bottom.fill(BLACK)

            # draw walls
            self.display_map(self.surface)

            # Animate the dead pacman
            self.surface.blit(self.Dead_pacman[i], (self.pacman.rect.x, self.pacman.rect.y))
            self.display_lifes(self.bottom)
            self.fake_screen.blit(self.top, (0, 0))
            self.fake_screen.blit(self.surface, (0, 32))
            self.fake_screen.blit(self.bottom, (0, self.HEIGHT+32))

            self.screen.blit(self.scale_output(self.fake_screen, self.scale), (0, 0))

            # *after* drawing everything, flip the display
            pygame.display.flip()
            i += 1

        # Reinit everything
        self.pacman.reinit(14, 17)
        for ghost in self.Ghosts:
            if ghost.color == "red":
                ghost.reinit(14, 14, "jail")
            if ghost.color == "blue":
                ghost.reinit(13, 14, "jail")
            if ghost.color == "yellow":
                ghost.reinit(13, 14, "jail")
            if ghost.color == "pink":
                ghost.reinit(15, 14, "jail")

    def scale_output(self, my_surface, my_scale):
        """
        Scale the suface given as parameter
        """
        # Scale ?
        if my_scale != 1:
            frame = pygame.transform.scale(my_surface, (int(self.FULL_WIDTH * my_scale), int(self.FULL_HEIGHT * my_scale)))
        else:
            frame = my_surface
        return frame

    # count number of pacgums in map
    def count_pacgums(self):
        """
        Count the total of pacgums in the map
        """
        y_length = len(MAP)
        x_length = len(MAP[0])
        self.pacgums = 0
        for y in range(y_length):
            for x in range(x_length):
                if MAP[y][x] in (1, 2):
                    self.pacgums += 1

        return self.pacgums

    def display_map(self, my_surface):
        """
        Display the map
        """
        y_length = len(MAP)
        x_length = len(MAP[0])
        for y in range(y_length):
            for x in range(x_length):
                c = MAP[y][x]
                if c in self.Walls:
                    my_surface.blit(self.Walls[c], (x*24, y*24))

    def collided(self):
        """
        Check for collisions
        """
        # See if the player block has collided with anything.
        hit_list = pygame.sprite.spritecollide(self.pacman, self.all_ghosts, False, pygame.sprite.collide_circle)

        return hit_list

    def play(self):
        """
        Main play function
        launch the game loop
        """
        clock = pygame.time.Clock()
        # Game loop
        running = True
        while running:

            # keep loop running at the right speed
            clock.tick(self.FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False

            self.pacman.update()
            self.all_ghosts.update()

            self.display_board_game()

            # Everything on screen
            self.screen.blit(self.scale_output(self.fake_screen, self.scale), (0, 0))

            # *after* drawing everything, flip the display
            pygame.display.flip()


            # Collision test
            hit_list = self.collided()
            if hit_list:
                if self.pacman.mode == "chase":
                    for ghost in hit_list:
                        if ghost.mode == "runaway":
                            ghost.x = 14
                            ghost.y = 15
                            ghost.rect.center = (ghost.x * 24 + 12, ghost.y * 24 + 12)
                            ghost.mode = "jail"
                            GHOST_TIMERS[ghost.color]['jail'] = random.randint(1, 10)
                            self.score += 200
                        else:
                            self.lifes -= 1
                            self.loose_life()
                else:
                    self.lifes -= 1
                    self.loose_life()

            # Won ?
            if self.pacgums == 0:
                running = False

            if self.lifes == 0:
                running = False


# Root code
def main():
    """
    main code to call the game
    """
    game = Game()

    # Play the game
    game.play()

    print("Remaining pacgums:", game.pacgums)
    print("Score:", game.score)

    pygame.quit()

if __name__ == "__main__":
    # execute only if run as a script
    main()
