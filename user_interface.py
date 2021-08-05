import tkinter as tk

import config

SQ_SIZE = 10
INFO_H = 100
BOARD_H = config.ROWS * SQ_SIZE
BOARD_W = config.COLS * SQ_SIZE
def pix(x, y): return (x*SQ_SIZE, y*SQ_SIZE, (x+1)*SQ_SIZE, (y+1)*SQ_SIZE)

# Fonts
TURN_F = f'Arial {INFO_H//4}'
CLOCK_F = f'Arial {INFO_H//4}'

# root initiation
root = tk.Tk()
root.title('Astar')
root.resizable(False, False)

# Info top box
info = tk.Frame(root)
turn_ind = tk.Label(info, text='Drawing', font=TURN_F)
clock = tk.Label(info, text='00.00', font=CLOCK_F)

info.configure(
    width=BOARD_W, height=INFO_H,
    padx=5, pady=5, bg='grey20')
clock.grid(row=0, column=0, sticky='w')
turn_ind.grid(row=0, column=1, sticky='ew', padx=5)
info.columnconfigure(turn_ind, weight=1)

# Game board
game_space = tk.Canvas(root, **config.no_border)
game_space.configure(width=BOARD_W, height=BOARD_H, bg='green')

board = [[game_space.create_rectangle(pix(x, y), fill=config.EMPTY)
          for x in range(config.COLS)] for y in range(config.ROWS)]

arrows = [[game_space.create_line(0,0, 0,0, fill='red', arrow=tk.LAST)
           for x in range(config.COLS)] for y in range(config.ROWS)]

def arrow_coord(orig, dest):
    return (
        (orig[1]+.5)*SQ_SIZE, (orig[0]+.5)*SQ_SIZE,
        (dest[1]+.5)*SQ_SIZE, (dest[0]+.5)*SQ_SIZE)

info.pack(fill=tk.X)
game_space.pack()

if __name__ == "__main__":
    
    root.mainloop()
