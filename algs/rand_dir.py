from random import randint

class Rand_Dir():

  dirs = {
    0 : 'up',
    1 : 'right',
    2: 'down',
    3: 'left'
  }

  def get_dir(self):
    return self.dirs[randint(0, 3)]