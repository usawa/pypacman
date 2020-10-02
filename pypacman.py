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

JAIL = { "red": (12,14) ,
         "blue": (13,14),
         "yellow": (14,14),
         "pink": (15,14)
}

PACMAN_TIMERS = {
    "normal": 999999999,
    "chase": 8
}

PACMAN_POS = (14, 17)

GHOST_TIMERS = {
    "red": {
        "jail": 3,
        "scatter": 10,
        "chase": 15,
        "random": 10
    },
    "blue": {
        "jail": 4,
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
        [15, 15, 15, 15, 15, 15,  1,  1,  1,  1, 51, 64,  0,  0,  0,  0, 64, 50,  1,  1,  1,  1, 15, 15, 15, 15, 15, 15],
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
            self.mode_changed = True
            for ghost in self.game.Ghosts:
                if ghost.mode != "to_jail":
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
        self.direction = ""
        self.speed = 4
        self.blinking_tempo = 0
        self.in_tunnel = False

        # for collisions
        self.radius = 6

        # for the timers
        self.start_time = time.time()
        self.mode_changed = False


        self.image = self.game.Ghost_pics[self.color]['left'][1]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * 24 + 12, self.y * 24 + 12)

        self.real_x = self.x * 24 + 12
        self.real_y = self.y * 24 + 12

    # In chase or runaway modes, we calculate distance between ghost and pacman
    def distance_based_direction(self):
        """
        calculate a direction based on the distance with pacman
        """
        x = self.x
        y = self.y
        self.distances = dict()

        # Previously in jail: target to the up to force ghost to go outside
        if self.old_mode == "jail":
            self.target = (14, 1)
            # Once we're outside: we go to expected coordinates
            if self.y <= self.game.jail_output:
                self.old_mode = ""
        elif self.mode == "scatter":
            self.target = (SCATTER[self.color][0], SCATTER[self.color][1])
        elif self.mode == "to_jail":
            self.target = (JAIL[self.color][0], JAIL[self.color][1])
        else:
            self.target = (self.game.pacman.x, self.game.pacman.y)

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
            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            self.distances[direction] = distance

        if self.mode in ("chase", "scatter", "to_jail"):
            min_dist = 99999999999
        elif self.mode == "runaway":
            min_dist = -1

        for key, value in self.distances.items():
            # In chase mode : select the nearest direction
            if self.mode in ("chase", "scatter", "to_jail"):
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
        if self.mode in ("random", "jail"):
            self.direction = random.choice(self.allowed_moves)
        elif self.mode in ("chase", "runaway", "scatter", "to_jail"):
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
        # Problems with right tunnel : a ghost can go there
        if (self.x+1 < 28 and MAP[self.y][self.x+1] < 16) or self.x+1 == 28:
            self.allowed_moves.append("right")
        # if in jail, and no more in jail mode, we can go outside
        if MAP[self.y - 1][self.x] < 16 or (self.mode != "jail" and MAP[self.y - 1][self.x] == 17):
            self.allowed_moves.append("up")
        if MAP[self.y + 1][self.x] < 16 or (self.mode == "to_jail" and MAP[self.y + 1][self.x] == 17):
            self.allowed_moves.append("down")

        # Remove opposition direction By default : no turn back
        if self.direction != '':
            reverse = self.opposite[self.moves.index(self.direction)]

            if self.forbid_turnback and reverse in self.allowed_moves:
                #if reverse in self.allowed_moves:
                self.allowed_moves.remove(reverse)

            # It should happen only if a row line
            if len(self.allowed_moves) == 0:
                self.allowed_moves.append(reverse)


    # Check time spent in current mode then change it based on a timer
    def change_mode(self, new_mode=False):
        """
        Change the current move mode, based on a timer or a given value
        """
        current_time = time.time()

        if new_mode:
            # start time of runaway is aways the same as pacman in chase
            self.start_time = self.game.pacman.start_time
            self.old_mode = self.mode
            self.mode = new_mode
            self.mode_changed = True

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

        # For blinking temporisation in Frightened mode
        self.blinking_tempo += 0.25

        # Choose a direction only when we're on a MAP coordinates
        if self.rect.x % 24 == 0 and self.rect.y % 24 == 0:

            self.x = int(self.rect.x / 24)
            self.y = int(self.rect.y / 24)

            # Check if we're in to_jail and we are now on expected coordinates
            if self.mode == "to_jail" and self.x == JAIL[self.color][0] and self.y == JAIL[self.color][1]:
                self.reinit(JAIL[self.color][0], JAIL[self.color][1], "jail")

            # What are the allowed moves ?
            self.get_allowed_moves()

            # choose a direction, based on the ghost mode
            self.choose_direction()

            # change mode alreay done, directino alreay set, we can forbid
            self.forbid_turnback = True

            """
            Allowed speeds:
            1       24 moves to the next position
            2       12
            2.1818  11
            2.4     10
            3        8
            3.4285   7
            4        6
            4.8      5
            6        4
            8        3
            12       2
            24       1
            """

            # new speed ?
            if self.mode == "to_jail":
                self.speed = 12
            elif self.mode == "runaway":
                self.speed = 2
            elif self.mode == "chase":
                if self.color == "red":
                    if self.speed == 4:
                        self.speed = 4.8
                    else:
                        self.speed = 4
                else:
                    self.speed = 4
            else:
                self.speed = 4

            # in tunnel reduce speed to 2
            if MAP[self.y][self.x] == 15:
                if not self.in_tunnel:
                    self.in_tunnel = True
            else:
                self.in_tunnel = False

            if self.in_tunnel:
                self.speed = 2

        # Direction is set : move the ghost
        if self.direction == "left":
            self.real_x -= self.speed
            self.rect.x = round(self.real_x)
            # go to right border
            if self.rect.x < -12 :
                self.rect.x = self.game.WIDTH-12
                self.real_x = self.rect.x

        if self.direction == "right":
            self.real_x += self.speed
            self.rect.x = round(self.real_x)
            # go to left border
            if self.rect.x >= self.game.WIDTH:
                self.rect.x = -12
                self.real_x = -12

        if self.direction == "up":
            self.real_y -= self.speed
            self.rect.y = round(self.real_y)
            if self.rect.y < 0:
                self.rect.y = self.game.HEIGHT-12
                self.real_y = self.rect.y

        if self.direction == "down":
            self.real_y += self.speed
            self.rect.y = round(self.real_y)
            if self.rect.y >= self.game.HEIGHT:
                self.rect.y = 0
                self.real_y = 0

        if self.mode == "runaway":
            current_time = time.time()
            # The last 3 seconds : blink
            if GHOST_TIMERS[self.color]['runaway'] - (current_time - self.start_time) < 3:
                self.image = self.game.Frightened_ghost_blinking[int(self.blinking_tempo) % 4 + 1]
            else:
                self.image = self.game.Frightened_ghost[int(self.blinking_tempo) % 2 + 1]
        elif self.mode == "to_jail":
            self.image = self.game.Ghost_eyes[self.direction]
        else:
            self.image = self.game.Ghost_pics[self.color][self.direction][int(self.blinking_tempo) % 2 + 1]
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
        self.Ghost_eyes = None
        self.Frightened_ghost = None
        self.Frightened_ghost_blinking = None
        self.Walls = None

        self.ghosts_in_a_row = 0

        self.WIDTH = len(MAP[0])*24
        self.HEIGHT = len(MAP)*24

        self.FULL_WIDTH = self.WIDTH
        self.FULL_HEIGHT = self.HEIGHT + 64

        self.lifes = 3

        self.pacgums = self.count_pacgums()
        self.score = 0

        self.scale = 1
        self.FPS = 30 

        # Search for prison door to determine coordinates
        self.jail_output = None
        y_length = len(MAP)
        x_length = len(MAP[0])
        for y in range(y_length):
            for x in range(x_length):
                if MAP[y][x] == 17:
                    self.jail_output = y - 1
                    break
            if self.jail_output:
                break

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
        for color in ("red", "blue", "yellow", "pink"):
            self.Ghosts.append(Ghost(self, JAIL[color][0], JAIL[color][1], color, "jail"))

        # Prepare runaway values
        for ghost in self.Ghosts:
            GHOST_TIMERS[ghost.color]['runaway'] = PACMAN_TIMERS['chase']

        # Prepare to_jail values : no real timer, so 99999
        for ghost in self.Ghosts:
            GHOST_TIMERS[ghost.color]['to_jail'] = 99999

        # declare pacman
        self.pacman = Pacman(self, PACMAN_POS[0], PACMAN_POS[1])

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
        self.Frightened_ghost_blinking[2] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_4.png')).convert()
        self.Frightened_ghost_blinking[3] = self.Frightened_ghost[2]
        self.Frightened_ghost_blinking[4] = pygame.image.load(os.path.join(img_folder, 'frightened_ghost_3.png')).convert()

        # Standard ones
        self.Ghost_pics = dict()
        for color in ('red', 'yellow', 'blue', 'pink'):
            self.Ghost_pics[color] = dict()
            for direction in ('left', 'right', 'up', 'down'):
                self.Ghost_pics[color][direction] = dict()
                for i in range(1, 3):
                    self.Ghost_pics[color][direction][i] = pygame.image.load(os.path.join(img_folder, color+'_'+direction+'_ghost_'+str(i)+'.png')).convert()

        # Ghost eyes
        self.Ghost_eyes = dict()
        for direction in ('left', 'right', 'up', 'down'):
            self.Ghost_eyes[direction] = pygame.image.load(os.path.join(img_folder, 'ghost_eyes_'+direction+'.png')).convert()

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

        # Score
        self.display_text(self.top,"Player 1     Score: "+str(int(self.score)), 24, 6)
        # draw walls
        self.display_map(self.surface)

        # Draw sprites
        self.all_sprites.draw(self.surface)

        self.display_lifes(self.bottom)
        self.fake_screen.blit(self.top, (0, 0))
        self.fake_screen.blit(self.surface, (0, 32))
        self.fake_screen.blit(self.bottom, (0, self.HEIGHT+32))

    def display_text(self, my_surface, my_text, pos_x, pos_y):
        """
        TBD: display a text
        """
        font = pygame.font.Font('RetroGaming.ttf', 18)
        text = font.render(my_text, True, WHITE)
        my_surface.blit(text, (pos_x, pos_y))

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
        while i < 15:

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
            if i<11:
                self.surface.blit(self.Dead_pacman[i], (self.pacman.rect.x, self.pacman.rect.y))
            else:
                if i%2:
                    self.surface.blit(self.Dead_pacman[10], (self.pacman.rect.x, self.pacman.rect.y))
            self.display_lifes(self.bottom)
            self.fake_screen.blit(self.top, (0, 0))
            self.fake_screen.blit(self.surface, (0, 32))
            self.fake_screen.blit(self.bottom, (0, self.HEIGHT+32))

            self.screen.blit(self.scale_output(self.fake_screen, self.scale), (0, 0))

            # *after* drawing everything, flip the display
            pygame.display.flip()
            i += 1

            time.sleep(0.1)
        pygame.display.update()

        # Reinit everything
        self.pacman.reinit(PACMAN_POS[0], PACMAN_POS[1])
        for ghost in self.Ghosts:
            ghost.reinit(JAIL[ghost.color][0], JAIL[ghost.color][1], "jail")


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
        self.ghosts_in_a_row = 0
        lives_gained = 0

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

            # Add a life every 10000 points
            if int(self.score ) / 10000 > lives_gained:
                lives_gained += 1
                self.lifes += 1

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
                            ghost.change_mode("to_jail")
                            self.ghosts_in_a_row += 1
                            # Use a pow()
                            ghost_score = 200*math.pow(2, self.ghosts_in_a_row-1)
                            self.score += ghost_score
                        elif ghost.mode != "to_jail":
                            self.lifes -= 1
                            self.loose_life()
                else:
                    if self.pacman.mode != "to_jail":
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
