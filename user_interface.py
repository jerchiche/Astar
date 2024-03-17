import tkinter as tk

import utils as u

###############################################################################
#   Settings
###############################################################################
SQ_SIZE = 10
INFO_H = 100
BOARD_H = u.ROWS * SQ_SIZE
BOARD_W = u.COLS * SQ_SIZE

_drag = [u.EMPTY, []]

def pix(x, y): return (x*SQ_SIZE, y*SQ_SIZE, (x+1)*SQ_SIZE, (y+1)*SQ_SIZE)

###############################################################################
# Fonts
TURN_F = f'Arial {INFO_H//4}'
CLOCK_F = f'Arial {INFO_H//4}'

###############################################################################
#   Root initiation
###############################################################################
root = tk.Tk()
root.title('Astar')
root.resizable(False, False)

###############################################################################
#   Info top box
###############################################################################
info = tk.Frame(root, padx=5, pady=5, bg='grey20')
turn_ind = tk.Label(info, text='Drawing', font=TURN_F)
clock = tk.Label(info, text='00.00', font=CLOCK_F)

clock.grid(row=0, column=0, sticky='w')
turn_ind.grid(row=0, column=1, sticky='ew', padx=5)
info.columnconfigure(turn_ind, weight=1)

###############################################################################
#   Path board
###############################################################################
game_space = tk.Canvas(root, **u.no_border)
game_space.configure(width=BOARD_W, height=BOARD_H, bg='green')

board = [[game_space.create_rectangle(pix(x, y), fill=u.EMPTY)
          for x in range(u.COLS)] for y in range(u.ROWS)]

info.pack(fill=tk.X)
game_space.pack(fill=tk.BOTH)

###############################################################################
#   Drawing
###############################################################################
def click(event):
    row, col = event.x//SQ_SIZE, event.y//SQ_SIZE
    _drag[0] = game_space.itemcget(board[col][row], 'fill')
    _drag[1] = [(row, col)]
    if _drag[0] == u.WALL: game_space.itemconfig(board[col][row], fill=u.EMPTY)
    else: game_space.itemconfig(board[col][row], fill=u.WALL)

def drag(event):
    row, col = event.x//SQ_SIZE, event.y//SQ_SIZE
    if (row, col) in _drag[1]: return
    if game_space.itemcget(board[col][row], 'fill') != _drag[0]: return
    if _drag[0] == u.WALL: game_space.itemconfig(board[col][row], fill=u.EMPTY)
    else: game_space.itemconfig(board[col][row], fill=u.WALL)

game_space.bind('<Button-1>', click)
game_space.bind('<B1-Motion>', drag)

###############################################################################
#   Main test
###############################################################################
if __name__ == "__main__":
    root.mainloop()
