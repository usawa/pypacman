#!/usr/bin/env python3

# from array import *
import random
import time
import math

class phantom:
    "Phantom management"

    moves = ["left","right","up","down"]
    opposite = ["right", "left", "down", "up" ]

    def __init__(self, x, y, color, mode):
        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.distances = dict()
        self.allowed_moves = []
        self.direction = ""

    def distance_based_direction(self):
        x = self.x
        y = self.y
        self.distances = dict()

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
            dist_x = abs(x - pacman.x)
            dist_y = abs(y - pacman.y)
#            distance = round(math.sqrt(dist_x*dist_x + dist_y*dist_y))
            distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)
            self.distances[direction] = distance
        if self.mode == "chase":
            min = 99999999999
        elif self.mode == "runaway":
            min = -1

        for key, value in self.distances.items():
            if self.mode == "chase":
                if value < min:
                    min = value
                    self.direction = key
            elif self.mode == "runaway":
                if value > min:
                    min = value
                    self.direction = key

    def choose_direction(self):
        if self.mode == "random":
            self.direction=random.choice(self.allowed_moves)
        elif self.mode == "chase" or self.mode == "runaway":
            self.distance_based_direction()

    def get_allowed_moves(self):
        self.allowed_moves = self.moves.copy()
        if MAP[self.y][self.x-1] >= 16:
            self.allowed_moves.remove("left")
        if self.x+1 < 28 and MAP[self.y][self.x+1] >= 16:
            self.allowed_moves.remove("right")
        if MAP[self.y - 1][self.x] >= 16:
            self.allowed_moves.remove("up")
        if MAP[self.y + 1][self.x] >= 16:
            self.allowed_moves.remove("down")

        if self.direction != "":
            reverse=self.opposite[self.moves.index(self.direction)]
            if reverse in self.allowed_moves:
                self.allowed_moves.remove(reverse)

    def move(self):
        self.get_allowed_moves()

#        if not self.direction:
        self.choose_direction()

        print("color=",self.color, "x=",self.x,"y=",self.y, "mode=",self.mode, "f.direction=", self.direction, "allowed_moves=",self.allowed_moves, "distances=",self.distances)

        if self.direction == "left":
            if MAP[self.y][self.x-1] <16:
                self.x = self.x -1
                if self.x < 0:
                    self.x = 27
        if self.direction == "right":
            if self.x+1 > 27:
                self.x = 0  
            elif MAP[self.y][self.x+1] <16:
                self.x = self.x + 1
        if self.direction == "up":
            if MAP[self.y - 1][self.x] <16:
                self.y = self.y - 1
        if self.direction == "down":
            if MAP[self.y + 1][self.x] <16:
                self.y = self.y + 1

class pacman:
    "pacman management"
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_status(self, status):
        """
        pacman status: pacgum, dead, normal
        """
        self.status = status
    
    def get_status(self):
        return self.status


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def display_map():
    y_length = len(MAP)
    x_length = len(MAP[0])
    for y in range(y_length):
        for x in range(x_length):
            c=MAP[y][x]
            if c==0:
                ghost = False
                for f in phantoms:
                    if f.x == x and f.y == y:
                        print(" G ", end="")
                        ghost = True
                        break
                if not ghost:
                    if pacman.x == x and pacman.y == y:
                        print(" P ",end="")
                    else:
                        print(" . ", end="")
            if c==16:
                print("\033[0;30;44m   \033[0;37;40m", end="")
            if c==17:
                print("   ", end="")
        print()

MAP = [     [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], 
            [16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0, 16, 17, 17, 16,  0, 16, 17, 17, 17, 16,  0, 16, 16,  0, 16, 17, 17, 17, 16,  0, 16, 17, 17, 16,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0,  0,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0,  0,  0, 16],
            [16, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16, 16],
            [17, 17, 17, 17, 17, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [17, 17, 17, 17, 17, 16,  0, 16, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [17, 17, 17, 17, 17, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17, 17, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16],
            [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 17, 17, 17, 17, 17, 17, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
            [16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17, 17, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16],
            [17, 17, 17, 17, 17, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [17, 17, 17, 17, 17, 16,  0, 16, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [17, 17, 17, 17, 17, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 17, 17, 17, 17, 17],
            [16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16],
            [16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0, 16, 16, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16,  0, 16, 16, 16, 16,  0, 16],
            [16,  0,  0,  0, 16, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 16, 16,  0,  0,  0, 16],
            [16, 16, 16,  0, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16,  0, 16, 16, 16],
            [16, 16, 16,  0, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16,  0, 16, 16, 16],
            [16,  0,  0,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0, 16, 16,  0,  0,  0,  0,  0,  0, 16],
            [16,  0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16], 
            [16,  0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16, 16,  0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0, 16], 
            [16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 , 0 ,16], 
            [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], 
    ]

def collided():
    collided = False
    for f in phantoms:
        if f.x == pacman.x and f.y == pacman.y:
            collided = True
            break
    return collided

phantoms = []
#phantoms.append(phantom(1,1,"red","chase"))
#phantoms.append(phantom(26,1,"blue","random"))
phantoms.append(phantom(1,29,"yellow","runaway"))

pacman = pacman(14, 17)


display_map()

while not collided():
    for f in phantoms:
        # calculate distance

        f.move()

    time.sleep(0.3)

    display_map()

    # Are we in intersection ?

    # 
    # 

