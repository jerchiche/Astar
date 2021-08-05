import time, threading
from random import randrange, choice

import user_interface as ui
import config

from walls import walls
from config import (log, add, inBoard, manhDist, dist,
                    N, S, E, W, NE, NW, SE, SW, dir_list,
                    EMPTY, ORIG, DEST, WALL)

gs = ui.game_space
f = 'Dist to end'
g = 'Curr dist'
h = 'Total dist'
clock_call = None

def updateClock():
    global clock_call
    log.debug('Updating clock')
    clock_call = gs.after(10, updateClock)
    secs, hs = map(int, ui.clock['text'].split('.'))
    hs = (hs + 1) % 100
    if not hs: secs += 1
    if hs < 10: hs = f'0{hs}'
    if secs < 10: secs = f'0{secs}'
    ui.clock.configure(text=f'{secs}.{hs}')
    log.debug('Clock updated')

def board(row, col, new_type=None, b=None):
    log.debug(f'Calling board ({row}, {col}) with {new_type}')
    if not inBoard(row, col): return WALL
    if new_type:
        gs.itemconfig(ui.board[row][col], fill=new_type)
        log.debug(f'Changed board ({row}, {col}) to {new_type}')
    else:
        log.debug(
            f'Accessed board ({row}, {col}) and found ' +
            f'{gs.itemcget(ui.board[row][col], "fill")}')
        if b: return b[row][col]
        else: return gs.itemcget(ui.board[row][col], 'fill')

def addWall(pos, length, direction=N):
    for _ in range(length):
        if board(*pos) == EMPTY:
            board(*pos, WALL)
        pos = add(pos, direction)

def updateArrow(orig, dest):
    gs.coords(ui.arrows[dest[0]][dest[1]], *ui.arrow_coord(orig, dest))

def resort(l, i, key = None):
    '''Sort sorted list where only index was modified'''
    if key == None: key = lambda x: x
    if i < 0: i += len(l)
    while i > 1 and (key(l[i]) < key(l[i-1])):
        l[i], l[i-1] = l[i-1], l[i]

def showFinding(orig, dest, heuristic=dist):
    open_l = []
    close_l = []
    dist_d = {}
    open_l.append(orig)
    dist_d[orig] = {f: heuristic(orig, dest),  g: 0}
    dist_d[orig][h] = dist_d[orig][f] + dist_d[orig][g]
    log.info(f'Looking for path between {orig} and {dest}')
    while open_l[0] != dest:
        time.sleep(.01)
        log.debug(f'Current is {open_l[0]}')
        if len(open_l)>1: board(*open_l[0], 'orange')
        for pos in [add(open_l[0], d) for d in dir_list]:
            if board(*pos) != WALL and pos not in close_l:
                try:
                    index = open_l.index(pos)
                    if dist_d[pos][g] > dist_d[open_l[0]][g] + 1:
                        dist_d[pos][g] = dist_d[open_l[0]][g] + 1
                        dist_d[pos][h] = dist_d[pos][f] + dist_d[pos][g]
                        dist_d[pos]['from'] = open_l[0]
                        new_i = index
                        while new_i > 1 and dist_d[pos][h] < dist_d[open_l[new_i-1]][h]:
                            new_i -= 1
                        if new_i != index:
                            open_l.insert(new_i, open_l.pop(index))
                        #updateArrow(current, pos)
                except ValueError:
                    dist_d[pos] = {
                        f: heuristic(pos, dest), 
                        g:  dist_d[open_l[0]][g] + 1,
                        'from': open_l[0]}
                    dist_d[pos][h] = dist_d[pos][f] + dist_d[pos][g]
                    index = 1
                    while index < len(open_l) and dist_d[pos][h] > dist_d[open_l[index]][h]:
                        index += 1
                    open_l.insert(index, pos)
                    #updateArrow(current, pos)
                    if pos != dest: board(*pos, 'yellow')
                log.debug(f'Distance for {pos} is {open_l[-1]}')
        close_l.append(open_l.pop(0))
    path = [close_l[-1]]
    while dist_d[path[-1]].get('from', False):
        path.append(dist_d[path[-1]]['from'])
    log.info(f'Path found is {path}')
    for r, c in path:
        board(r, c, 'purple')
    print('Done')
    gs.after_cancel(clock_call)
    return path

def findPath(b, orig, dest, heuristic=dist):
    log.info(f'Looking for path between {orig} and {dest}')
    open_l = []
    close_l = []
    dist_d = {}
    open_l.append(orig)
    dist_d[orig] = {f: heuristic(orig, dest),  g: 0}
    dist_d[orig][h] = dist_d[orig][f] + dist_d[orig][g]
    while open_l and open_l[0] != dest:
        log.debug(f'Current is {open_l[0]}')
        for pos in [add(open_l[0], d) for d in dir_list]:
            if board(*pos, b=b) != WALL and pos not in close_l:
                try:
                    index = open_l.index(pos)
                    if dist_d[pos][g] > dist_d[open_l[0]][g] + 1:
                        dist_d[pos][g] = dist_d[open_l[0]][g] + 1
                        dist_d[pos][h] = dist_d[pos][f] + dist_d[pos][g]
                        dist_d[pos]['from'] = open_l[0]
                        new_i = index
                        while new_i > 1 and dist_d[pos][h] < dist_d[open_l[new_i-1]][h]:
                            new_i -= 1
                        if new_i != index:
                            open_l.insert(new_i, open_l.pop(index))
                        #updateArrow(current, pos)
                except ValueError:
                    dist_d[pos] = {
                        f: heuristic(pos, dest), 
                        g:  dist_d[open_l[0]][g] + 1,
                        'from': open_l[0]}
                    dist_d[pos][h] = dist_d[pos][f] + dist_d[pos][g]
                    index = 1
                    while index < len(open_l) and dist_d[pos][h] > dist_d[open_l[index]][h]:
                        index += 1
                    open_l.insert(index, pos)
                log.debug(f'Distance for {pos} is {open_l[-1]}')
        close_l.append(open_l.pop(0))
    if open_l:
        path = [close_l[-1]]
        while dist_d[path[-1]].get('from', False):
            path.append(dist_d[path[-1]]['from'])
        log.info(f'Path found is {path}')
        return path
    else:
        log.info(f'Path not found')


def main(orig=None, dest=None, walls=None, heuristic=dist, show=False):
    updateClock()
    if not orig:
        orig = (randrange(config.ROWS), randrange(5))
    if not dest:
        dest = (randrange(config.ROWS), randrange(config.COLS-5, config.COLS))
    
    searchingThread = threading.Thread(
        target=showFinding,
        args=(orig, dest, heuristic))
    
    board(*orig, ORIG)
    board(*dest, DEST)
    
    if not walls:
        for _ in range(30):
            pos = (randrange(0, config.ROWS), randrange(config.COLS))
            d = choice(dir_list)
            addWall(pos, randrange(5, 10), d)
    else:
        for r, c in walls:
            board(r, c, WALL)
    
    if show: searchingThread.start()
    else:
        b = [[board(r, c) for c in range(config.COLS)] for r in range(config.ROWS)]
        for r, c in findPath(b, orig, dest, heuristic):
            board(r,c,'purple')

    ui.root.mainloop()
    if show: searchingThread.join()

if __name__ == '__main__':
    orig = (12, 12)
    dest = (25, 48)
    
    main(orig, dest, walls, heuristic=dist, show=1)
