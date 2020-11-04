# pypacman
A small pacman written in Python, as a pygame proof of concept.

# IT'S NOT FINISHED. Feel Free to contrib, modify, update, rewrite...

## License
The **code and the graphics** are made by myself, and are under **GPLv3** License.
The font is a freeware one.
The sounds are coming from https://www.sounds-resource.com/arcade/pacman/sound/10603/ . No idea about the license, probably (c) Namco.

## The bible
Watch this video: https://www.youtube.com/watch?v=ataGotQ7ir8
## Goals
In September we had a "forum des associations" (non profit organization forum), and I talked with an facilitator of a computer workshop for children (managed by the city), and they wanted to create a pacman, then got stuck because they didn't know how to move the ghosts.
The guy has no real knowledge (he's autodidact) and no big maths skills. I started to tell him to use Pythagore to calculate distances, and so on, but he was lost.
Once at home, I started to think about it : how, it 1980, guys implemented a quick chase algorithm, as arcade machines were slow. So I forgot every A* algorithms, And tried to find one. And I found that Pacman is more complex than expected, as all ghosts have different behaviors. So, I started to implement it.
My goals were:
- understand and implement each ghost algorithm 
- refresh my Python knowledge and skills, as I'm not a "real" developper, but a Sys/DevOps (and now a security guy).
- help this guy
- At the end, get something playable.

## Issues 
The game isn't finished. I stopped the dev once all algorithms were implemented. However I faced issues :
- Pacman and ghosts speed : the algorithm is fast but perfectible
- Directions can be modified only on a "case" of the map. For example, in "frightened" mode, the ghosts have to finish their move to the next case to turn back.
- Levels aren't implemented, neither the start/pause screen, even if the code is ready for that. More code is needed for the bonuses.
- The code itself : I'm not a dev. I code Python for sysadmin, like snmp probes, nagios probes, ansible modules, etc. I also coded parsers, but games, never! So a LOT of things, essentially based on objects, are perfectible. A lot!
- I found sound has issues on Fedora 33 with pygame 1.9.6, so please prefer latest 2.0.0+ (even dev)
- But, ... it works :) And its quite fast.

## Installation
Use Python 3.6+
Just install pygame 2.0.0.devXX (1.9.6 should work but with some sound issues). See pygame website to see how to do it.
Then launch ./pypacman.py

Code was written using Visual Studio Code (what a wonderful thing!).
Sprites has been designed using Piskel https://www.piskelapp.com/

Tested on Linux (Fedora 32) and MacOS 10.13 and 10.15. On MacOS, perfs are really better with sdl2 and pygame 2.0.0.devXX.
```bash
./pypacman.py
```

Performances are terrible on HiDPI (retina) displays and pygame 1.9.x. Launch with :
```bash
./pypacman.py -AppleMagnifiedMode YES
```

## Play
- Map is the real pacman one
- Pellets are the real pacman ones
- Bonus are the real pacman ones
- Ghosts are the real pacman ones, chase algorithms and timers are the same. However speed isn't the same, and directions could change as Pythagore calculation are better.

Just use the direction keys. Close the window, win or loose to quit (not finished).
