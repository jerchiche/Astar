import logging
from itertools import product

###############################################################################
# Logging
###############################################################################
LOG_FORMAT = '%(asctime)s - %(levelname)-8s - %(message)s'
LOG_FORMAT = logging.Formatter(LOG_FORMAT)

log = logging.getLogger('term')
log.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(LOG_FORMAT)
log.addHandler(c_handler)

flog = logging.getLogger('to_file')
flog.setLevel(logging.INFO)
f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(LOG_FORMAT)
flog.addHandler(f_handler)

###############################################################################
# GUI settings
###############################################################################
no_border = {'borderwidth':0, 'highlightthickness':0}

# Sizes
ROWS = 50
COLS = 50

# Map items
EMPTY = 'white'
ORIG = 'green'
DEST = 'blue'
WALL = 'red'

###############################################################################
# Directions
###############################################################################
N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)
NE = (-1, 1)
NW = (-1, -1)
SE = (1, 1)
SW = (1, -1)
dir_list = (N, S, E, W, NE, NW, SE, SW)

###############################################################################
# Basic functions
###############################################################################
def in_board(r=None, c=None):
    if r is None and c is None: return product(range(ROWS), range(COLS))
    elif r is None: return c in range(COLS)
    elif c is None: return r in range(ROWS)
    else: return r in range(ROWS) and c in range(COLS)
def add(vec1, vec2): return tuple(v1+v2 for v1, v2 in zip(vec1, vec2))
def dist(vec1, vec2):
    return round(sum((v1-v2)**2 for v1, v2 in zip(vec1, vec2))**(1/2), 2)
def manh_dist(vec1, vec2):
    return sum(abs(v1-v2) for v1, v2 in zip(vec1, vec2))

###############################################################################
if __name__ == "__main__":
    orig = (0, 0)
    dest = (3, 4)
    log.info(f'{dist(orig, dest)=}')
    log.info(f'{manh_dist(orig, dest)=}')
