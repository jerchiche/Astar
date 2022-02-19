import time, threading
from random import randrange

import user_interface as ui
import utils as u

###############################################################################
#
###############################################################################
gs = ui.game_space
f = 'Dist to end'
g = 'Curr dist'
h = 'Total dist'
clock_call = None

###############################################################################
#
###############################################################################
def up_clock():
    global clock_call
    clock_call = gs.after(10, up_clock)
    secs, hs = map(int, ui.clock['text'].split('.'))
    hs = (hs + 1) % 100
    if not hs: secs += 1
    ui.clock.configure(text=f'{str(secs).zfill(2)}.{str(hs).zfill(2)}')

###############################################################################
#
###############################################################################
def board(row, col, color=None):
    if not u.in_board(row, col): return u.WALL
    if color: gs.itemconfig(ui.board[row][col], fill=color)
    else: return gs.itemcget(ui.board[row][col], 'fill')

def add_wall(pos, length=1, direction=u.N):
    for _ in range(length):
        if board(*pos) == u.EMPTY: board(*pos, u.WALL)
        pos = u.add(pos, direction)

def show_finding(orig, dest, heuristic=u.dist, show=False):
    up_clock()
    open_l = []
    close_l = []
    dist_d = {}
    open_l.append(orig)
    dist_d[orig] = {f: heuristic(orig, dest),  g: 0}
    dist_d[orig][h] = dist_d[orig][f] + dist_d[orig][g]
    while open_l and open_l[0] != dest:
        if show and len(open_l)>1: board(*open_l[0], 'orange')
        for pos in [u.add(open_l[0], d) for d in u.dir_list]:
            if board(*pos) != u.WALL and pos not in close_l:
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
                    if show and pos != dest: board(*pos, 'yellow')
                u.log.debug(f'Distance for {pos} is {open_l[-1]}')
        close_l.append(open_l.pop(0))
    gs.after_cancel(clock_call)
    if open_l:
        path = [close_l[-1]]
        while dist_d[path[-1]].get('from', False):
            path.append(dist_d[path[-1]]['from'])
        u.log.info(f'Path found is {path}')
        for r, c in path:
            board(r, c, 'purple')
        return path
    else: u.log.info(f'Path not found')

###############################################################################
#
###############################################################################
def main(orig=None, dest=None, heuristic=u.dist, show=False):
    orig = orig or (randrange(u.ROWS), randrange(5))
    dest = dest or (randrange(u.ROWS), randrange(u.COLS-5, u.COLS))
    
    searching_thread = threading.Thread(
        target=show_finding,
        args=(orig, dest, heuristic))
    
    ui.turn_ind.bind('<Button-1>', lambda _: searching_thread.start())
    
    board(*orig, u.ORIG)
    board(*dest, u.DEST)
    

    ui.root.mainloop()
    if show: searching_thread.join()

###############################################################################
#
###############################################################################
if __name__ == '__main__':
    orig = (12, 12)
    dest = (25, 48)
    
    main(heuristic=u.dist, show=1)
