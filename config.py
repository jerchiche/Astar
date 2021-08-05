import logging, os

# Logging
log_set = {
    'level': logging.INFO,
    'format': r'%(asctime)s.%(msecs)03d - %(levelname)-8s - %(message)s',
    'datefmt': r'%H-%M-%S'}
logging.basicConfig(**log_set)
log = logging.getLogger()

# GUI settings
no_border = {'borderwidth':0, 'highlightthickness':0}

# Map items
EMPTY = 'white'
ORIG = 'green'
DEST = 'blue'
WALL = 'red'

# Directions
N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)
NE = (-1, 1)
NW = (-1, -1)
SE = (1, 1)
SW = (1, -1)
dir_list = [N, S, E, W, NE, NW, SE, SW]

# Sizes
ROWS = 50
COLS = 50

# Basic functions
def inBoard(r, c): return r in range(ROWS) and c in range(COLS)
def add(vec1, vec2): return tuple(v1+v2 for v1, v2 in zip(vec1, vec2))
def dist(vec1, vec2):
    return round(sum((v1-v2)**2 for v1, v2 in zip(vec1, vec2))**(1/2), 2)
def manhDist(vec1, vec2):
    return sum(abs(v1-v2) for v1, v2 in zip(vec1, vec2))

if __name__ == "__main__":
    orig = (0, 0)
    dest = (1, 1)
    print(
        f'Distance between {orig} and {dest} is: '
        f'{dist(orig, dest)}')
    print(
        f'Manhattan distance between {orig} and {dest} is: '
        f'{manhDist(orig, dest)}')
