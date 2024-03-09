#!/usr/bin/env python3
"""
A single pacman game designed as a proof of concept:
- to learn python
- to understand ghosts algorithms
"""

import sys
import random
import time
import math
import os
import pygame
import argparse

LEVELS = {}

LEVELS[1] = {
    'MODES': (
        ['scatter', 7 ],
        [ 'chase', 20 ],
        [ 'scatter', 7 ],
        [ 'chase', 20 ],
        [ 'scatter', 7 ],
        [ 'chase', 20 ],
        [ 'scatter', 5 ],
        [ 'chase', 9999999 ]
    ),
    'red_dots_remaining': 20,
    'bonus': 'cherry'
}
"""
LEVELS[2] = [
    ['scatter', 7 ],
    [ 'chase', 20 ],
    [ 'scatter', 7 ],
    [ 'chase', 20 ],
    [ 'scatter', 5 ],
    [ 'chase', 1033.14 ],
    [ 'scatter', 0.01 ],
    [ 'chase', 9999999 ]
]

LEVELS[3] = LEVELS[2]
LEVELS[4] = LEVELS[2]

LEVELS[5] = [
    ['scatter', 5 ],
    [ 'chase', 20 ],
    [ 'scatter', 5 ],
    [ 'chase', 20 ],
    [ 'scatter', 5 ],
    [ 'chase', 1037.14 ],
    [ 'scatter', 0.01 ],
    [ 'chase', 9999999 ]
]

LEVELS[6] = LEVELS[5]
"""

FRUITS = {  "cherry": {  'id': 7, "score": 100 },
            "strawberry": {  'id': 8, "score": 300 },
            "orange": {  'id': 9, "score": 500 },
            "apple": {  'id': 10, "score": 700 },
            "melon": {  'id': 11, "score": 1000 },
            "galboss": {  'id': 12, "score": 2000 },
            "bell": {  'id': 13, "score": 3000 },
            "key": {  'id': 14, "score": 5000 }
}

SCATTER = { "red": (26,1) ,
            "blue": (26,29),
            "yellow": (1,29),
            "pink": (1,1)
}

JAIL = { "red": (12,14) ,
         "blue": (13,14),
         "yellow": (15,14),
         "pink": (14,14)
}


PACMAN_TIMERS = {
    "normal": 999999999,
    "chase": 6
}

PACMAN_POS = (13, 23)

FORBIDDEN_UP = [
    (12, 10),
    (15, 10),
    (12, 22),
    (15, 22)
]

# 28 (0-27) x 31 (0-30)
# 1 is path with pacgum
# 0 is clear path
# 2 is big pacgum
MAP = [
        [52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53, 52, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 53],
        [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
        [50,  2, 34, 32, 32, 35,  1, 34, 32, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 32, 35,  1, 34, 32, 32, 35,  1, 51],
        [50,  1, 33,  0,  0, 33,  1, 33,  0,  0,  0, 33,  1, 33, 33,  1, 33,  0,  0,  0, 33,  1, 33,  0,  0, 33,  2, 51],
        [50,  1, 36, 32, 32, 37,  1, 36, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 37,  1, 36, 32, 32, 37,  1, 51],
        [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
        [50,  1, 34, 32, 32, 35,  1, 34, 35,  1, 34, 32, 32, 32, 32, 32, 32, 35,  1, 34, 35,  1, 34, 32, 32, 35,  1, 51],
        [50,  1, 36, 32, 32, 37,  1, 33, 33,  1, 36, 32, 32, 35, 34, 32, 32, 37,  1, 33, 33,  1, 36, 32, 32, 37,  1, 51],
        [50,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1, 51],
        [54, 49, 49, 49, 49, 57,  1, 33, 36, 32, 32, 35,  0, 33, 33,  0, 34, 32, 32, 37, 33,  1, 56, 49, 49, 49, 49, 55],
        [16, 16, 16, 16, 16, 50,  1, 33, 34, 32, 32, 37,  0, 36, 37,  0, 36, 32, 32, 35, 33,  1, 51, 16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16, 50,  1, 33, 33,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 33, 33,  1, 51, 16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16, 50,  1, 33, 33,  0, 56, 49, 49, 17, 17, 49, 49, 57,  0, 33, 33,  1, 51, 16, 16, 16, 16, 16],
        [48, 48, 48, 48, 48, 58,  1, 36, 37,  0, 51, 64, 64,  0,  0, 64, 64, 50,  0, 36, 37,  1, 59, 48, 48, 48, 48, 48],
        [15, 15, 15, 15, 15, 15,  1,  0,  0,  0, 51, 64,  0,  0,  0,  0, 64, 50,  0,  0,  0,  1, 15, 15, 15, 15, 15, 15],
        [49, 49, 49, 49, 49, 57,  1, 34, 35,  0, 51, 64, 64, 64, 64, 64, 64, 50,  0, 34, 35,  1, 56, 49, 49, 49, 49, 49],
        [16, 16, 16, 16, 16, 50,  1, 33, 33,  0, 59, 48, 48, 48, 48, 48, 48, 58,  0, 33, 33,  1, 51, 16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16, 50,  1, 33, 33,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 33, 33,  1, 51, 16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16, 50,  1, 33, 33,  0, 34, 32, 32, 32, 32, 32, 32, 35,  0, 33, 33,  1, 51, 16, 16, 16, 16, 16],
        [52, 48, 48, 48, 48, 58,  1, 36, 37,  0, 36, 32, 32, 35, 34, 32, 32, 37,  0, 36, 37,  1, 59, 48, 48, 48, 48, 53],
        [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 51],
        [50,  1, 34, 32, 32, 35,  1, 34, 32, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 32, 35,  1, 34, 32, 32, 35,  1, 51],
        [50,  1, 36, 32, 35, 33,  1, 36, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 37,  1, 33, 34, 32, 37,  1, 51],
        [50,  2,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1,  1,  0,  0,  1,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  2, 51],
        [54, 32, 35,  1, 33, 33,  1, 34, 35,  1, 34, 32, 32, 32, 32, 32, 32, 35,  1, 34, 35,  1, 33, 33,  1, 34, 32, 55],
        [52, 32, 37,  1, 36, 37,  1, 33, 33,  1, 36, 32, 32, 35, 34, 32, 32, 37,  1, 33, 33,  1, 36, 37,  1, 36, 32, 53],
        [50,  1,  1,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1, 33, 33,  1,  1,  1,  1,  1,  1, 51],
        [50,  1, 34, 32, 32, 32, 32, 37, 36, 32, 32, 35,  1, 33, 33,  1, 34, 32, 32, 37, 36, 32, 32, 32, 32, 35,  1, 51],
        [50,  1, 36, 32, 32, 32, 32, 32, 32, 32, 32, 37,  1, 36, 37,  1, 36, 32, 32, 32, 32, 32, 32, 32, 32, 37,  1, 51],
        [50,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 , 1 ,51],
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
        self.real_x = None
        self.real_y = None
        self.speed = None
        self.mode = None
        self.mode_changed = None
        self.direction = None
        self.image = None
        self.allowed_moves = None
        self.count_moves = None
        self.start_time = None
        self.miss_loops = None
        self.set_bonus = None
        self.reinit(x, y)

    def reinit(self, x, y):
        """
        Reinit pacman parameters
        """
        self.x = x
        self.y = y

        self.image = self.game.Pacman_pics['left'][1]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 + 12, self.y * 24 + 12)
        self.real_x = self.x * 24 * 10
        self.real_y = self.y * 24 * 10
        self.speed = 55
        self.direction = "left"
        self.mode = "normal"
        self.allowed_moves = []
        self.count_moves = 0
        self.miss_loops = 0
        # for the timers
        self.start_time = time.time()
        self.mode_changed = False

        # for collisions
        self.radius = 3

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
            # play sound
            pygame.mixer.Sound.play(self.game.munch[self.game.pacgums%2 + 1])

            self.game.score += 10
            MAP[self.y][self.x] = 0
            self.game.pacgums -= 1
            self.miss_loops = 5

        # Big pacgum : 50 It's time to chase !
        if MAP[self.y][self.x] == 2:
            # play sound
            pygame.mixer.Sound.play(self.game.snd_power_pellet,2)
            self.game.score += 50
            MAP[self.y][self.x] = 0
            self.game.pacgums -= 1
            self.miss_loops = 15
            chase = True

        # Removed fruits for simplicity
        # Bonus !
        if MAP[self.y][self.x] >= 7 and MAP[self.y][self.x] <= 14:
            self.game.score += FRUITS[LEVELS[self.game.level]['bonus']]['score']
            MAP[self.y][self.x] = 0
            self.game.eat_bonus(LEVELS[self.game.level]['bonus'])

        # Bonus management !
        # First bonus at 170 remainings
        # Second bonus at 70 remainings
        if self.game.pacgums in (70,170) and self.set_bonus != self.game.pacgums:
            self.set_bonus = self.game.pacgums
            MAP[17][13] = FRUITS[LEVELS[self.game.level]['bonus']]['id']

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
            self.mode_changed = True
            for ghost in self.game.Ghosts:
                if ghost.mode != "eaten":
                    ghost.change_mode("runaway")

        # rotate between modes based on timer
        else:
            mode_time = PACMAN_TIMERS[self.mode]
            if current_time - self.start_time > mode_time:
                if self.mode == "chase":
                    # Reinit ghosts in a row counter
                    self.game.ghosts_in_a_row = 0
                    self.mode = "normal"
                self.start_time = current_time
                self.mode_changed = True

        if self.mode_changed:
            print("Pacman mode changed to", self.mode)

    # move pacman
    def update(self):
        """
        used to move pacman in any direction
        """
        current_speed = self.speed
        if self.miss_loops:
            current_speed -= self.miss_loops
            self.miss_loops = 0

        # if the next move exceeds the next case
        if self.direction == 'left' and self.real_x-current_speed < (self.x-1)*24*10:
            next_speed = self.real_x - (self.x-1)*240
        elif self.direction == 'right' and self.real_x+current_speed > (self.x+1)*24*10:
            next_speed = (self.x+1)*240  - self.real_x
        elif self.direction == 'up' and self.real_y-current_speed < (self.y-1)*24*10:
            next_speed = self.real_y - (self.y-1)*240
        elif self.direction == 'down' and self.real_y+current_speed > (self.y+1)*24*10:
            next_speed = (self.y+1)*240 - self.real_y
        else:
            next_speed = current_speed

        moved = False
        next_loops = (next_speed, current_speed-next_speed)
        for speed in next_loops:
            if speed == 0:
                continue

            # Choose a direction only when we're on a MAP coordinates
            if (self.real_x /10) % 24 == 0 and (self.real_y/10) % 24 == 0:

                self.x = int(self.real_x / 10 / 24)
                self.y = int(self.real_y / 10 / 24)

                self.change_mode()

                self.get_allowed_moves()

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    if MAP[self.y][self.x-1] < 16:
                        self.direction = "left"
                elif keys[pygame.K_RIGHT]:
                    if self.x+1 < 28 and MAP[self.y][self.x+1] < 16:
                        self.direction = "right"
                elif keys[pygame.K_UP]:
                    if MAP[self.y - 1][self.x] < 16:
                        self.direction = "up"
                elif keys[pygame.K_DOWN]:
                    if self.y + 1 < 30 and MAP[self.y + 1][self.x] < 16:
                        self.direction = "down"

            #print('Pacman, direction=', self.real_x, self.real_y, self.x, self.y,  self.direction, 'Original speed=', self.speed, 'loop_speed=',speed, 'loops values', next_loops)

            # Direction is set : move the ghost
            moved = True
            if self.direction == "left" and "left" in self.allowed_moves:
                self.real_x -= speed
                self.rect.x = round(self.real_x/10)
                # go to right tunnel 
                if self.rect.x <= -24 :
                    self.rect.x = self.game.WIDTH-24
                    self.real_x = self.rect.x*10
            elif self.direction == "right" and "right" in self.allowed_moves:
                self.real_x += speed
                self.rect.x = round(self.real_x/10)
                # go to left tunnel
                if self.rect.x >= self.game.WIDTH:
                    self.rect.x = -24
                    self.real_x = -240
            elif self.direction == "up" and "up" in self.allowed_moves:
                self.real_y -= speed
                self.rect.y = round(self.real_y/10)
            elif self.direction == "down" and "down" in self.allowed_moves:
                self.real_y += speed
                self.rect.y = round(self.real_y/10)
            else:
                moved = False
        if moved:
            self.count_moves += 1

        self.rect.x = round(self.real_x/10) - 4
        self.rect.y = round(self.real_y/10) - 4

        if self.direction:
            if moved:
                self.image = self.game.Pacman_pics[self.direction][self.count_moves % 3 + 1]
            else:
                self.image = self.game.Pacman_pics[self.direction][2]

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
        self.real_x = None
        self.real_y = None
        self.color = color
        self.mode = None
        self.old_mode = None
        self.distances = None
        self.allowed_moves = None
        self.forbid_turnback = None
        self.in_tunnel = None
        self.direction = None
        self.speed = None
        self.count_moves = None
        self.blinking_tempo = None
        self.mode_changed = None
        self.start_time = None
        self.image = None
        self.target = None

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
        #self.direction = "left"
        self.direction = ''
        self.speed = 55
        self.blinking_tempo = 0
        self.in_tunnel = False

        # for collisions
        self.radius = 3

        # for the timers
        self.start_time = time.time()
        self.mode_changed = False


        if self.color in ('red', 'yellow', 'blue', 'pink'):
            self.image = self.game.Ghost_pics[self.color]['left'][1]
        else:
            self.image = self.game.Bonuses[self.color]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 + 12, self.y * 24 + 12)

        self.real_x = self.x * 24 * 10
        self.real_y = self.y * 24 * 10

    # Pinky is pink
    def get_pinky_ambush_direction(self):
        """
        Pinky will go 4 tiles from pacman, depending its direction
        """
        if self.game.pacman.direction == "left":
            ambush_x = self.game.pacman.x - 4
            ambush_y = self.game.pacman.y
        elif self.game.pacman.direction == "right":
            ambush_x = self.game.pacman.x + 4
            ambush_y = self.game.pacman.y
        elif self.game.pacman.direction == "down":
            ambush_x = self.game.pacman.x
            ambush_y = self.game.pacman.y + 4
        else:
            ambush_x = self.game.pacman.x - 4
            ambush_y = self.game.pacman.y - 4
    
        self.target = (ambush_x, ambush_y)

    # Inky is blue
    def get_inky_ambush_direction(self):
        """
        Inky will go to the opposite position 
        between Blinky (red) and two tiles from pacman
        """
        if self.game.pacman.direction == "left":
            ambush_x = self.game.pacman.x - 2
            ambush_y = self.game.pacman.y
        elif self.game.pacman.direction == "right":
            ambush_x = self.game.pacman.x + 2
            ambush_y = self.game.pacman.y
        elif self.game.pacman.direction == "down":
            ambush_x = self.game.pacman.x
            ambush_y = self.game.pacman.y + 2
        else:
            ambush_x = self.game.pacman.x - 2
            ambush_y = self.game.pacman.y - 2

        # Then, opposite direction from blinky (red) to this point
        ambush_x = ambush_x + ( self.game.red.x - ambush_x )
        ambush_y = ambush_y + ( self.game.red.y - ambush_y )

        self.target = (ambush_x, ambush_y)

    # Clyde is yellow
    def get_clyde_sneaking_direction(self):
        """
        Clyde (yellow) will chase pacman until it's too close.
        At less than 8 tiles, its direction becomes the scatter one
        """
        # Pythagore, of course
        dist_x = abs(self.x - self.game.pacman.x)
        dist_y = abs(self.y - self.game.pacman.y)
        distance = math.sqrt(dist_x**2 + dist_y**2)
        if distance >= 8:
            self.target = (self.game.pacman.x, self.game.pacman.y)
        else:
            self.target = (SCATTER[self.color][0], SCATTER[self.color][1])

    # In chase or runaway modes, we calculate distance between ghost and pacman
    def choose_direction(self):
        """
        calculate a direction based on the distance with pacman
        """
        x = self.x
        y = self.y
        self.distances = dict()

        if self.forbid_turnback == False:
            self.forbid_turnback = True

        if self.mode == "scatter":
            self.target = (SCATTER[self.color][0], SCATTER[self.color][1])
        elif self.mode == "eaten":
            self.target = (JAIL[self.color][0], JAIL[self.color][1])
        elif self.mode == "chase":
            if self.color == "pink":
                self.get_pinky_ambush_direction()
            elif self.color == "blue":
                self.get_inky_ambush_direction()
            elif self.color == "yellow":
                self.get_clyde_sneaking_direction()
            elif self.color == "red":
                self.target = (self.game.pacman.x, self.game.pacman.y)
            else:
                # Runaway
                self.target = (self.game.pacman.x, self.game.pacman.y)

        #if self.mode == "runaway" and self.forbid_turnback:
        #    self.direction = random.choice(list(self.allowed_moves))
        #    return 0

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
            dist_x = abs(x - self.target[0])
            dist_y = abs(y - self.target[1])
            #distance = round(math.sqrt(dist_x * dist_x + dist_y * dist_y))
            distance = math.sqrt(dist_x**2 + dist_y**2)
            self.distances[direction] = distance

        if self.mode in ("chase", "scatter", "eaten", "jail"):
            min_dist = 99999999999
        elif self.mode == "runaway":
            min_dist = -1

        for key, value in self.distances.items():
            # In chase mode : select the nearest direction
            if self.mode in ("chase", "scatter", "eaten" , "jail"):
                if value < min_dist:
                    min_dist = value
                    self.direction = key
            # In run away mode: select the farthest direction
            elif self.mode == "runaway":
                if value > min_dist:
                    min_dist = value
                    self.direction = key

    # Checks the free positions around the ghost
    def get_allowed_moves(self, x=None, y=None):
        """
        based on current position, list all possible directions
        """
        allowed_moves = []

        if not x:
            x = self.x
            y = self.y

        # check walls
        # 28 (0-27) x 31 (0-30)
        if MAP[y][x-1] < 16:
            allowed_moves.append("left")
        # Problems with right tunnel : a ghost can go there
        if (x+1 < 28 and MAP[y][x+1] < 16) or x+1 == 28:
            allowed_moves.append("right")
        # if not in jail mode , we can go outside
        if x<28 and (MAP[y - 1][x] < 16 or (self.mode != "jail" and MAP[y - 1][x] == 17)):
            allowed_moves.append("up")
        # You can only enter in jail in eaten mode
        if x<28 and (MAP[y + 1][x] < 16 or (self.mode == "eaten" and MAP[y + 1][x] == 17)):
            allowed_moves.append("down")

        # In some positions ghist isn't allowed to go up, except if eaten (to go directly in jail)
        if 'up' in allowed_moves and self.mode != 'eaten':
            for position in FORBIDDEN_UP:
                if x == position[0] and y-1 == position[1]:
                    allowed_moves.remove('up')
                    break

        # Remove opposition direction By default : no turn back
        if self.direction != '':
            reverse = self.opposite[self.moves.index(self.direction)]

            if self.forbid_turnback and reverse in allowed_moves:
                #if reverse in self.allowed_moves:
                allowed_moves.remove(reverse)

            # It should happen only if a row line
            if len(allowed_moves) == 0:
                allowed_moves.append(reverse)

        return(allowed_moves)

    # Check time spent in current mode then change it based on a timer
    def change_mode(self, new_mode=False):
        """
        Change the current move mode, based on a timer or a given value
        """
        self.mode_changed = False

        if new_mode:
            # start time of runaway is aways the same as pacman in chase
            self.old_mode = self.mode
            self.mode = new_mode
            self.mode_changed = True
        else:
            # Modes are managed by game loop
            # Runaway is sync with pacman current status
            if self.mode == 'runaway':
                if self.game.pacman.mode != 'chase':
                    self.mode = LEVELS[self.game.level]['MODES'][self.game.current_mode_idx][0]
                    self.get_speed()

            # Eaten and runaway are specific: don't change the mod during it
            if self.mode not in ('eaten', 'runaway'):
                self.mode = LEVELS[self.game.level]['MODES'][self.game.current_mode_idx][0]
                if self.old_mode != self.mode:
                    self.mode_changed = True
                    self.old_mode = self.mode

                if self.color == 'red' and self.game.pacgums <= LEVELS[self.game.level]['red_dots_remaining']:
                    self.mode = "chase"

        if self.mode_changed:
            self.get_speed()
            self.start_time = time.time()
            if self.mode not in ('scatter'):
                self.forbid_turnback = False
            print(self.color, "mode changed to ", self.mode)

    def get_speed(self):
        # new speed ?
        if self.mode == "eaten":
            self.speed = 180
        elif self.mode == "runaway":
            self.speed = 20
        elif self.mode == "chase":
            self.speed = 55
        else:
            self.speed = 55

    # main function
    def update(self):
        """
        Update the ghost status and position
        main control
        """
        # For blinking temporisation in Frightened mode
        self.blinking_tempo += 0.25

        # Check if we're in eaten and we are now on expected coordinates
        if self.mode == "eaten" and self.x == JAIL[self.color][0] and self.y == JAIL[self.color][1]:
            self.reinit(JAIL[self.color][0], JAIL[self.color][1], "jail")

        # change mode based on timer
        self.change_mode()

        # in tunnel divide speed by 2
        if MAP[self.y][self.x] == 15:
            self.in_tunnel = True
        else:
            self.in_tunnel = False

        current_speed = self.speed
        if self.in_tunnel:
            current_speed = int(self.speed/2)

        # if the next move exceeds the next case
        if self.direction == 'left' and self.real_x-current_speed < (self.x-1)*24*10:
            next_speed = self.real_x - (self.x-1)*240
        elif self.direction == 'right' and self.real_x+current_speed > (self.x+1)*24*10:
            next_speed = (self.x+1)*240  - self.real_x
        elif self.direction == 'up' and self.real_y-current_speed < (self.y-1)*24*10:
            next_speed = self.real_y - (self.y-1)*240
        elif self.direction == 'down' and self.real_y+current_speed > (self.y+1)*24*10:
            next_speed = (self.y+1)*240 - self.real_y
        else:
            next_speed = current_speed


        next_loops = (next_speed, current_speed-next_speed)
        #if self.color == 'red':
        #    print("next_loops=", next_loops)

        for speed in next_loops:
            if speed == 0:
                continue
            # Choose a direction only when we're on a MAP coordinates
            if (self.real_x /10) % 24 == 0 and (self.real_y/10) % 24 == 0:

                self.x = int(self.real_x / 10 / 24)
                self.y = int(self.real_y / 10 / 24)

                # What are the allowed moves ?
                self.allowed_moves = self.get_allowed_moves()
                self.choose_direction()

                # change mode alreay done, directino alreay set, we can forbid
                self.forbid_turnback = True

            #if self.color == "red":
            #    print(self.color, 'direction=', self.real_x, self.real_y, self.x, self.y,  self.direction, 'Original speed=', self.speed, 'real_speed', real_speed, 'loop_speed=',speed, 'loops values', next_loops)

            # Direction is set : move the ghost
            if self.direction == "left":
                self.real_x -= speed
                self.rect.x = round(self.real_x/10)
                # go to right tunnel 
                if self.rect.x <= -24 :
                    self.rect.x = self.game.WIDTH-24
                    self.real_x = self.rect.x*10
            elif self.direction == "right":
                self.real_x += speed
                self.rect.x = round(self.real_x/10)
                # go to left tunnel
                if self.rect.x >= self.game.WIDTH:
                    self.rect.x = -24
                    self.real_x = -240
            elif self.direction == "up":
                self.real_y -= speed
                self.rect.y = round(self.real_y/10)
            elif self.direction == "down":
                self.real_y += speed
                self.rect.y = round(self.real_y/10)

        self.rect.x = round(self.real_x/10) - 4
        self.rect.y = round(self.real_y/10) - 4

        # Ghosts bitmaps depending of the status
        if self.mode == "runaway":
            current_time = time.time()
            # The last 3 seconds : blink
            if PACMAN_TIMERS['chase'] - (current_time - self.start_time) < 3:
                self.image = self.game.Frightened_ghost_blinking[int(self.blinking_tempo) % 4 + 1]
            else:
                self.image = self.game.Frightened_ghost[int(self.blinking_tempo) % 2 + 1]
        elif self.mode == "eaten":
            self.image = self.game.Ghost_eyes[self.direction]
        else:
            self.image = self.game.Ghost_pics[self.color][self.direction][int(self.blinking_tempo) % 2 + 1]

class Game:
    """
    Main class that manages the full game
    """
    def __init__(self):
        self.theme = "default"
        self.dymmy = None
        self.Pacman_pics = None
        self.Dead_pacman = None
        self.Ghost_pics = None
        self.Ghost_eyes = None
        self.Scores = None
        self.Frightened_ghost = None
        self.Frightened_ghost_blinking = None
        self.Walls = None
        self.Bonuses = None
        self.Ready = None
        self.ghosts_in_a_row = 0

        # ghosts are set using setattr but pylint is yelling...
        self.pink = None
        self.red = None
        self.blue = None
        self.yellow = None

        # Sounds
        self.munch = None

        self.WIDTH = len(MAP[0])*24
        self.HEIGHT = len(MAP)*24

        self.FULL_WIDTH = self.WIDTH
        self.FULL_HEIGHT = self.HEIGHT + 72

        self.lifes = 3

        self.pacgums = self.count_pacgums()
        self.score = 0

        self.scale = 1
        self.FPS = 30

        self.count_loops = 0

        self.level = 0


        self.start_mode_timer = None
        self.current_mode_idx = 0
        self.current_mode = None

        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()

        # parse args
        self.parse_args()

        # Check vertical resolution
        display_infos = pygame.display.Info()
        y_resolution = display_infos.current_h

        if y_resolution < 800:
            self.scale = 0.75


        self.screen = pygame.display.set_mode((int(self.FULL_WIDTH * self.scale), int(self.FULL_HEIGHT * self.scale)))
        self.fake_screen = pygame.Surface((self.FULL_WIDTH, self.FULL_HEIGHT))
        pygame.display.set_caption("Pacman by Usawa")

        # create a surface to work on
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.top = pygame.Surface((self.WIDTH, 32))
        self.bottom = pygame.Surface((self.WIDTH, 40))

        # load bitmaps
        self.load_bitmaps()
        # load sounds
        self.load_sounds()

        # declare sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_ghosts = pygame.sprite.Group()

        # Bonus
        self.bonus = None

        self.red = Ghost(self, 13, 11, 'red', "scatter")
        for color in ("blue", "yellow", "pink"):
            setattr(self, color, Ghost(self, JAIL[color][0], JAIL[color][1], color, "jail") )

        self.Ghosts = []

        self.Ghosts.append(self.pink)
        self.Ghosts.append(self.red)
        self.Ghosts.append(self.yellow)
        self.Ghosts.append(self.blue)

        # declare pacman
        self.pacman = Pacman(self, PACMAN_POS[0], PACMAN_POS[1])

        self.all_sprites.add(self.pacman)
        self.all_sprites.add(self.Ghosts)
        # for collisions
        self.all_ghosts.add(self.Ghosts)

    def parse_args(self):
        """
        Parse arguments
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--theme', help='Theme name', default='default')
        args = parser.parse_args()

        # Even if not set, theme is 'default'
        # Check if theme directory is here
        if not os.path.isdir(os.path.join(os.path.dirname(__file__), 'themes/'+args.theme)):
            print("Theme "+args.theme+" directory not found. Default will be used", file=sys.stderr)
            self.theme = 'default'
        else:
            self.theme = args.theme


    def load_sounds(self):
        """
        load sounds
        """
        game_folder = os.path.dirname(__file__)
        snd_folder = os.path.join(game_folder, 'themes/'+self.theme+'/snd')

        self.ready = pygame.mixer.Sound(os.path.join(snd_folder,'game_start.wav'))

        self.munch = dict()
        self.munch[1] = pygame.mixer.Sound(os.path.join(snd_folder, 'munch_1.wav'))
        self.munch[2] = pygame.mixer.Sound(os.path.join(snd_folder, 'munch_2.wav'))

        self.snd_eat_fruit = pygame.mixer.Sound(os.path.join(snd_folder, 'eat_fruit.wav'))
        self.snd_eat_ghost = pygame.mixer.Sound(os.path.join(snd_folder, 'eat_ghost.wav'))
        self.snd_power_pellet = pygame.mixer.Sound(os.path.join(snd_folder, 'power_pellet.wav'))

        self.snd_death_1 = pygame.mixer.Sound(os.path.join(snd_folder, 'death_1.wav'))
        self.snd_death_2 = pygame.mixer.Sound(os.path.join(snd_folder, 'death_2.wav'))

        self.snd_retreating = pygame.mixer.Sound(os.path.join(snd_folder, 'retreating.wav'))

        self.snd_siren_1 = pygame.mixer.Sound(os.path.join(snd_folder, 'siren_1.wav'))

    def load_bitmaps(self):
        """
        Load all bitmaps in use in the game
        """

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'themes/'+self.theme+'/img')

        # load ghost pictures
        self.Frightened_ghost = dict()
        self.Frightened_ghost[1] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'frightened_ghost_1.png')).convert(),(32,32))
        self.Frightened_ghost[2] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'frightened_ghost_2.png')).convert(),(32,32))
        self.Frightened_ghost[1].set_colorkey(BLACK)
        self.Frightened_ghost[2].set_colorkey(BLACK)

        # frightened and blinking
        self.Frightened_ghost_blinking = dict()
        self.Frightened_ghost_blinking[1] = self.Frightened_ghost[1]
        self.Frightened_ghost_blinking[2] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'frightened_ghost_4.png')).convert(),(32,32))
        self.Frightened_ghost_blinking[3] = self.Frightened_ghost[2]
        self.Frightened_ghost_blinking[4] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'frightened_ghost_3.png')).convert(),(32,32))
        self.Frightened_ghost_blinking[2].set_colorkey(BLACK)
        self.Frightened_ghost_blinking[4].set_colorkey(BLACK)

        # Standard ones
        self.Ghost_pics = dict()
        for color in ('red', 'yellow', 'blue', 'pink'):
            self.Ghost_pics[color] = dict()
            for direction in ('left', 'right', 'up', 'down'):
                self.Ghost_pics[color][direction] = dict()
                for i in range(1, 3):
                    self.Ghost_pics[color][direction][i] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, color+'_'+direction+'_ghost_'+str(i)+'.png')).convert(),(32,32))
                    self.Ghost_pics[color][direction][i].set_colorkey(BLACK)

        # Ghost eyes
        self.Ghost_eyes = dict()
        for direction in ('left', 'right', 'up', 'down'):
            self.Ghost_eyes[direction] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'ghost_eyes_'+direction+'.png')).convert(),(32,32))
            self.Ghost_eyes[direction].set_colorkey(BLACK)

        # load pacman pictures
        self.Pacman_pics = dict()
        for direction in ('left', 'right', 'up', 'down'):
            self.Pacman_pics[direction] = dict()
            for i in range(1, 4):
                self.Pacman_pics[direction][i] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'pacman_'+direction+'_'+str(i)+'.png')).convert(),(32,32))
                self.Pacman_pics[direction][i].set_colorkey(BLACK)

        # dead pacman pictures
        self.Dead_pacman = dict()
        for i in range(1, 11):
            self.Dead_pacman[i] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, 'pacman_dead_'+str(i)+'.png')).convert(),(32,32))
            self.Dead_pacman[i].set_colorkey(BLACK)

        # Ghost scores
        self.Scores = dict()
        for score in (100, 200, 300, 400, 500, 700, 800, 1000, 1600, 2000, 3000, 5000):
            self.Scores[score] = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder, str(score)+'.png')).convert(),(32,32))
            self.Scores[score].set_colorkey(BLACK)

        # load walls based on values in MAP and if associated png exists
        self.Walls = dict()
        for l in MAP:
            for c in l:
                if c not in self.Walls:
                    png = os.path.join(img_folder, str(c) + ".png")
                    if os.path.exists(png):
                        self.Walls[c] = pygame.image.load(png).convert()

        # Bonuses
        for bonus in range(7,15):
            self.Walls[bonus] = pygame.image.load(os.path.join(img_folder, str(bonus)+'.png')).convert()
            self.Walls[bonus].set_colorkey(BLACK)

        # Ready
        self.Ready = pygame.image.load(os.path.join(img_folder, 'ready.png')).convert()
        self.Ready.set_colorkey(BLACK)

    def display_board_game(self):
        """
        Display board game with map and sprites
        """
        # Draw all
        self.clear_all_surfaces()

        # Score
        self.display_score()
        # draw walls
        self.display_map(self.surface)

        # Draw sprites
        self.all_sprites.draw(self.surface)

        self.display_lifes(self.bottom)

        self.blit_all_surfaces()

    def display_text(self, my_surface, my_text, pos_x, pos_y, color=WHITE):
        """
        TBD: display a text
        """
        font = pygame.font.Font('RetroGaming.ttf', 18)
        text = font.render(my_text, True, color)
        my_surface.blit(text, (pos_x, pos_y))

    def display_score(self):
        self.display_text(self.top, "Player 1     Score: {}".format(self.score), 24, 6)

    def display_lifes(self, my_surface):
        """
        Based on number of remaining lifes, display them
        """
        for life in range(0, self.lifes - 1):
            my_surface.blit(self.Pacman_pics['right'][2], (life*32+24, 4))

    def eat_bonus(self, bonus):
        """
        Display bonus value
        """

        x_pos = 13*24
        y_pos = 17*24

        pygame.mixer.Sound.play(self.snd_eat_fruit)

        score = FRUITS[bonus]['score']
        i = 1
        while i < 7:

            # evaluate the pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Draw all
            self.clear_all_surfaces()

            # Score
            self.display_score()
            # draw walls
            self.display_map(self.surface)

            # Draw sprites
            self.all_sprites.draw(self.surface)
            self.display_lifes(self.bottom)

            # draw score on the top of ghost
            self.surface.blit(self.Scores[score], (x_pos, y_pos - (4*i)))

            self.blit_all_surfaces()

            # *after* drawing everything, flip the display
            pygame.display.flip()

            i += 1
            time.sleep(0.05)

    def eat_ghost(self, ghost, score):
        """
        Display Score over ghost
        """

        x_pos = ghost.rect.x
        y_pos = ghost.rect.y
        pygame.mixer.Sound.play(self.snd_eat_ghost)
        self.all_sprites.remove(ghost)
        i = 1
        while i < 7:

            # evaluate the pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Draw all
            self.clear_all_surfaces()

            # Score
            self.display_score()
            # draw walls
            self.display_map(self.surface)

            # Draw sprites
            self.all_sprites.draw(self.surface)
            self.display_lifes(self.bottom)

            # draw score on the top of ghost
            self.surface.blit(self.Scores[score], (x_pos, y_pos - (4*i)))

            self.blit_all_surfaces()

            # *after* drawing everything, flip the display
            pygame.display.flip()

            i += 1
            time.sleep(0.05)
        self.all_sprites.add(ghost)
        # sound for ghost back to jail
        pygame.mixer.Sound.play(self.snd_retreating)


    def start_game(self):
        """
        Start a game
        """
        i = 0
        pygame.mixer.Sound.play(self.ready)

        while i<4:
            # evaluate the pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            i += 1 
            # Draw all
            self.clear_all_surfaces()

            # draw walls
            self.display_map(self.surface)
            # Score
            self.display_score()
            # draw walls
            self.display_map(self.surface)

            # Draw sprites
            self.all_sprites.draw(self.surface)
            self.display_lifes(self.bottom)

            # draw Ready !
            self.surface.blit(self.Ready, (11*24, 17*24))

            self.blit_all_surfaces()

            # *after* drawing everything, flip the display
            pygame.display.flip()

            time.sleep(1)
        pygame.mixer.Sound.play(self.snd_siren_1, loops=-1, fade_ms=500 )

        
    def loose_life(self):
        """
        Display the dead pacman animation
        and reset everything
        """

        self.lifes -= 1

        # remove bonus
        MAP[17][13] = 0

        # Play sound 
        pygame.mixer.stop()
        pygame.mixer.Sound.play(self.snd_death_1)
        i = 1
        while i < 15:

            # evaluate the pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Draw all
            self.clear_all_surfaces()

            # draw walls
            self.display_map(self.surface)

            # Animate the dead pacman
            if i<11:
                self.surface.blit(self.Dead_pacman[i], (self.pacman.rect.x, self.pacman.rect.y))
            else:
                if i%2:
                    self.surface.blit(self.Dead_pacman[10], (self.pacman.rect.x, self.pacman.rect.y))
            self.display_lifes(self.bottom)

            self.blit_all_surfaces()

            # *after* drawing everything, flip the display
            pygame.display.flip()
            i += 1

            time.sleep(0.1)
        pygame.display.update()
        pygame.mixer.Sound.play(self.snd_death_2)

        # Reinit everything
        self.pacman.reinit(PACMAN_POS[0], PACMAN_POS[1])
        for ghost in self.Ghosts:
            ghost.reinit(JAIL[ghost.color][0], JAIL[ghost.color][1], "jail")

        # Remaining lifes ? We restart
        if self.lifes > 0:
            self.start_game()
        
        # Timers reinit
        self.current_mode_idx = 0
        self.start_mode_timer = time.time()


    def clear_all_surfaces(self):
        """
        All surfaces in black
        """
        self.fake_screen.fill(BLACK)
        self.surface.fill(BLACK)
        self.top.fill(BLACK)
        self.bottom.fill(BLACK)

    def blit_all_surfaces(self):
        """
        Put all surfaces on screen and scale it if needed
        """
        self.fake_screen.blit(self.top, (0, 0))
        self.fake_screen.blit(self.surface, (0, 32))
        self.fake_screen.blit(self.bottom, (0, self.HEIGHT+32))
        self.screen.blit(self.scale_output(self.fake_screen, self.scale), (0, 0))

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
                    if c != 2:
                        my_surface.blit(self.Walls[c], (x*24, y*24))
                    else:
                        if self.count_loops%8 in range(0,3):
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
        self.ghosts_in_a_row = 0
        lives_gained = 0

        clock = pygame.time.Clock()
        # Game loop
        running = True
        while running and self.level <= 1:
            self.count_loops = 0

            # start game
            self.start_game()

            # increment level
            self.level += 1

            self.current_mode_idx = 0
            self.current_mode = LEVELS[self.level]['MODES'][self.current_mode_idx][0]
            self.start_mode_timer = time.time()

            while running:

                # keep loop running at the right speed
                clock.tick(self.FPS)

                self.count_loops += 1

                # Process input (events)
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        running = False

                # check if it's time to change mode
                current_time = time.time()
                if current_time - self.start_mode_timer > LEVELS[self.level]['MODES'][self.current_mode_idx][1]:
                    self.start_mode_timer = current_time
                    self.current_mode_idx += 1
                    self.current_mode = LEVELS[self.level]['MODES'][self.current_mode_idx][0]

                self.pacman.update()
                self.all_ghosts.update()

                # Add a life every 10000 points
                if int(self.score / 10000) > lives_gained:
                    lives_gained += 1
                    self.lifes += 1

                self.display_board_game()

                # *after* drawing everything, flip the display
                pygame.display.flip()


                # Collision test
                hit_list = self.collided()
                if hit_list:
                    if self.pacman.mode == "chase":
                        for ghost in hit_list:
                            if ghost.mode == "runaway":
                                ghost.change_mode("eaten")
                                self.ghosts_in_a_row += 1
                                # Use a pow()
                                ghost_score = 200*math.pow(2, self.ghosts_in_a_row-1)
                                self.score += ghost_score
                                # Found a sort of bug where collided the same ghost 5 times in a row !!! (collide function bug ???)
                                #if ghost_score > 1600:
                                #    self.ghosts_in_a_row = 0
                                # diplay score
                                self.eat_ghost(ghost, ghost_score)
                            elif ghost.mode != "eaten":
                                self.loose_life()
                    else:
                        for ghost in hit_list:
                            if ghost.mode not in ("eaten", "runaway"):
                                self.loose_life()
                                break

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
